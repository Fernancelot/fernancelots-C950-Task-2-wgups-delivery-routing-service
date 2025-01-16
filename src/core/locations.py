"""
WGUPS (Western Governors University Parcel Service) location management module.
Handles loading and processing of location data and distance calculations.
"""

import csv
from typing import List, Tuple, Optional


def load_distance_data() -> List[List[Optional[float]]]:
    """
    Load distance matrix from CSV file.
    
    Returns:
        2D list containing distances between locations.
        None values indicate missing direct distances.
    """
    with open('./data/distances.csv') as distance_file:
        csv_reader = csv.reader(distance_file)
        # Skip headers but get total number of locations
        location_count = len(next(csv_reader)[2:])
        
        # Initialize distance matrix with None values
        distance_matrix = [[None] * location_count for _ in range(location_count)]

        # Populate distance matrix from CSV data
        for row_idx, row in enumerate(csv_reader):
            for col_idx, distance in enumerate(row[2:]):
                if distance:  # Only process non-empty cells
                    distance_matrix[row_idx][col_idx] = float(distance)

    return distance_matrix


def load_location_data() -> List[str]:
    """
    Load and format location addresses from CSV file.
    
    Returns:
        List of formatted location addresses.
    """
    with open('./data/distances.csv') as distance_file:
        csv_reader = csv.reader(distance_file, delimiter=',')
        raw_addresses = next(csv_reader)[2:]  # Skip first two columns
        
        # Format addresses to include only first line
        formatted_addresses = []
        for address in raw_addresses:
            # Extract first line and remove trailing comma/space
            address_line = address.splitlines()[1].strip(', ')
            formatted_addresses.append(address_line)

    return formatted_addresses


def calculate_distance(route: List[int], distance_matrix: List[List[float]]) -> float:
    """
    Calculate total distance between consecutive locations in a route.
    
    Args:
        route: List of location indices representing the delivery route
        distance_matrix: 2D list of distances between locations
        
    Returns:
        Total distance of the route in miles
    """
    total_distance = 0.0

    # Calculate distance between each consecutive pair of locations
    for i in range(len(route) - 1):
        current_location = route[i]
        next_location = route[i + 1]

        # Get distance from matrix, checking both directions
        if distance_matrix[current_location][next_location] is not None:
            total_distance += distance_matrix[current_location][next_location]
        else:
            total_distance += distance_matrix[next_location][current_location]

    return total_distance


def calculate_route_segment(
    locations: Tuple[int, int], 
    distance_matrix: List[List[float]]
) -> float:
    """
    Calculate distance between two specific locations.
    
    Args:
        locations: Tuple of (start_location_index, end_location_index)
        distance_matrix: 2D list of distances between locations
        
    Returns:
        Distance between the two locations in miles
    """
    start_idx, end_idx = locations
    
    # Check both directions in the distance matrix
    if distance_matrix[start_idx][end_idx] is not None:
        return distance_matrix[start_idx][end_idx]
    return distance_matrix[end_idx][start_idx]  # Return reverse direction if forward is None