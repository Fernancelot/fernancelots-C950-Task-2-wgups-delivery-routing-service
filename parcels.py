import datetime
import csv
import cli_interface

class ParcelRegistry:
    """
    Implements an efficient registry for parcel tracking and management using a hash table structure.
    Provides O(1) average case lookup and insertion operations.
    """

    def __init__(self, initial_capacity=40):
        """
        Initializes registry with pre-allocated buckets for expected parcel volume.
        Time Complexity: O(1)
        """
        self.capacity = initial_capacity
        self.storage = [[] for _ in range(self.capacity)]
        self.entry_count = 0
        self.LOAD_THRESHOLD = 0.75

    def compute_index(self, tracking_id):
        """
        Maps tracking ID to storage bucket using hash function.
        Time Complexity: O(1)
        Args:
            tracking_id (int): Package tracking identifier
        Returns:
            int: Computed storage index
        """
        return hash(str(tracking_id)) % self.capacity

    def register_parcel(self, tracking_id, parcel_data):
        """
        Adds or updates parcel record in the registry.
        Handles collisions using chaining.
        Time Complexity: O(n) worst case for collision chains

        Args:
            tracking_id (int): Package tracking identifier
            parcel_data (Parcel): Package data object
        Returns:
            bool: Success status of registration
        """
        if not isinstance(tracking_id, int) or tracking_id < 1:
            raise ValueError("Invalid tracking ID")

        index = self.compute_index(tracking_id)
        bucket = self.storage[index]

        # Update existing entry if found
        for i, (existing_id, _) in enumerate(bucket):
            if existing_id == tracking_id:
                bucket[i] = (tracking_id, parcel_data)
                return True

        # Add new entry
        bucket.append((tracking_id, parcel_data))
        self.entry_count += 1

        # Check if resize needed
        if self.entry_count / self.capacity > self.LOAD_THRESHOLD:
            self._expand_capacity()

        return True

    def locate_parcel(self, tracking_id):
        """
        Retrieves parcel information by tracking ID.
        Time Complexity: O(n) worst case for collision chains

        Args:
            tracking_id (int): Package tracking identifier
        Returns:
            Parcel: Package data object
        Raises:
            LookupError: If package not found
        """
        if not isinstance(tracking_id, int) or tracking_id < 1:
            raise ValueError("Invalid tracking ID")

        index = self.compute_index(tracking_id)
        bucket = self.storage[index]

        for stored_id, parcel_data in bucket:
            if stored_id == tracking_id:
                return parcel_data

        raise LookupError(f"Package #{tracking_id} not found")

    def _expand_capacity(self):
        """
        Doubles registry capacity and redistributes entries.
        Time Complexity: O(n) where n is number of entries
        """
        # Store current entries
        entries = []
        for bucket in self.storage:
            entries.extend(bucket)

        # Reset storage with doubled capacity
        self.capacity *= 2
        self.storage = [[] for _ in range(self.capacity)]
        self.entry_count = 0

        # Reinsert all entries
        for tracking_id, parcel_data in entries:
            self.register_parcel(tracking_id, parcel_data)


class Parcel:
    """
    Represents an individual delivery parcel with tracking and routing information.
    """

    def __init__(self, tracking_id, destination, city, state, zip_code, deadline,
                 weight, special_instructions, assigned_vehicle=None):
        """
        Initializes parcel with delivery requirements and tracking details.
        Time Complexity: O(1)
        """
        self.tracking_id = tracking_id
        self.destination = destination
        self.dest_city = city
        self.dest_state = state
        self.dest_zip = zip_code
        self.deadline = self._parse_deadline(deadline)
        self.weight = weight
        self.special_instructions = special_instructions
        self.status = "at hub"
        self.start_time = None
        self.delivery_time = None
        self.assigned_vehicle = assigned_vehicle

    def _parse_deadline(self, deadline_str):
        """
        Parses deadline string into datetime object.
        Time Complexity: O(1)
        """
        if deadline_str.strip().upper() == 'EOD':
            return datetime.datetime.strptime('5:00 PM', '%I:%M %p')
        try:
            return datetime.datetime.strptime(deadline_str, '%I:%M %p')
        except ValueError:
            raise ValueError(f"Invalid deadline format: {deadline_str}")

    def __str__(self):
        """
        Provides formatted string representation of parcel details.
        Time Complexity: O(1)
        """
        status_str = f"{self.status}"
        if self.delivery_time:
            status_str += f" (Delivered at {self.delivery_time.strftime('%I:%M %p')})"
        elif self.start_time:
            status_str += f" (Started at {self.start_time.strftime('%I:%M %p')})"

        return (f"Package #{self.tracking_id}: {self.destination}, {self.dest_city}, "
                f"{self.dest_state} {self.dest_zip} | Weight: {self.weight} | "
                f"Deadline: {self.deadline.strftime('%I:%M %p')} | Status: {status_str}")


