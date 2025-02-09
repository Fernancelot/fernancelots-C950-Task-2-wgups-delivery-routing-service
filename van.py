import datetime
import locations as dist
import parcels


class DeliveryVehicle:
    """
    Represents a delivery vehicle with routing and cargo management capabilities.
    Time Complexity: O(1) for initialization
    """

    def __init__(self, vehicle_id, departure_time, operator_id):
        """
        Initializes delivery vehicle with operational parameters.
        Args:
            vehicle_id (int): Unique identifier for vehicle
            departure_time (str): Scheduled start time ('HH:MM:SS')
            operator_id (int): Assigned driver identifier
        """
        self.id = vehicle_id
        self.leave_time = datetime.datetime.strptime(departure_time, '%H:%M:%S')
        self.speed = 18.0  # Average speed in mph
        self.max_cargo = 16  # Maximum package capacity
        self.shipments = []  # Currently loaded parcels
        self.current_loc = 0  # Current location index (0 = hub)
        self.distance_traveled = 0.0  # Accumulated route distance
        self.operator = operator_id  # Assigned driver
        self.route = []  # Planned delivery sequence
        self.status = "at hub"
        self.last_location = None
        self.current_delivery = None

    def __str__(self):
        """
        Provides string representation of vehicle status.
        Time Complexity: O(1)
        """
        return (f"Truck {self.id} | Driver {self.operator} | "
                f"Status: {self.status} | Packages: {len(self.shipments)}/{self.max_cargo} | "
                f"Distance: {self.distance_traveled:.1f} miles")

    def update_status(self, current_time):
        """
        Updates vehicle status based on current time.
        Time Complexity: O(1)
        """
        if current_time < self.leave_time.time():
            self.status = "at hub"
        elif self.route and self.distance_traveled > 0:
            self.status = "en route"
        else:
            self.status = "completed deliveries"


# Initialize delivery fleet
fleet = [
    DeliveryVehicle(1, '08:00:00', 1),  # First truck leaves at 8:00 AM
    DeliveryVehicle(2, '09:05:00', 2),  # Second truck leaves at 9:05 AM
    DeliveryVehicle(3, '10:20:00', 1)  # Third truck leaves at 10:20 AM (after address correction)
]


def initialize_fleet(cargo_loads):
    """
    Distributes parcels to vehicles based on optimized loading plan.
    Time Complexity: O(n) where n is total number of packages

    Args:
        cargo_loads (dict): Pre-sorted mapping of parcels to vehicles
    Returns:
        list[DeliveryVehicle]: Configured vehicle fleet
    """
    try:
        # Load packages onto assigned vehicles
        for vehicle_id, package_ids in cargo_loads.items():
            vehicle = next(v for v in fleet if v.id == vehicle_id)

            if len(package_ids) > vehicle.max_cargo:
                raise ValueError(f"Too many packages assigned to vehicle {vehicle_id}")

            for package_id in package_ids:
                package = parcels.delivery_registry.locate_parcel(package_id)
                if package:
                    vehicle.shipments.append(package)
                    package.assigned_vehicle = vehicle.id
                    package.start_time = vehicle.leave_time
                else:
                    raise LookupError(f"Package {package_id} not found")

        return fleet

    except Exception as e:
        raise Exception(f"Error initializing fleet: {str(e)}")


def calculate_progress(query_time, vehicle, distances):
    """
    Determines vehicle location and progress at specified time.
    Time Complexity: O(n) where n is number of route points

    Args:
        query_time: Time point for progress calculation
        vehicle: Vehicle to track
        distances: Distance matrix for route calculations
    Returns:
        tuple: Current location index and total distance traveled
    """
    if not isinstance(query_time, datetime.time):
        raise ValueError("Invalid query time format")

    # Reset progress tracking
    current_time = vehicle.leave_time
    current_loc = 0
    travel_distance = 0.0

    # If before departure time, return hub location
    if query_time < vehicle.leave_time.time():
        return current_loc, travel_distance

    # Track progress through route
    for i in range(len(vehicle.route) - 1):
        current = vehicle.route[i]
        next_stop = vehicle.route[i + 1]

        # Calculate segment distance and time
        segment_distance = dist.calculate_distance([current, next_stop], distances)
        travel_time = segment_distance / vehicle.speed  # Hours
        segment_arrival = current_time + datetime.timedelta(hours=travel_time)

        # Update delivery times for packages at this stop
        if query_time >= segment_arrival.time():
            current_loc = next_stop
            travel_distance += segment_distance
            current_time = segment_arrival

            # Update package delivery times
            for package in vehicle.shipments:
                if dist.get_location_index(package.destination) == next_stop:
                    package.delivery_time = segment_arrival
        else:
            # Interpolate position between stops
            time_ratio = ((query_time.hour * 3600 + query_time.minute * 60 + query_time.second) -
                          (current_time.hour * 3600 + current_time.minute * 60 + current_time.second)) / \
                         (travel_time * 3600)
            travel_distance += segment_distance * time_ratio
            break

    vehicle.distance_traveled = travel_distance
    vehicle.current_loc = current_loc
    vehicle.update_status(query_time)

    return current_loc, travel_distance


def get_total_mileage():
    """
    Calculates total mileage for all vehicles.
    Time Complexity: O(1)
    Returns:
        float: Combined mileage of all vehicles
    """
    return sum(vehicle.distance_traveled for vehicle in fleet)


def get_vehicle_location_name(vehicle, addresses):
    """
    Gets the current location name for a vehicle.
    Time Complexity: O(1)

    Args:
        vehicle: Vehicle to locate
        addresses: List of delivery addresses
    Returns:
        str: Current location name
    """
    if vehicle.status == "at hub":
        return "WGUPS Hub"
    elif vehicle.current_loc < len(addresses):
        return addresses[vehicle.current_loc]
    else:
        return "Unknown Location"