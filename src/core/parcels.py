"""
WGUPS (Western Governors University Parcel Service) parcel management module.
Implements parcel storage and lookup using a list-based hash table implementation.
"""
import datetime
import csv


class ParcelHash:
    """
    A hash table implementation using lists for storing parcel data.
    Uses chaining to handle collisions.
    """
    def __init__(self):
        """Initialize hash table with 40 empty bucket lists."""
        self.size = 40
        self.table = [[] for _ in range(self.size)]
        self.num_parcels = 0
        self.load_threshold = 1.5

    def _get_bucket(self, parcel_id):
        """Get the appropriate bucket for a parcel ID."""
        bucket_idx = hash(parcel_id) % self.size
        return self.table[bucket_idx]

    def insert(self, parcel_id, parcel_data):
        """
        Insert or update a parcel in the hash table using the parcel ID as key.
        Returns True if successful.
        """
        bucket = self._get_bucket(parcel_id)
        parcel_entry = [parcel_id, parcel_data]

        # Check if parcel already exists
        for entry in bucket:
            if entry[0] == parcel_id:
                entry[1] = parcel_data
                return True

        # Add new parcel
        bucket.append(parcel_entry)
        self.num_parcels += 1

        # Check if resize needed
        if self.num_parcels / self.size > self.load_threshold:
            self._resize_table()

        return True

    def lookup(self, parcel_id):
        """Look up and return a parcel using its ID."""
        bucket = self._get_bucket(parcel_id)

        for entry in bucket:
            if entry[0] == parcel_id:
                return entry[1]

        raise LookupError(f"Parcel {parcel_id} not found")

    def _resize_table(self):
        """
        Double table size and rehash all entries when load factor exceeded.
        """
        # Save current entries
        old_entries = []
        for bucket in self.table:
            for entry in bucket:
                old_entries.append(entry)

        # Reset table with double size
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.num_parcels = 0

        # Reinsert all entries
        for parcel_id, parcel_data in old_entries:
            self.insert(parcel_id, parcel_data)


class Parcel:
    """Class representing a delivery parcel and its attributes."""

    def __init__(self, parcel_id, address, city, state, zip_code, deadline, weight, notes, truck=None):
        """Initialize parcel with provided attributes."""
        self.parcel_id = parcel_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = "at hub"
        self.dispatch_time = datetime.datetime.strptime("00:00", '%H:%M')
        self.delivery_time = datetime.datetime.strptime("00:00", '%H:%M')
        self.truck = truck

    def __str__(self):
        """Return string representation of parcel."""
        return (f"{self.parcel_id}, {self.address}, {self.city}, {self.state}, {self.zip_code}, "
                f"{self.weight}, {self.deadline}, {self.notes}, {self.status}, {self.delivery_time}")


# Global hash table instance for all parcels
wgups_parcels = ParcelHash()


