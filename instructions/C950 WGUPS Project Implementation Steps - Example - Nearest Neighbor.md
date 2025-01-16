# Task 2 - Project Implementation Steps - Example: Nearest Neighbor

---

## C950 WGUPS Project - Implementation Steps

*Note: This is an example implementation using the Nearest Neighbor Greedy Algorithm.*

Feel free to cite this document, but it is highly recommended to develop your own approach.

---

### A) Package Data Steps:

1. Create a HashTable data structure (refer to *C950 - Webinar-1: Let’s Go Hashing*).
2. Create `Package` and `Truck` objects and prepare the following files:
   - `packages.csv`
   - `distance.csv`
   - `addresses.csv`
3. Define `loadPackageData(HashTable)` to:
   - Read packages from `packages.csv` (refer to *C950 - Webinar-2: Getting Greedy*).
   - Update the `Package` object.
   - Insert the `Package` object into the HashTable with `key=PackageID` and `item=Package`.

---

### B) Distance Data Steps:

#### B.1) Upload Distances:

4. Create a `distanceData` list.
5. Define `loadDistanceData(distanceData)` to:
   - Read the `distance.csv` file row by row.
   - Append each row to `distanceData` (two-dimensional list). Refer to *C950 WGUPS Distance Table Matrix*.

#### B.2) Upload Addresses:

6. Create an `addressData` list.
7. Define `loadAddressData(addressData)` to:
   - Read only addresses from the `addresses.csv` file.
   - Append addresses to `addressData`.

---

### C) Algorithm to Load Packages:

#### C.1) Function to Return Distance Between Two Addresses:

8. Define `distanceBetween(address1, address2)`.
9. Return `distanceData[addressData.index(address1)][addressData.index(address2)]`.
   - *Example*: Distances between addresses can be accessed via `distanceData[i][j]`.

#### C.2) Function to Find Minimum Distance/Address:

10. Define `minDistanceFrom(fromAddress, truckPackages)`.
11. Return the minimum distance address to `fromAddress` by calling `distanceBetween(address1, address2)` in a loop for all addresses in the truck.

#### C.3) Function to Load Packages into Trucks:

12. Define `truckLoadPackages()`.
13. Load trucks based on provided assumptions (e.g., Truck-2 must have certain packages, some packages must go together, some packages are delayed, etc.).
14. Load packages and addresses manually/heuristically or loop through package addresses and call `minDistanceFrom(fromAddress, truckPackages)` for all unvisited addresses in the truck until each truck holds 16 packages.

---

### D) Algorithm to Deliver Packages:

#### D.1) Function to Deliver Packages in a Truck:

15. Define `truckDeliverPackages(truck)`.
16. Loop through truck package addresses and call `minDistanceFrom(fromAddress, truckPackages)` for all unvisited addresses.

#### D.2) Keep Track of Miles and Delivery Times:

17. Update delivery status and delivery time in the HashTable for each delivered package and maintain total mileage and delivery times.
   - *Time Calculation*: `timeToDeliver(h) = distance(miles) / 18 (mph)` (assuming average truck speed is 18 mph).
   - Use `datetime.timedelta` to accumulate time:
     ```python
     time_obj = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
     ```

---

### E) UI to Interact with the Users:

18. Create a UI to interact and report results based on requirements.

#### Possible Menu Options:

```
1. Print All Package Status and Total Mileage
2. Get a Single Package Status with a Time
3. Get All Package Status with a Time
4. Exit the Program
```

#### Example Output:

```
PackageID | Address              | City             | State | Zip   | Delivery Deadline | Mass KILO | Special Notes      | Status             | DeliveryTime
-----------------------------------------------------------------------------------------------------------
1         | 195 W Oakland Ave   | Salt Lake City   | UT    | 84115 | 10:30 AM          | 21        |                   | Delivered by Truck-2 | 08:46:20
2         | 2530 S 500 E        | Salt Lake City   | UT    | 84106 | EOD               | 44        |                   | At Hub             |
3         | 233 Canyon Rd       | Salt Lake City   | UT    | 84103 | EOD               | 2         | Can only be on Truck 2 | In Route by Truck-2 |
...
```

---

*C950 WGUPS Project - Implementation Steps - End*

