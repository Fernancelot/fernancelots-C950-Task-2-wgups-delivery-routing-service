import datetime
from math import inf
import random
import locations as dist
import parcels
import van

def coordinate_deliveries():
    """
    Master delivery coordination function. Controls loading, route optimization, and delivery timing.
    """
    # Load parcel data and prepare distance matrix
    shipments = parcels.import_parcels()
    route_distances = dist.import_distances()
    delivery_points = list(dist.import_addresses())

    # Initialize the fleet with loaded shipments
    van.initialize_fleet(shipments)

    # Adjust for known special cases (e.g., Package 9 address correction)
    for vehicle in van.fleet:
        for item in vehicle.shipments:
            item.start_time = vehicle.leave_time
            if item.tracking_id == 9:
                item.destination = '410 S State St'
                item.dest_city = 'Salt Lake City'
                item.dest_state = 'UT'
                item.dest_zip = '84111'

    # Initialize best routes and distances
    best_distances = [inf, inf, inf]
    best_paths = [[], [], []]

    # Optimize routes for each vehicle
    for _ in range(100):  # Iterative optimization
        for i, vehicle in enumerate(van.fleet):
            best_paths[i] = optimize_route(vehicle, route_distances, delivery_points)
            best_distances[i] = validate_and_update(vehicle, best_paths[i], best_distances[i], route_distances)

    # Rebalance loads and validate delivery times if needed
    for i in range(len(van.fleet)):
        for j in range(i + 1, len(van.fleet)):
            van1 = van.fleet[i]
            van2 = van.fleet[j]
            if not check_delivery_times(van1, route_distances, delivery_points) or \
               not check_delivery_times(van2, route_distances, delivery_points):
                rebalance_loads(van1, van2, route_distances, delivery_points)

    # Total mileage can be stored or returned but not printed here
    total_mileage = sum(vehicle.distance_traveled for vehicle in van.fleet)
    return total_mileage  # Return mileage to be handled elsewhere

def optimize_route(vehicle, distances, locations):
    """
    Optimize delivery routes for a single vehicle using a 3-opt algorithm.
    """
    hub = locations.index('4001 South 700 East')
    route_points = []

    # Map each shipment's address to location indices
    for item in vehicle.shipments:
        dest = item.destination
        for point in locations:
            if point == dest:
                route_points.append(locations.index(point))
                break

    # Prepare initial route with unique delivery points
    route_points = list(set(route_points))
    random.shuffle(route_points)

    # Add hub start/end points for round trips
    route_points.insert(0, hub)
    if vehicle.id == 1:
        route_points.append(hub)

    # Perform 3-opt optimization
    current_best = route_points
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route_points) - 3):
            for j in range(i + 1, len(route_points) - 2):
                for k in range(j + 1, len(route_points) - 1):
                    candidate = (
                        route_points[:i] +
                        route_points[i:j + 1][::-1] +
                        route_points[j + 1:k + 1][::-1] +
                        route_points[k + 1:]
                    )
                    current_dist = dist.calculate_distance(current_best, distances)
                    candidate_dist = dist.calculate_distance(candidate, distances)
                    if candidate_dist < current_dist:
                        current_best = candidate
                        improved = True
    return current_best

def validate_and_update(vehicle, final_route, best_distance, distances):
    """
    Validate a route and update it if it improves the vehicle's total distance.
    """
    new_dist = dist.calculate_distance(final_route, distances)
    if new_dist < best_distance:
        best_distance = new_dist
        vehicle.route = final_route
    return best_distance

def check_delivery_times(vehicle, distances, locations):
    """
    Check if all deliveries meet their respective deadlines.
    """
    current_time = vehicle.leave_time
    vehicle.distance_traveled = 0
    vehicle.current_loc = 0

    # Traverse the route and validate delivery times
    for i in range(len(vehicle.route) - 1):
        current = vehicle.route[i]
        next_stop = vehicle.route[i + 1]
        vehicle.current_loc = next_stop
        leg_distance = dist.calculate_distance((current, next_stop), distances)
        vehicle.distance_traveled += leg_distance
        travel_time = leg_distance / vehicle.speed
        current_time += datetime.timedelta(hours=travel_time)

        # Assign delivery times to packages
        for item in vehicle.shipments:
            if locations.index(item.destination) == next_stop:
                item.delivery_time = current_time

    # Ensure all shipments are delivered on time
    return all(item.delivery_time <= item.deadline for item in vehicle.shipments)

def rebalance_loads(van1, van2, distances, locations):
    """
    Rebalance loads between two vehicles if deliveries are not meeting constraints.
    """
    for item1 in van1.shipments:
        for item2 in van2.shipments:
            if not item1.special_instructions and not item2.special_instructions:
                route1_backup = van1.route.copy()
                route2_backup = van2.route.copy()
                van1.shipments.remove(item1)
                van2.shipments.remove(item2)
                van1.shipments.append(item2)
                van2.shipments.append(item1)
                item2.vehicle = 1
                item1.vehicle = 2
                van1.route = optimize_route(van1, distances, locations)
                van2.route = optimize_route(van2, distances, locations)
                if check_delivery_times(van1, distances, locations) and check_delivery_times(van2, distances, locations):
                    return True
                van1.shipments.remove(item2)
                van2.shipments.remove(item1)
                van1.shipments.append(item1)
                van2.shipments.append(item2)
                van1.route = route1_backup
                van2.route = route2_backup
    return False