# Global registry instance
delivery_registry = ParcelRegistry()


def import_parcels():
    """
    Processes parcel data from CSV and organizes into vehicle loads.
    Time Complexity: O(n) where n is number of packages
    Returns:
        dict: Mapping of truck IDs to lists of package IDs
    """
    vehicle_loads = {1: [], 2: [], 3: []}
    processing_queue = []
    grouped_parcels = set()
#    EOD = datetime.datetime.strptime("5:00 PM", '%I:%M %p')

    try:
        with open('./data/parcels.csv') as parcel_data:
            csv_parser = csv.reader(parcel_data)

            # Process each parcel entry
            for row in csv_parser:
                # Clean the tracking ID string and convert to int
                tracking_id = int(row[0].strip().strip("'"))
                destination = row[1].strip()
                city = row[2].strip()
                state = row[3].strip()
                zip_code = row[4].strip()
                deadline = row[5].strip()
                weight = row[6].strip()
                special_instructions = row[7].strip()

                # Create and register parcel
                new_parcel = Parcel(tracking_id, destination, city, state, zip_code,
                                    deadline, weight, special_instructions)
                delivery_registry.register_parcel(tracking_id, new_parcel)
                processing_queue.append(new_parcel)

        # Sort by deadline
        processing_queue.sort(key=lambda p: p.deadline)

        # Process special instructions and constraints
        current_time = datetime.datetime.now().time()
        for parcel in processing_queue[:]:
            if parcel.special_instructions:
                if 'Must be delivered with' in parcel.special_instructions:
                    _handle_grouped_delivery(parcel, vehicle_loads, grouped_parcels)
                elif 'Delayed' in parcel.special_instructions:
                    _handle_delayed_delivery(parcel, vehicle_loads)
#                elif 'Wrong address' in parcel.special_instructions:
#                    _handle_wrong_address(parcel)
                elif 'Can only be on truck' in parcel.special_instructions:
                    truck_num = int(parcel.special_instructions[-1])
                    vehicle_loads[truck_num].append(parcel.tracking_id)
                    processing_queue.remove(parcel)

        # Distribute remaining packages
        _distribute_remaining_packages(processing_queue, vehicle_loads)

        return vehicle_loads

    except FileNotFoundError:
        raise FileNotFoundError("parcels.csv file not found in data directory")
    except Exception as e:
        raise Exception(f"Error importing parcels: {str(e)}")


def _handle_grouped_delivery(parcel, vehicle_loads, grouped_parcels):
    """Helper function to process grouped delivery requirements"""
    if parcel.tracking_id not in grouped_parcels:
        vehicle_loads[1].append(parcel.tracking_id)
        grouped_parcels.add(parcel.tracking_id)


def _handle_delayed_delivery(parcel, vehicle_loads):
    """Helper function to process delayed delivery requirements"""
    arrival_time = None
    for text in parcel.special_instructions.split():
        if ':' in text:
            arrival_time = datetime.datetime.strptime(text, '%H:%M').time()
            break

    if arrival_time:
        if arrival_time.hour < 9:
            vehicle_loads[1].append(parcel.tracking_id)
        elif arrival_time.hour < 10 or (arrival_time.hour == 10 and arrival_time.minute < 20):
            vehicle_loads[2].append(parcel.tracking_id)
        else:
            vehicle_loads[3].append(parcel.tracking_id)

"""
def _handle_wrong_address(parcel):
#    Helper function to process wrong address correction
    if parcel.tracking_id == 9:
        parcel.destination = "300 State St"
        parcel.dest_zip = "84103"
"""


def _distribute_remaining_packages(queue, vehicle_loads):
    """Helper function to distribute remaining packages across trucks"""
    for parcel in queue[:]:
        # Find truck with lowest current load
        truck_loads = [(i, len(packages)) for i, packages in vehicle_loads.items()]
        truck_loads.sort(key=lambda x: x[1])

        for truck_id, load_size in truck_loads:
            if load_size < 16:
                vehicle_loads[truck_id].append(parcel.tracking_id)
                queue.remove(parcel)
                break
        else:
            raise Exception("No available capacity on any truck")


def update_status(query_time):
    """
    Updates delivery status of all parcels based on query time.
    Time Complexity: O(n) where n is number of packages

    Args:
        query_time: Time to check status
    """
    for i in range(1, 41):
        try:
            parcel = delivery_registry.locate_parcel(i)
            if parcel:
                if not parcel.start_time or query_time < parcel.start_time.time():
                    parcel.status = "at hub"
                elif not parcel.delivery_time or query_time < parcel.delivery_time.time():
                    parcel.status = f"en route on truck {parcel.assigned_vehicle}"
                else:
                    parcel.status = "delivered"
        except LookupError:
            continue  # Skip if package not found
