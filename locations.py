import csv


def import_distances():
    """
    Loads and processes distance matrix from CSV data source.
    Time Complexity: O(n²) where n is number of locations

    Returns:
        list[list[float]]: Matrix of distances between delivery points
    Raises:
        FileNotFoundError: If distance data file not found
        ValueError: If data format is invalid
    """
    try:
        with open('./data/distances.csv') as route_data:
            csv_parser = csv.reader(route_data)
            delivery_points = next(csv_parser)[2:]  # Skip first two columns of header

            # Initialize distance matrix
            matrix_size = len(delivery_points)
            distance_matrix = [[0.0] * matrix_size for _ in range(matrix_size)]

            # Populate matrix with distances
            for row_idx, row in enumerate(csv_parser):
                for col_idx, distance in enumerate(row[2:]):
                    try:
                        # Convert empty or invalid entries to None
                        distance_matrix[row_idx][col_idx] = float(distance) if distance.strip() else None
                    except ValueError:
                        distance_matrix[row_idx][col_idx] = None

            # Fill in symmetric entries
            for i in range(matrix_size):
                for j in range(i + 1, matrix_size):
                    if distance_matrix[i][j] is None and distance_matrix[j][i] is not None:
                        distance_matrix[i][j] = distance_matrix[j][i]
                    elif distance_matrix[j][i] is None and distance_matrix[i][j] is not None:
                        distance_matrix[j][i] = distance_matrix[i][j]

            return distance_matrix

    except FileNotFoundError:
        raise FileNotFoundError("distances.csv file not found in data directory")
    except Exception as e:
        raise ValueError(f"Error processing distance data: {str(e)}")


def import_addresses():
    """
    Extracts and standardizes delivery location addresses from CSV.
    Time Complexity: O(n) where n is number of locations

    Returns:
        list[str]: Clean list of delivery addresses
    Raises:
        FileNotFoundError: If distance data file not found
    """
    try:
        with open('./data/distances.csv') as route_data:
            csv_parser = csv.reader(route_data)
            raw_addresses = next(csv_parser)[2:]

            formatted_addresses = []
            for addr in raw_addresses:
                # Extract and clean main address line
                addr_parts = addr.strip().splitlines()
                if len(addr_parts) > 1:
                    main_address = addr_parts[1].strip(' ,')
                    formatted_addresses.append(main_address)
                else:
                    formatted_addresses.append(addr.strip())

            return formatted_addresses

    except FileNotFoundError:
        raise FileNotFoundError("distances.csv file not found in data directory")
    except Exception as e:
        raise ValueError(f"Error processing address data: {str(e)}")


def calculate_distance(route_segment, distance_matrix):
    """
    Computes total distance for a sequence of delivery points.
    Time Complexity: O(n) where n is length of route segment

    Args:
        route_segment (list): Sequence of location indices
        distance_matrix (list[list[float]]): Distance matrix
    Returns:
        float: Total distance of route segment
    Raises:
        ValueError: If invalid route points or missing distances
    """
    if not route_segment or len(route_segment) < 2:
        return 0.0

    total_distance = 0.0

    try:
        # Sum distances between consecutive points
        for i in range(len(route_segment) - 1):
            point_a = route_segment[i]
            point_b = route_segment[i + 1]

            # Check both directions in case of one-way distance recording
            distance = None
            if point_a < len(distance_matrix) and point_b < len(distance_matrix):
                if distance_matrix[point_a][point_b] is not None:
                    distance = distance_matrix[point_a][point_b]
                elif distance_matrix[point_b][point_a] is not None:
                    distance = distance_matrix[point_b][point_a]

            if distance is None:
                raise ValueError(f"Missing distance between points {point_a} and {point_b}")

            total_distance += distance

        return total_distance

    except IndexError:
        raise ValueError("Invalid location indices in route segment")


def get_location_index(address):
    """
    Finds index of location in address list.
    Time Complexity: O(n) where n is number of addresses

    Args:
        address (str): Address to look up
    Returns:
        int: Index of address in location list
    Raises:
        ValueError: If address not found
    """
    addresses = import_addresses()

    # Try exact match first
    try:
        return addresses.index(address)
    except ValueError:
        # Try fuzzy matching
        normalized_address = address.lower().replace(' ', '')
        normalized_addresses = [addr.lower().replace(' ', '') for addr in addresses]

        try:
            return normalized_addresses.index(normalized_address)
        except ValueError:
            raise ValueError(f"Address not found: {address}")


def get_address_by_index(index):
    """
    Gets address string for given location index.
    Time Complexity: O(1)

    Args:
        index (int): Location index
    Returns:
        str: Address at index
    Raises:
        IndexError: If invalid index
    """
    addresses = import_addresses()
    if 0 <= index < len(addresses):
        return addresses[index]
    else:
        raise IndexError(f"Invalid location index: {index}")
