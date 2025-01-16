"""
WGUPS (Western Governors University Parcel Service) Parcel Management Module
This module implements parcel storage and management using a custom hash table implementation.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Any
import csv


@dataclass
class Parcel:
    """
    Represents a delivery parcel with all its attributes and status information.
    """
    parcel_id: int
    address: str
    city: str
    state: str
    zip_code: str
    deadline: datetime
    weight: str
    notes: str
    status: str = "at hub"
    dispatch_time: datetime = None
    delivery_time: datetime = None
    truck: Optional[int] = None

    def __post_init__(self):
        """Initialize datetime fields if they weren't set"""
        if self.dispatch_time is None:
            self.dispatch_time = datetime.strptime("00:00", '%H:%M')
        if self.delivery_time is None:
            self.delivery_time = datetime.strptime("00:00", '%H:%M')

    def __str__(self) -> str:
        """String representation of the parcel for display purposes."""
        return (f"{self.parcel_id}, {self.address}, {self.city}, {self.state}, "
                f"{self.zip_code}, {self.weight}, {self.deadline}, {self.notes}, "
                f"{self.status}, {self.delivery_time}")


class ParcelHash:
    """
    Custom hash table implementation for storing parcel data.
    Uses chaining for collision resolution.
    """
    def __init__(self, initial_capacity: int = 40):
        """
        Initialize hash table with given capacity.
        
        Args:
            initial_capacity: Initial size of the hash table
        """
        self.size: int = initial_capacity
        self.count: int = 0
        self.load_factor: float = 1.5
        self.table: List[List] = [[] for _ in range(self.size)]

    def _get_hash(self, parcel_id: int) -> List:
        """
        Get the bucket for a given parcel ID.
        
        Args:
            parcel_id: The ID of the parcel
            
        Returns:
            The bucket (list) where the parcel should be stored
        """
        index = hash(parcel_id) % self.size
        return self.table[index]

    def insert(self, parcel_id: int, parcel_data: Any) -> bool:
        """
        Insert or update a parcel in the hash table.
        
        Args:
            parcel_id: The ID of the parcel
            parcel_data: The parcel data to store
            
        Returns:
            True if insertion successful, False otherwise
        """
        bucket = self._get_hash(parcel_id)
        entry = [parcel_id, parcel_data]

        # Update existing parcel if found
        for item in bucket:
            if item[0] == parcel_id:
                item[1] = parcel_data
                return True

        # Add new parcel
        bucket.append(entry)
        self.count += 1

        # Check if resize needed
        if self.count / self.size > self.load_factor:
            self._resize()

        return True

    def lookup(self, parcel_id: int) -> Any:
        """
        Look up a parcel by ID.
        
        Args:
            parcel_id: The ID of the parcel to find
            
        Returns:
            The parcel data if found
            
        Raises:
            LookupError: If parcel not found
        """
        bucket = self._get_hash(parcel_id)
        for item in bucket:
            if item[0] == parcel_id:
                return item[1]
        raise LookupError(f"No parcel found with ID {parcel_id}")

    def _resize(self) -> None:
        """
        Double the size of the hash table when load factor exceeded.
        """
        # Store old data
        old_table = self.table

        # Double size and reset table
        self.size *= 2
        self.count = 0
        self.table = [[] for _ in range(self.size)]

        # Reinsert all items
        for bucket in old_table:
            for parcel_id, parcel_data in bucket:
                self.insert(parcel_id, parcel_data)


# Global instance of the parcel hash table
delivery_parcels = ParcelHash()


