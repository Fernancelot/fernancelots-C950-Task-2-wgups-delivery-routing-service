import datetime
import locations as dist
import parcels


class DeliveryVehicle:
    """
    Represents a delivery vehicle with routing and cargo management capabilities.
    """

    def __init__(self, vehicle_id, departure_time, operator_id):
        """
        Initializes delivery vehicle with operational parameters.
        Time Complexity: O(1)

        Args:
            vehicle_id: Unique identifier for vehicle
            departure_time: Scheduled start time
            operator_id: Assigned driver identifier
        """
        self.id = vehicle_id
        self.leave_time = datetime.datetime.strptime(departure_time, '%H:%M:%S')
        self.speed = 18  # Average speed in mph
        self.max_cargo = 16  # Maximum package capacity
        self.shipments = []  # Currently loaded parcels
        self.current_loc = 0  # Current location index
        self.distance_traveled = 0  # Accumulated route distance
        self.operator = operator_id  # Assigned driver
        self.route = []  # Planned delivery sequence


# Initialize delivery fleet
fleet = [
    DeliveryVehicle(1, '08:00:00', 1),
    DeliveryVehicle(2, '09:06:00', 2),
    DeliveryVehicle(3, '10:21:00', 1)
]


def initialize_fleet(cargo_loads):
    """
    Distributes parcels to vehicles based on optimized loading plan.
    Time Complexity: O(n²)

    Args:
        cargo_loads: Pre-sorted mapping of parcels to vehicles
    Returns:
        list[DeliveryVehicle]: Configured vehicle fleet
    """
    # Load parcels onto assigned vehicles - O(n)
    for load in cargo_loads[1]:
        fleet[0].shipments.append(parcels.delivery_registry.locate_parcel(load))
    for load in cargo_loads[2]:
        fleet[1].shipments.append(parcels.delivery_registry.locate_parcel(load))
    for load in cargo_loads[3]:
        fleet[2].shipments.append(parcels.delivery_registry.locate_parcel(load))

    # Update parcel tracking with vehicle assignments - O(n²)
    for vehicle in fleet:
        for item in vehicle.shipments:
            item.assigned_vehicle = vehicle.id

    return fleet


def calculate_progress(query_time, vehicle, distances):
    """
    Determines vehicle location and progress at specified time.
    Time Complexity: O(n)

    Args:
        query_time: Time point for progress calculation
        vehicle: Vehicle to track
        distances: Distance matrix for route calculations
    Returns:
        tuple: Current location index and total distance traveled
    """
    current_time = vehicle.leave_time
    current_loc = 0
    travel_distance = 0

    # Track progress through route until query time
    for i in range(len(vehicle.route) - 1):
        if current_time.time() < query_time:
            current_loc = vehicle.route[i]
            next_loc = vehicle.route[i + 1]

            # Update location and timing
            segment_distance = dist.calculate_distance((current_loc, next_loc), distances)
            current_loc = next_loc
            travel_distance += segment_distance
            segment_time = segment_distance / vehicle.speed
            current_time += datetime.timedelta(hours=segment_time)
        else:
            return current_loc, travel_distance

    return current_loc, travel_distance