def read_parcels():
    """
    Read parcel data from CSV and sort into truck loads based on delivery constraints.
    Returns dictionary of truck loads containing parcel IDs.
    """
    grouped_parcels = set()  # Parcels that must be delivered together
    truck_loads = {1: [], 2: [], 3: []}  # Parcels assigned to each truck
    unassigned = []  # Parcels pending assignment
    assigned = []    # Parcels already assigned

    EOD = datetime.datetime.strptime("16:59:59", '%H:%M:%S')

    with open('data/parcels.csv') as parcel_file:
        csv_reader = csv.reader(parcel_file, delimiter=',')
        next(csv_reader)  # Skip header

        # Create parcels from CSV data
        for row in csv_reader:
            parcel_id = int(row[0])
            deadline = (datetime.datetime.strptime(row[5], '%H:%M %p')
                       if row[5][0].isnumeric() else EOD)

            # Create parcel object
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

            # Add to hash table and sort list
            wgups_parcels.insert(parcel_id, parcel)
            unassigned.append(parcel)

        # Sort by deadline
        unassigned.sort(key=lambda p: p.deadline)
        working_list = unassigned.copy()

        # First pass: Handle special delivery requirements
        for parcel in unassigned:
            if not parcel.notes:
                continue

            # Handle truck-specific assignments
            if 'on truck' in parcel.notes:
                truck_num = int(parcel.notes.split()[-1])
                truck_loads[truck_num].append(parcel.parcel_id)
                assigned.append(parcel)
                continue

            # Handle wrong address case
            if 'Wrong address' in parcel.notes:
                truck_loads[3].append(parcel.parcel_id)
                assigned.append(parcel)
                continue

            # Handle grouped deliveries
            if 'delivered with' in parcel.notes:
                pointer = parcel.notes.find('with') + 5
                group = parcel.notes[pointer:].split(', ')
                grouped_parcels.add(parcel.parcel_id)
                assigned.append(parcel)

                if parcel.parcel_id not in truck_loads[1]:
                    truck_loads[1].append(parcel.parcel_id)
                    for group_id in group:
                        group_id = int(group_id)
                        grouped_parcels.add(group_id)
                        for p in working_list:
                            if p.parcel_id == group_id and p.parcel_id not in truck_loads[1]:
                                truck_loads[1].append(p.parcel_id)
                                assigned.append(p)

            # Handle delayed parcels
            if 'Delayed' in parcel.notes:
                arrival = _parse_arrival_time(parcel.notes)

                if arrival.hour < 9:
                    truck_loads[1].append(parcel.parcel_id)
                elif arrival.hour < 10 or (arrival.hour == 10 and arrival.minute < 20):
                    truck_loads[2].append(parcel.parcel_id)
                else:
                    truck_loads[3].append(parcel.parcel_id)

                assigned.append(parcel)
                continue

        # Remove assigned parcels from working list
        for parcel in assigned:
            if parcel in working_list:
                working_list.remove(parcel)

        # Get delivery locations for each truck
        truck_locations = _get_truck_locations(truck_loads)

        # Second pass: Assign by deadline and location
        _assign_remaining_parcels(working_list, truck_loads, truck_locations)

        return truck_loads


def update_parcel_status(query_time):
    """Update status of all parcels based on query time."""
    for i in range(1, 41):
        parcel = wgups_parcels.lookup(i)

        if query_time < parcel.dispatch_time.time():
            parcel.status = "at hub"
        elif parcel.dispatch_time.time() <= query_time < parcel.delivery_time.time():
            parcel.status = "en route"
        else:
            parcel.status = "delivered"


def _parse_arrival_time(notes):
    """Extract arrival time from notes string."""
    for part in notes.split():
        if part[0].isnumeric():
            return datetime.datetime.strptime(part, '%H:%M')


def _get_truck_locations(truck_loads):
    """Get set of delivery locations for each truck."""
    locations = {1: set(), 2: set(), 3: set()}

    for truck_id, load in truck_loads.items():
        for parcel_id in load:
            parcel = wgups_parcels.lookup(parcel_id)
            locations[truck_id].add(parcel.address)
            locations[truck_id].add(parcel.zip_code)

    return locations


def _assign_remaining_parcels(parcels, truck_loads, truck_locations):
    """Assign remaining parcels to trucks based on location and capacity."""
    # First assign by matching locations
    for parcel in parcels[:]:  # Use slice to allow removal during iteration
        if parcel.deadline != datetime.datetime.strptime("16:59:59", '%H:%M:%S'):
            for truck_id, locations in truck_locations.items():
                if len(truck_loads[truck_id]) < 16:
                    if (parcel.address in locations or
                        parcel.zip_code in locations):
                        truck_loads[truck_id].append(parcel.parcel_id)
                        parcels.remove(parcel)
                        break

    # Assign any remaining parcels to least loaded truck
    while parcels:
        parcel = parcels[0]

        # Find truck with smallest load
        available_truck = min(truck_loads.items(),
                            key=lambda x: len(x[1]))[0]

        if len(truck_loads[available_truck]) >= 16:
            raise ValueError("Unable to assign all parcels - trucks at capacity")

        truck_loads[available_truck].append(parcel.parcel_id)
        parcels.remove(parcel)