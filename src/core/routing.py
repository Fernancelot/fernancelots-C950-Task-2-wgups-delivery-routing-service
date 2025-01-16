"""
WGUPS (Western Governors University Parcel Service) routing module.
Implements the 3-opt algorithm for route optimization and handles the dispatch process.
"""

import datetime
import random
from math import inf
from src.core import locations, parcels, trucks


def initialize_routes():
    """
    Initialize and optimize delivery routes using 3-opt algorithm.
    Ensures all packages meet delivery requirements.

    Time Complexity: O(n²) for overall initialization process
    """
    # Load initial data
    truck_loads = parcels.read_parcels()
    distance_matrix = locations.load_distance_data()
    location_list = list(locations.load_location_data())

    # Initialize trucks with sorted packages
    trucks.load_trucks(truck_loads)

    # Handle special case for package with wrong address
    _update_wrong_address()

    # Initialize tracking variables
    best_distances = [inf, inf, inf]
    best_routes = [[], [], []]

    # Optimize routes using 3-opt algorithm
    for _ in range(100):  # Multiple attempts to find best routes
        for i, truck in enumerate(trucks.delivery_trucks):
            # Generate optimized route
            best_routes[i] = optimize_route_3opt(truck, distance_matrix, location_list)
            # Update if better route found
            best_distances[i] = _update_truck_route(truck, best_routes[i], best_distances[i], distance_matrix)

    # Verify and adjust routes to meet delivery deadlines
    _verify_delivery_times(distance_matrix, location_list)


def optimize_route_3opt(truck, distance_matrix, locations_list):
    """
    Optimize delivery route using 3-opt algorithm.
    Attempts to minimize route distance while avoiding crossing paths.

    Time Complexity: O(n³) for the 3-opt optimization
    """
    # Initialize with hub location
    hub_idx = locations_list.index('4001 South 700 East')
    route_points = []

    # Map package addresses to location indices
    for parcel in truck.parcels:
        for idx, location in enumerate(locations_list):
            if location == parcel.address:
                route_points.append(idx)
                break

    # Remove duplicates and randomize initial route
    route_points = list(set(route_points))
    random.shuffle(route_points)

    # Add hub to start (and end for truck 1)
    route_points.insert(0, hub_idx)
    if truck.id == 1:
        route_points.append(hub_idx)

    current_best = route_points
    improvements_possible = True

    while improvements_possible:
        improvements_possible = False

        # Try all possible 3-opt moves
        for i in range(1, len(truck.parcels) - 3):
            for j in range(i + 1, len(truck.parcels) - 2):
                for k in range(j + 1, len(truck.parcels) - 1):
                    # Generate new route with 3-opt move
                    new_route = (route_points[:i] +
                               route_points[i:j + 1][::-1] +
                               route_points[j + 1:k + 1][::-1] +
                               route_points[k + 1:])

                    # Calculate distances for comparison
                    current_distance = locations.calculate_distance(current_best, distance_matrix)
                    new_distance = locations.calculate_distance(new_route, distance_matrix)

                    # Update if improvement found
                    if new_distance < current_distance:
                        current_best = new_route
                        improvements_possible = True

    return current_best


def _update_truck_route(truck, new_route, current_best_distance, distance_matrix):
    """
    Update truck route if new route is better than current best.
    Returns the better distance of the two options.
    """
    new_distance = locations.calculate_distance(new_route, distance_matrix)
    if new_distance < current_best_distance:
        current_best_distance = new_distance
        truck.route = new_route

    return current_best_distance


def _verify_delivery_times(distance_matrix, locations_list):
    """
    Verify all packages will be delivered on time.
    Swap packages between trucks if needed to meet deadlines.
    """
    for i in range(len(trucks.delivery_trucks)):
        for j in range(i + 1, len(trucks.delivery_trucks)):
            truck1 = trucks.delivery_trucks[i]
            truck2 = trucks.delivery_trucks[j]

            if not _check_delivery_times(truck1, distance_matrix, locations_list) or \
               not _check_delivery_times(truck2, distance_matrix, locations_list):
                _swap_packages(truck1, truck2, distance_matrix, locations_list)


def _check_delivery_times(truck, distance_matrix, locations_list):
    """
    Check if all packages on a truck will be delivered by their deadlines.
    """
    current_time = truck.departure_time
    truck.distance_traveled = 0
    truck.current_location = 0

    for i in range(len(truck.route) - 1):
        # Calculate travel time and distance
        start_loc = truck.route[i]
        end_loc = truck.route[i + 1]
        truck.current_location = end_loc

        travel_distance = locations.calculate_route_segment((start_loc, end_loc), distance_matrix)
        truck.distance_traveled += travel_distance
        travel_time = travel_distance / truck.speed
        current_time += datetime.timedelta(hours=travel_time)

        # Update truck 3 departure if truck 1 returns later
        if truck.id == 1 and truck.current_location == 0 and \
           current_time > trucks.delivery_trucks[2].departure_time:
            trucks.delivery_trucks[2].departure_time = current_time

        # Update package delivery times
        for parcel in truck.parcels:
            if locations_list.index(parcel.address) == end_loc:
                parcel.delivery_time = current_time

    # Verify all deadlines are met
    return all(parcel.delivery_time <= parcel.deadline for parcel in truck.parcels)


def _swap_packages(truck1, truck2, distance_matrix, locations_list):
    """
    Attempt to swap packages between trucks to meet delivery deadlines.
    """
    for parcel1 in truck1.parcels:
        for parcel2 in truck2.parcels:
            if not parcel1.notes and not parcel2.notes:
                # Store current routes
                route1_backup = truck1.route.copy()
                route2_backup = truck2.route.copy()

                # Attempt swap
                truck1.parcels.remove(parcel1)
                truck2.parcels.remove(parcel2)
                truck1.parcels.append(parcel2)
                truck2.parcels.append(parcel1)
                parcel2.truck = truck1.id
                parcel1.truck = truck2.id

                # Optimize new routes
                truck1.route = optimize_route_3opt(truck1, distance_matrix, locations_list)
                truck2.route = optimize_route_3opt(truck2, distance_matrix, locations_list)

                # Check if new routes meet deadlines
                if _check_delivery_times(truck1, distance_matrix, locations_list) and \
                   _check_delivery_times(truck2, distance_matrix, locations_list):
                    return True

                # Revert changes if deadlines not met
                truck1.parcels.remove(parcel2)
                truck2.parcels.remove(parcel1)
                truck1.parcels.append(parcel1)
                truck2.parcels.append(parcel2)
                parcel1.truck = truck1.id
                parcel2.truck = truck2.id
                truck1.route = route1_backup
                truck2.route = route2_backup

    return False


def _update_wrong_address():
    """Update the address for the package with incorrect address."""
    for truck in trucks.delivery_trucks:
        for parcel in truck.parcels:
            parcel.dispatch_time = truck.departure_time
            if parcel.parcel_id == 9:
                parcel.address = '410 S State St'
                parcel.city = 'Salt Lake City'
                parcel.state = 'UT'
                parcel.zip_code = '84111'