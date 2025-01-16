"""
WGUPS (Western Governors University Parcel Service) truck management module.
Handles truck objects, loading, and route progress tracking.
"""

import datetime
from typing import List, Tuple
import locations
import parcels


class Truck:
    """
    Represents a delivery truck with its attributes and current state.
    """
    def __init__(self, truck_id: int, departure: str, driver: int):
        """
        Initialize a new truck.

        Args:
            truck_id: Unique identifier for the truck
            departure: Departure time in HH:MM:SS format
            driver: Driver ID (1 or 2)
        """
        self.id = truck_id
        self.departure_time = datetime.datetime.strptime(departure, '%H:%M:%S')
        self.speed = 18  # Average speed in mph
        self.max_parcels = 16
        self.parcels: List = []
        self.current_location = 0
        self.distance_traveled = 0.0
        self.driver = driver
        self.route: List = []


# Initialize the three delivery trucks with specific departure times and drivers
delivery_trucks = [
    Truck(1, '08:00:00', 1),  # First truck, first driver
    Truck(2, '09:06:00', 2),  # Second truck, second driver
    Truck(3, '10:21:00', 1)   # Third truck, first driver returns
]


def load_trucks(truck_loads: dict) -> List[Truck]:
    """
    Load trucks with parcels based on the sorted loads.

    Args:
        truck_loads: Dictionary mapping truck IDs to lists of parcel IDs

    Returns:
        List of loaded truck objects
    """
    # Assign parcels to trucks
    for parcel_id in truck_loads[1]:
        delivery_trucks[0].parcels.append(parcels.wgups_parcels.lookup(parcel_id))
    for parcel_id in truck_loads[2]:
        delivery_trucks[1].parcels.append(parcels.wgups_parcels.lookup(parcel_id))
    for parcel_id in truck_loads[3]:
        delivery_trucks[2].parcels.append(parcels.wgups_parcels.lookup(parcel_id))

    # Set truck assignment for each parcel
    for truck in delivery_trucks:
        for parcel in truck.parcels:
            parcel.truck = truck.id

    return delivery_trucks


def calculate_route_progress(
    query_time: datetime.time,
    truck: Truck,
    distances: List[List[float]]
) -> Tuple[int, float]:
    """
    Calculate truck's progress along its route at the given time.

    Args:
        query_time: Time to check progress
        truck: Truck to check
        distances: Distance matrix between locations

    Returns:
        Tuple of (current location index, miles traveled)
    """
    current_time = truck.departure_time
    current_loc = 0
    miles = 0.0

    # Follow route until query time is reached
    for i in range(len(truck.route) - 1):
        if current_time.time() < query_time:
            current_loc = truck.route[i]
            next_loc = truck.route[i + 1]

            # Calculate distance and time to next location
            segment_distance = locations.calculate_route_segment((current_loc, next_loc), distances)
            current_loc = next_loc
            miles += segment_distance
            
            # Update time based on speed
            travel_time = segment_distance / truck.speed
            current_time += datetime.timedelta(hours=travel_time)
        else:
            break

    return current_loc, miles