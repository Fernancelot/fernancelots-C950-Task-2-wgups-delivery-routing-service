# Western Governor University's Parcel Service
---
## WGUPS Time Complexity Analysis

[ Task 2 : Implementation Phase of the WGUPS Routing Program ]

Christopher D Powell ( ~Commonly referred to by code-name designation: _Fernancelot_ )
Student ID 001307071  
WGU Email: cpow181@wgu.edu
  ( Completed in the Year of 2025, in the month of 1, upon the 15th day )
C950 Data Structures and Algorithms II - Task 2  
Course Version NHP3  
Python Version: 3.13.1  
IDE: PyCharm 2024.1.4 (Professional Edition)  
Build #PY-241.18034.82

---


# Time Complexity Analysis

## Core Components

### Hash Table Operations (parcels.py)
- Insert: O(1) average case, O(n) worst case
- Lookup: O(1) average case, O(n) worst case
- Resize: O(n) where n is number of parcels
- Space Complexity: O(n)

### Route Optimization (routing.py)
- 3-opt Algorithm: O(n³) where n is number of delivery locations
- Route Verification: O(n) per route
- Package Swapping: O(n²) in worst case
- Space Complexity: O(n) for route storage

### Location Management (locations.py)
- Load Distance Data: O(n²) where n is number of locations
- Calculate Route Distance: O(n) where n is route length
- Calculate Segment Distance: O(1)
- Space Complexity: O(n²) for distance matrix

### Truck Operations (trucks.py)
- Load Trucks: O(n) where n is number of packages
- Route Progress Calculation: O(n) where n is route length
- Space Complexity: O(n) per truck

### Interface Operations (interface.py)
- Status Updates: O(n) where n is number of packages
- Display Operations: O(1)
- Space Complexity: O(1)

## Critical Paths

### Package Loading Process
1. Hash Table Creation: O(n)
2. Initial Sort: O(n log n)
3. Load Assignment: O(n)
Total: O(n log n)

### Route Optimization Process
1. Address Mapping: O(n)
2. 3-opt Algorithm: O(n³)
3. Verification: O(n)
Total: O(n³)

### Delivery Execution
1. Route Following: O(n)
2. Status Updates: O(n)
3. Progress Tracking: O(n)
Total: O(n)

## Space Complexity Summary
- Hash Table: O(n)
- Distance Matrix: O(n²)
- Route Storage: O(n)
- Total: O(n²)

## Performance Considerations
1. Hash Table Implementation
   - Chaining for collision resolution
   - Load factor management

2. Route Optimization
   - 3-opt local search
   - Early termination conditions
   - Constraint validation

3. Memory Management
   - Efficient data structures
   - Minimal redundancy
   - Clear cleanup paths