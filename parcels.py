import datetime
import csv


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
    EOD = datetime.datetime.strptime("5:00 PM", '%I:%M %p')

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
        for parcel in processing_queue[:]:
            if parcel.special_instructions:
                if 'Must be delivered with' in parcel.special_instructions:
                    _handle_grouped_delivery(parcel, vehicle_loads, grouped_parcels)
                elif 'Delayed' in parcel.special_instructions:
                    _handle_delayed_delivery(parcel, vehicle_loads)
                elif 'Wrong address' in parcel.special_instructions:
                    vehicle_loads[3].append(parcel.tracking_id)
                    processing_queue.remove(parcel)
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
            continue  # Skip if package not foundimport datetime
import csv

class ParcelRegistry:
    """
    Implements an efficient registry for parcel tracking and management using a hash table structure.
    Provides O(1) average case lookup and insertion operations.
    """

    LOAD_THRESHOLD = 1.5  # Maximum load factor before resizing
    entry_count = 0

    def __init__(self):
        """
        Initializes registry with pre-allocated buckets for expected parcel volume.
        Time Complexity: O(1)
        """
        self.capacity = 40  # Initial size based on expected parcel count
        self.storage = [[] for _ in range(self.capacity)]

    def compute_index(self, tracking_id):
        """
        Maps tracking ID to storage bucket using hash function.
        Time Complexity: O(1)
        """
        return hash(tracking_id) % self.capacity

    def register_parcel(self, tracking_id, parcel_data):
        """
        Adds or updates parcel record in the registry.
        Handles collisions using chaining.
        Time Complexity: O(n) worst case for collision chains
        """
        index = self.compute_index(tracking_id)
        target_bucket = self.storage[index]
        entry = [tracking_id, parcel_data]

        # Update existing entry if found
        for record in target_bucket:
            if record[0] == tracking_id:
                record[1] = parcel_data
                return True

        # Add new entry if not found
        target_bucket.append(entry)
        self.entry_count += 1

        # Check if resize needed
        if self.entry_count / self.capacity > self.LOAD_THRESHOLD:
            self.expand_capacity()

        return True

    def locate_parcel(self, tracking_id):
        """
        Retrieves parcel information by tracking ID.
        Time Complexity: O(n) worst case for collision chains
        """
        index = self.compute_index(tracking_id)
        target_bucket = self.storage[index]

        # Search within the target bucket
        if target_bucket:
            for record in target_bucket:
                if record[0] == tracking_id:
                    return record[1]
            raise LookupError(f"No record found for tracking ID {tracking_id}")
        raise LookupError("Registry lookup operation failed")

    def expand_capacity(self):
        """
        Doubles registry capacity and redistributes entries.
        Maintains load factor below threshold.
        Time Complexity: O(n²) for redistribution
        """
        # Preserve existing entries
        temp_storage = []
        for bucket in self.storage:
            for record in bucket:
                temp_storage.append(record)

        # Reset and expand registry
        self.capacity *= 2
        self.storage = [[] for _ in range(self.capacity)]
        self.entry_count = 0

        # Redistribute entries
        for tracking_id, parcel_data in temp_storage:
            self.register_parcel(tracking_id, parcel_data)


class Parcel:
    """
    Represents an individual delivery parcel with tracking and routing information.
    """

    def __init__(self, tracking_id, destination, city, state, zip_code, deadline,
                 weight, special_instructions, assigned_vehicle):
        """
        Initializes parcel with delivery requirements and tracking details.
        Time Complexity: O(1)
        """
        self.tracking_id = tracking_id
        self.destination = destination
        self.dest_city = city
        self.dest_state = state
        self.dest_zip = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_instructions = special_instructions
        self.status = "at hub"
        self.start_time = datetime.datetime.strptime("08:00", '%H:%M')  # Default start time
        self.delivery_time = datetime.datetime.strptime("17:00", '%H:%M')  # Default end time
        self.assigned_vehicle = assigned_vehicle

    def __str__(self):
        """
        Provides formatted string representation of parcel details.
        Time Complexity: O(1)
        """
        return (f"{self.tracking_id}, {self.destination}, {self.dest_city}, "
                f"{self.dest_state}, {self.dest_zip}, {self.weight}, "
                f"{self.deadline}, {self.special_instructions}, {self.status}, "
                f"{self.delivery_time}")