def read_parcels() -> dict:
    """
    Read parcel data from CSV and sort into truck loads based on constraints.
    
    Returns:
        Dictionary of truck loads with parcel IDs
    """
    loads = {1: [], 2: [], 3: []}
    sort_list = []
    loaded_list = []
    buddy_parcels = set()
    
    # Set end of day time
    EOD = datetime.strptime("17:00", '%H:%M')

    with open('./data/parcels.csv') as parcel_file:
        parcel_reader = csv.reader(parcel_file, delimiter=',')
        next(parcel_reader)  # Skip header

        # Create parcel objects from CSV data
        for row in parcel_reader:
            parcel_id = int(row[0])
            deadline = (datetime.strptime(row[5], '%H:%M %p') 
                      if row[5][0].isnumeric() else EOD)
            
            parcel = Parcel(
                parcel_id=parcel_id,
                address=row[1],
                city=row[2],
                state=row[3],
                zip_code=row[4],
                deadline=deadline,
                weight=row[6],
                notes=row[7]
            )
            
            delivery_parcels.insert(parcel_id, parcel)
            sort_list.append(parcel)

        sort_list.sort(key=lambda p: p.deadline)
        sort_copy = sort_list.copy()

        # Sort parcels into truck loads based on constraints
        for parcel in sort_list:
            if parcel.notes:
                # Handle truck-specific requirements
                if 'on truck' in parcel.notes:
                    truck_num = int(parcel.notes.split()[-1])
                    loads[truck_num].append(parcel.parcel_id)
                    loaded_list.append(parcel)
                    continue

                # Handle wrong address case
                elif 'Wrong address' in parcel.notes:
                    loads[3].append(parcel.parcel_id)
                    loaded_list.append(parcel)
                    continue

                # Handle buddy delivery requirements
                elif 'delivered with' in parcel.notes:
                    buddy_start = parcel.notes.find('with') + 5
                    buddies = parcel.notes[buddy_start:].split(', ')
                    buddy_parcels.add(parcel.parcel_id)
                    loaded_list.append(parcel)
                    
                    if parcel.parcel_id not in loads[1]:
                        loads[1].append(parcel.parcel_id)
                        for buddy in buddies:
                            buddy_id = int(buddy)
                            buddy_parcels.add(buddy_id)
                            for p in sort_copy:
                                if p.parcel_id == buddy_id and p.parcel_id not in loads[1]:
                                    loads[1].append(p.parcel_id)
                                    loaded_list.append(p)

                # Handle delayed parcels
                elif 'Delayed' in parcel.notes:
                    arrival = _parse_delay_time(parcel.notes)
                    if arrival.hour < 9:
                        loads[1].append(parcel.parcel_id)
                    elif arrival.hour < 10 or (arrival.hour == 10 and arrival.minute < 20):
                        loads[2].append(parcel.parcel_id)
                    else:
                        loads[3].append(parcel.parcel_id)
                    loaded_list.append(parcel)
                    continue

        # Remove assigned parcels from sort list
        _remove_assigned_parcels(sort_list, loads)
        
        # Get location data for each truck
        truck_locations = _get_truck_locations(loads, loaded_list)
        
        # Distribute remaining parcels
        _distribute_remaining_parcels(sort_list, loads, truck_locations, loaded_list)

    return loads


def update_statuses(query_time) -> None:
    """
    Update parcel statuses based on the query time.
    
    Args:
        query_time: Time to check status against
    """
    for parcel_id in range(1, 41):
        parcel = delivery_parcels.lookup(parcel_id)
        
        if query_time < parcel.dispatch_time.time():
            parcel.status = "at hub"
        elif parcel.dispatch_time.time() <= query_time < parcel.delivery_time.time():
            parcel.status = "en route"
        else:
            parcel.status = "delivered"


def _parse_delay_time(notes: str) -> datetime:
    """Parse delay time from notes string."""
    for part in notes.split():
        if part[0].isnumeric():
            return datetime.strptime(part, '%H:%M')
    return datetime.strptime("00:00", '%H:%M')


def _remove_assigned_parcels(sort_list: List[Parcel], loads: dict) -> None:
    """Remove parcels that have been assigned to trucks from the sort list."""
    assigned = set()
    for truck_load in loads.values():
        assigned.update(truck_load)
    
    sort_list[:] = [p for p in sort_list if p.parcel_id not in assigned]


def _get_truck_locations(loads: dict, loaded_list: List[Parcel]) -> dict:
    """Get addresses and zip codes for parcels in each truck load."""
    locations = {1: set(), 2: set(), 3: set()}
    
    for truck_id, truck_load in loads.items():
        for loaded in loaded_list:
            if loaded.parcel_id in truck_load:
                locations[truck_id].add(loaded.address)
                locations[truck_id].add(loaded.zip_code)
                
    return locations


def _distribute_remaining_parcels(
    sort_list: List[Parcel], 
    loads: dict,
    truck_locations: dict,
    loaded_list: List[Parcel]
) -> None:
    """Distribute remaining parcels to trucks based on location and capacity."""
    # First pass: Match by location
    for parcel in sort_list[:]:
        for truck_id, locations in truck_locations.items():
            if len(loads[truck_id]) < 16:
                if parcel.address in locations or parcel.zip_code in locations:
                    loads[truck_id].append(parcel.parcel_id)
                    sort_list.remove(parcel)
                    break

    # Second pass: Distribute remaining to least loaded truck
    while sort_list:
        parcel = sort_list[0]
        truck_id = min(loads, key=lambda k: len(loads[k]))
        
        if len(loads[truck_id]) >= 16:
            raise ValueError("Unable to distribute all parcels: trucks at capacity")
            
        loads[truck_id].append(parcel.parcel_id)
        sort_list.remove(parcel)