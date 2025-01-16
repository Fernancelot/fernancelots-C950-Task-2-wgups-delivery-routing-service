"""
WGUPS (Western Governors University Parcel Service) routing module.
Implements the 3-opt algorithm for route optimization and manages the delivery process.

Overall Time Complexity: O(n³) due to 3-opt algorithm
Space Complexity: O(n) for route storage
"""

import datetime
import random
from math import inf
import locations
import parcels
import trucks


def initialize_routes():
    """
    Initialize and optimize delivery routes using 3-opt algorithm.
    Ensures all packages meet delivery requirements.
    
    Time Complexity: O(n³) for overall process
    Process Flow:
    1. Load initial data - O(n)
    2. Initialize trucks - O(n)
    3. Run 3-opt optimization - O(n³)
    4. Verify delivery times - O(n²)
    """
    # Load initial data - O(n)
    truck_loads = parcels.read_parcels()
    distance_matrix = locations.load_distance_data()
    location_list = list(locations.load_location_data())

    # Initialize trucks - O(n)
    trucks.load_trucks(truck_loads)

    # Handle special case for package with wrong address - O(n)
    _update_wrong_address()

    # Initialize tracking variables - O(1)
    best_distances = [inf, inf, inf]
    best_routes = [[], [], []]

    # Optimize routes using 3-opt algorithm - O(n³)
    for _ in range(100):  # Constant factor
        for i, truck in enumerate(trucks.delivery_trucks):
            best_routes[i] = optimize_route_3opt(truck, distance_matrix, location_list)
            best_distances[i] = _update_truck_route(truck, best_routes[i], best_distances[i], distance_matrix)

    # Verify and adjust routes to meet delivery deadlines - O(n²)
    _verify_delivery_times(distance_matrix, location_list)


def optimize_route_3opt(truck, distance_matrix, locations_list):
    """
    Optimize delivery route using 3-opt algorithm.
    Reduces route distance while avoiding crossing paths.
    
    Time Complexity: O(n³) where n is number of locations
    Process Flow:
    1. Initialize route points - O(n)
    2. Try all possible 3-way swaps - O(n³)
    3. Update if improvement found - O(1)
    
    Returns:
        Optimized delivery route
    """
    # Initialize with hub location - O(1)
    hub_idx = locations_list.index('4001 South 700 East')
    route_points = []

    # Map package addresses to location indices - O(n)
    for parcel in truck.parcels:
        for idx, location in enumerate(locations_list):
            if location == parcel.address:
                route_points.append(idx)
                break

    # Remove duplicates and randomize initial route - O(n)
    route_points = list(set(route_points))
    random.shuffle(route_points)

    # Add hub to start (and end for truck 1) - O(1)
    route_points.insert(0, hub_idx)
    if truck.id == 1:
        route_points.append(hub_idx)

    current_best = route_points
    improvements_possible = True

    # Main 3-opt optimization loop - O(n³)
    while improvements_possible:
        improvements_possible = False

        # Try all possible 3-opt moves - O(n³)
        for i in range(1, len(truck.parcels) - 3):
            for j in range(i + 1, len(truck.parcels) - 2):
                for k in range(j + 1, len(truck.parcels) - 1):
                    # Generate new route with 3-opt move - O(1)
                    new_route = (route_points[:i] + 
                               route_points[i:j + 1][::-1] + 
                               route_points[j + 1:k + 1][::-1] + 
                               route_points[k + 1:])

                    # Calculate distances for comparison - O(n)
                    current_distance = locations.calculate_distance(current_best, distance_matrix)
                    new_distance = locations.calculate_distance(new_route, distance_matrix)

                    # Update if improvement found - O(1)
                    if new_distance < current_distance:
                        current_best = new_route
                        improvements_possible = True

    return current_best


[Rest of the routing.py documentation continues...]