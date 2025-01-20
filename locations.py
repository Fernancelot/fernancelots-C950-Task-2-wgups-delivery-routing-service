import csv

def import_distances():
    """
    Loads and processes distance matrix from CSV data source.
    Constructs a 2D array containing all point-to-point distances.
    Time Complexity: O(n²)

    Returns:
        list[list[float]]: Matrix of distances between delivery points
    """

    with open('./data/distances.csv') as route_data:
        csv_parser = csv.reader(route_data)
        delivery_points = next(csv_parser)[2:]  # Skip first two columns of header row
        
        # Initialize empty distance matrix matching location count
        distance_matrix = [[None] * len(delivery_points) for _ in range(len(delivery_points))]

        # Populate matrix with distances from CSV
        # Sets None for missing/empty entries
        for row_idx, row in enumerate(csv_parser):
            for col_idx, distance in enumerate(row[2:]):  # Skip first two columns of each row
                distance_matrix[row_idx][col_idx] = float(distance) if distance else None

    return distance_matrix


def import_addresses():
    """
    Extracts and standardizes delivery location addresses from CSV.
    Formats each address to include only the primary street address.
    Time Complexity: O(n)

    Returns:
        list[str]: Clean list of delivery addresses
    """

    with open('./data/distances.csv') as route_data:
        csv_parser = csv.reader(route_data, delimiter=',')
        raw_addresses = next(csv_parser)[2:]  # Skip first two columns
        
        formatted_addresses = []
        # Process each address to extract main street line
        for addr in raw_addresses:
            main_address = addr.splitlines()[1].strip(', ')  # Get second line and trim
            formatted_addresses.append(main_address)

    return formatted_addresses


def calculate_distance(route_segment, distance_matrix):
    """
    Computes total distance for a sequence of delivery points.
    Handles bi-directional distance lookup between points.
    Time Complexity: O(n)

    Args:
        route_segment (list): Sequence of location indices to calculate distance between
        distance_matrix (list[list[float]]): Matrix of point-to-point distances
    
    Returns:
        float: Total distance of the route segment
    """

    segment_distance = 0.0

    # Calculate cumulative distance between consecutive points
    for i in range(len(route_segment) - 1):
        point_a = route_segment[i]
        point_b = route_segment[i + 1]

        # Check both directions in case of one-way distance recording
        if distance_matrix[point_a][point_b] is not None:
            segment_distance += distance_matrix[point_a][point_b]
        else:
            segment_distance += distance_matrix[point_b][point_a]

    return segment_distance
