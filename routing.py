import datetime
from math import inf
import random
import locations as dist
import parcels
import van


def coordinate_deliveries():
    """
    Master delivery coordination function. Controls loading, route optimization, and delivery timing.
    Time Complexity: O(n³) where n is number of delivery points

    Returns:
        float: Total combined mileage for all trucks
    """
    try:
        # Initialize data
        shipments = parcels.import_parcels()
        route_distances = dist.import_distances()
        delivery_points = dist.import_addresses()

        # Initialize fleet
        van.initialize_fleet(shipments)

        # Handle special cases and constraints
        _handle_special_cases()

        # Optimize routes
        best_routes = _optimize_all_routes(route_distances, delivery_points)

        # Assign routes and verify constraints
        _assign_and_verify_routes(best_routes, route_distances, delivery_points)

        # Calculate and return total mileage
        return van.get_total_mileage()

    except Exception as e:
        raise Exception(f"Error coordinating deliveries: {str(e)}")


def _handle_special_cases():
    """
    Handles special package requirements like address corrections.
    Time Complexity: O(n) where n is number of packages
    """
    # Handle package #9 address correction
    try:
        package_9 = parcels.delivery_registry.locate_parcel(9)
        if package_9:
            package_9.destination = "410 S State St"
            package_9.dest_city = "Salt Lake City"
            package_9.dest_state = "UT"
            package_9.dest_zip = "84111"
    except LookupError:
        pass  # Package 9 not found


def _optimize_all_routes(distances, locations):
    """
    Optimizes routes for all vehicles using 3-opt algorithm.
    Time Complexity: O(n³) where n is number of delivery points
    """
    best_routes = []
    best_distances = []

    for vehicle in van.fleet:
        route = _create_initial_route(vehicle, locations)
        optimized_route = _optimize_route(route, distances)
        best_routes.append(optimized_route)
        best_distances.append(dist.calculate_distance(optimized_route, distances))

    return best_routes


def _create_initial_route(vehicle, locations):
    hub_index = locations.index("4001 South 700 East")
    delivery_points = []

    # Map package destinations to location indices
    for package in vehicle.shipments:
        try:
            point_index = dist.get_location_index(package.destination)
            if point_index not in delivery_points:
                delivery_points.append(point_index)
        except ValueError:
            continue

    # Only add return to hub for first vehicle
    route = [hub_index]
    route.extend(delivery_points)
    if vehicle.id == 1:  # Only first truck returns to hub
        route.append(hub_index)

    return route


def _optimize_route(route, distances, max_iterations=100):
    """
    Optimizes route using 3-opt local search algorithm.
    Time Complexity: O(n³) where n is route length
    """
    best_route = _greedy_improve(route.copy(), distances)
    best_distance = dist.calculate_distance(best_route, distances)

    for _ in range(max_iterations):
        improved = False
        for i in range(1, len(route) - 3):
            for j in range(i + 1, len(route) - 2):
                for k in range(j + 1, len(route) - 1):
                    new_route = (
                            route[:i] +
                            route[i:j + 1][::-1] +
                            route[j + 1:k + 1][::-1] +
                            route[k + 1:]
                    )
                    new_distance = dist.calculate_distance(new_route, distances)
                    if new_distance < best_distance:
                        best_route = new_route
                        best_distance = new_distance
                        improved = True
        if not improved:
            break
    return best_route

def _greedy_improve(route, distances):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                new_route = route.copy()
                new_route[i], new_route[j] = new_route[j], new_route[i]
                if dist.calculate_distance(new_route, distances) < dist.calculate_distance(route, distances):
                    route = new_route
                    improved = True
    return route



def _assign_and_verify_routes(routes, distances, locations):
    """
    Assigns optimized routes to vehicles and verifies delivery constraints.
    Time Complexity: O(n) where n is total number of packages
    """
    for vehicle, route in zip(van.fleet, routes):
        vehicle.route = route
        _verify_delivery_times(vehicle, distances, locations)


def _verify_delivery_times(vehicle, distances, locations):
    """
    Verifies all packages will be delivered on time.
    Time Complexity: O(n) where n is number of route points
    """
    current_time = vehicle.leave_time
    current_loc = 0

    # Track progress through route
    for i in range(len(vehicle.route) - 1):
        current = vehicle.route[i]
        next_stop = vehicle.route[i + 1]

        # Calculate arrival time at next stop
        segment_distance = dist.calculate_distance([current, next_stop], distances)
        travel_time = segment_distance / vehicle.speed
        arrival_time = current_time + datetime.timedelta(hours=travel_time)

        # Update delivery times and verify deadlines
        for package in vehicle.shipments:
            try:
                delivery_point = dist.get_location_index(package.destination)
                if delivery_point == next_stop:
                    package.delivery_time = arrival_time
                    if arrival_time.time() > package.deadline.time():
                        raise ValueError(f"Package {package.tracking_id} will miss deadline")
            except ValueError:
                continue

        current_time = arrival_time
        current_loc = next_stop


def rebalance_loads(van1, van2, distances, locations):
    """
    Attempts to rebalance loads between two vehicles to meet delivery constraints.
    Time Complexity: O(n²) where n is number of packages
    """
    # Try swapping non-constrained packages
    for pkg1 in van1.shipments:
        for pkg2 in van2.shipments:
            if not pkg1.special_instructions and not pkg2.special_instructions:
                # Backup current routes
                route1_backup = van1.route.copy()
                route2_backup = van2.route.copy()

                # Try swap
                van1.shipments.remove(pkg1)
                van2.shipments.remove(pkg2)
                van1.shipments.append(pkg2)
                van2.shipments.append(pkg1)

                # Reoptimize routes
                van1.route = _optimize_route(_create_initial_route(van1, locations), distances)
                van2.route = _optimize_route(_create_initial_route(van2, locations), distances)

                # Verify constraints
                try:
                    _verify_delivery_times(van1, distances, locations)
                    _verify_delivery_times(van2, distances, locations)
                    return True
                except ValueError:
                    # Restore original configuration if swap fails
                    van1.shipments.remove(pkg2)
                    van2.shipments.remove(pkg1)
                    van1.shipments.append(pkg1)
                    van2.shipments.append(pkg2)
                    van1.route = route1_backup
                    van2.route = route2_backup

    return False


def optimize_fleet_routes():
    """
    Optimizes routes for entire fleet ensuring all constraints are met.
    Time Complexity: O(n³) where n is total number of delivery points
    """
    route_distances = dist.import_distances()
    delivery_points = dist.import_addresses()

    # Optimize each vehicle's route
    for vehicle in van.fleet:
        # Create and optimize initial route
        route = _create_initial_route(vehicle, delivery_points)
        optimized_route = _optimize_route(route, route_distances)
        vehicle.route = optimized_route

        # Verify delivery times
        try:
            _verify_delivery_times(vehicle, route_distances, delivery_points)
        except ValueError as e:
            # If constraints not met, try rebalancing with other vehicles
            for other_vehicle in van.fleet:
                if other_vehicle != vehicle:
                    if rebalance_loads(vehicle, other_vehicle, route_distances, delivery_points):
                        break
            else:
                raise ValueError(f"Could not find valid route configuration: {str(e)}")