delivery_registry = ParcelRegistry()

def import_parcels():
    """
    Processes parcel data from CSV and organizes into vehicle loads.
    Time Complexity: O(n)
    """
    grouped_parcels = set()
    vehicle_loads = {1: [], 2: [], 3: []}
    processing_queue = []
    assigned_parcels = []
    EOD = datetime.datetime.strptime("16:59:59", '%H:%M:%S')

    try:
        with open('./data/parcels.csv') as parcel_data:
            csv_parser = csv.reader(parcel_data, delimiter=',')

            # Process each parcel entry
            for row in csv_parser:
                tracking_id = int(row[0])
                destination = row[1]
                city = row[2]
                state = row[3]
                zip_code = row[4]
                deadline = (datetime.datetime.strptime(row[5], '%I:%M %p')
                            if row[5][0].isnumeric() else EOD)
                weight = row[6]
                special_instructions = row[7]
                assigned_vehicle = None

                # Create and register parcel
                new_parcel = Parcel(tracking_id, destination, city, state, zip_code,
                                    deadline, weight, special_instructions, assigned_vehicle)
                delivery_registry.register_parcel(tracking_id, new_parcel)

                # Queue for sorting
                processing_queue.append(new_parcel)

            processing_queue.sort(key=lambda p: p.deadline)
            remaining_parcels = processing_queue.copy()

            # Sort parcels into vehicle loads based on constraints
            for parcel in processing_queue:
                if parcel.special_instructions:
                    # Handle vehicle-specific assignments
                    if 'on truck' in parcel.special_instructions:
                        target_vehicle = parcel.special_instructions.split()[-1].strip("'")
                        vehicle_loads[int(target_vehicle)].append(parcel.tracking_id)
                        assigned_parcels.append(parcel)
                        continue

                    # Handle address corrections
                    elif 'Wrong address' in parcel.special_instructions:
                        vehicle_loads[3].append(parcel.tracking_id)
                        assigned_parcels.append(parcel)
                        continue

                    # Handle grouped deliveries
                    elif 'delivered with' in parcel.special_instructions:
                        start_idx = parcel.special_instructions.find('with') + 5
                        group = parcel.special_instructions[start_idx:].split(', ')
                        grouped_parcels.add(parcel.tracking_id)
                        assigned_parcels.append(parcel)

                        if parcel.tracking_id not in vehicle_loads[1]:
                            vehicle_loads[1].append(parcel.tracking_id)
                            for companion in group:
                                grouped_parcels.add(int(companion))
                                for p in remaining_parcels:
                                    if int(companion) == p.tracking_id and \
                                            p.tracking_id not in vehicle_loads[1]:
                                        vehicle_loads[1].append(p.tracking_id)
                                        assigned_parcels.append(p)

                    # Handle delayed arrivals
                    elif 'Delayed' in parcel.special_instructions:
                        arrival = parcel.special_instructions.split(' ')
                        for text in arrival:
                            if text[0].isnumeric():
                                arrival = datetime.datetime.strptime(text, '%H:%M').time()

                        if arrival.hour < 9:
                            vehicle_loads[1].append(parcel.tracking_id)
                        elif arrival.hour < 10 or (arrival.hour == 10 and arrival.minute < 20):
                            vehicle_loads[2].append(parcel.tracking_id)
                        else:
                            vehicle_loads[3].append(parcel.tracking_id)
                        assigned_parcels.append(parcel)
                        continue

            # Remove assigned parcels from processing queue
            for parcel_id in vehicle_loads[1], vehicle_loads[2], vehicle_loads[3]:
                for pid in parcel_id:
                    for parcel in remaining_parcels:
                        if parcel.tracking_id == pid:
                            processing_queue.remove(parcel)
                    continue

            remaining_parcels = processing_queue.copy()
            zones1, zones2, zones3 = [], [], []

            # Group parcels by delivery zone
            for load in vehicle_loads[1]:
                for assigned in assigned_parcels:
                    if assigned.tracking_id == load:
                        zones1.append(assigned.destination)
                        zones1.append(assigned.dest_zip)
            for load in vehicle_loads[2]:
                for assigned in assigned_parcels:
                    if assigned.tracking_id == load:
                        zones2.append(assigned.destination)
                        zones2.append(assigned.dest_zip)
            for load in vehicle_loads[3]:
                for assigned in assigned_parcels:
                    if assigned.tracking_id == load:
                        zones3.append(assigned.destination)
                        zones3.append(assigned.dest_zip)

            # Assign early deadline parcels to matching zones
            for parcel in remaining_parcels:
                if parcel.deadline != EOD:
                    if ((parcel.destination in zones1 or parcel.dest_zip in zones1)
                            and len(vehicle_loads[1]) < 16):
                        vehicle_loads[1].append(parcel.tracking_id)
                        assigned_parcels.append(parcel)
                        processing_queue.remove(parcel)

            remaining_parcels = processing_queue.copy()

            # Assign remaining early deadline parcels
            for parcel in remaining_parcels:
                if parcel.deadline != EOD:
                    vehicle_loads[1].append(parcel.tracking_id)
                    processing_queue.remove(parcel)
                elif parcel.deadline == EOD:
                    break

            remaining_parcels = processing_queue.copy()

            # Assign by matching addresses
            for load in vehicle_loads[1], vehicle_loads[2], vehicle_loads[3]:
                for assigned in assigned_parcels:
                    if assigned.tracking_id in load:
                        for parcel in remaining_parcels:
                            if parcel.destination == assigned.destination:
                                if len(load) < 16:
                                    load.append(parcel.tracking_id)
                                    processing_queue.remove(parcel)

            remaining_parcels = processing_queue

            # Assign by matching zip codes
            for load in vehicle_loads[1], vehicle_loads[2], vehicle_loads[3]:
                for assigned in assigned_parcels:
                    if assigned.tracking_id in load:
                        for parcel in remaining_parcels:
                            if parcel.dest_zip == assigned.dest_zip:
                                if len(load) < 16:
                                    load.append(parcel.tracking_id)
                                    processing_queue.remove(parcel)

            # Distribute remaining parcels
            for parcel in processing_queue.copy():
                # Assign to vehicle with lowest current load
                if (len(vehicle_loads[1]) < 16 and
                        len(vehicle_loads[1]) <= len(vehicle_loads[2]) and
                        len(vehicle_loads[1]) <= len(vehicle_loads[3])):
                    vehicle_loads[1].append(parcel.tracking_id)
                    processing_queue.remove(parcel)
                elif (len(vehicle_loads[2]) < 16 and
                      len(vehicle_loads[2]) <= len(vehicle_loads[1]) and
                      len(vehicle_loads[2]) <= len(vehicle_loads[3])):
                    vehicle_loads[2].append(parcel.tracking_id)
                    processing_queue.remove(parcel)
                elif (len(vehicle_loads[3]) < 16 and
                      len(vehicle_loads[3]) <= len(vehicle_loads[2]) and
                      len(vehicle_loads[3]) <= len(vehicle_loads[1])):
                    vehicle_loads[3].append(parcel.tracking_id)
                    processing_queue.remove(parcel)
                else:
                    raise IndexError('Vehicle capacity exceeded')

            return vehicle_loads
    except FileNotFoundError:
        print("Error: parcels.csv file not found in data directory")
        raise
    except Exception as e:
        print(f"Error importing parcels: {str(e)}")
        raise

def update_status(query_time):
    """
    Updates delivery status of all parcels based on current time.
    Time Complexity: O(n)

    Args:
        query_time: Current time or user-specified query time
    """
    for i in range(1, 41):
        try:
            parcel = delivery_registry.locate_parcel(i)
            if parcel and hasattr(parcel, 'start_time') and parcel.start_time:
                if query_time < parcel.start_time.time():
                    parcel.status = "at hub"
                elif parcel.start_time.time() <= query_time < parcel.delivery_time.time():
                    parcel.status = "in transit"
                elif query_time >= parcel.delivery_time.time():
                    parcel.status = "delivered"
            else:
                print(f"Warning: Invalid parcel data for ID {i}")
        except LookupError as e:
            print(f"Parcel with ID {i} not found: {str(e)}")
        except Exception as e:
            print(f"Error processing parcel {i}: {str(e)}")
