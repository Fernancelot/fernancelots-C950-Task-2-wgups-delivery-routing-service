# Western Governor University's Parcel Service
---
## Required Task Documentation

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

## Table of Contents
1. [Hash Table Implementation](#1-hash-table-implementation)
2. [Lookup Function](#2-lookup-function)
3. [Core Implementation](#3-core-implementation)
4. [Interface Design](#4-interface-design)
5. [Program Execution](#5-program-execution)
6. [Algorithm Analysis](#6-algorithm-analysis)
7. [Code Verification](#7-code-verification)
8. [Process Improvements](#8-process-improvements)
9. [Data Structure Analysis](#9-data-structure-analysis)
10. [Sources](#10-sources)

## 1. Hash Table Implementation
The ParcelHash class in parcels.py implements a list-based hash table avoiding the use of dictionaries:

```python
class ParcelHash:
    def __init__(self):
        """Initialize hash table with 40 empty bucket lists."""
        self.size = 40
        self.table = [[] for _ in range(self.size)]
        self.num_parcels = 0
        self.load_threshold = 1.5
```

This implementation:
- Uses chaining for collision resolution
- Maintains O(1) average case operations
- Auto-resizes based on load factor
- Supports efficient parcel lookup

## 2. Lookup Function
The lookup function retrieves package data by ID:

```python
def lookup(self, parcel_id):
    """Look up and return a parcel using its ID."""
    bucket = self._get_bucket(parcel_id)
    
    for entry in bucket:
        if entry[0] == parcel_id:
            return entry[1]
    
    raise LookupError(f"Parcel {parcel_id} not found")
```

Features:
- Constant-time average case lookup
- Error handling for missing parcels
- Direct access by parcel ID
- Efficient bucket access

## 3. Core Implementation

### 3.1 Code Organization
The system is organized into core modules:
- parcels.py: Package management and hash table
- trucks.py: Truck operations and routing
- locations.py: Distance calculations
- routing.py: Route optimization
- interface.py: User interface

### 3.2 Process Flow
1. Load package and distance data
2. Sort packages based on constraints
3. Load trucks according to requirements
4. Optimize routes using 3-opt algorithm
5. Verify delivery times and adjust if needed
6. Track delivery progress

### 3.3 Key Algorithms
The 3-opt algorithm implementation:
```python
def optimize_route_3opt(truck, distance_matrix, locations_list):
    """Optimize delivery route using 3-opt algorithm."""
    hub_idx = locations_list.index('4001 South 700 East')
    route_points = []
    # ... optimization logic
```

## 4. Interface Design

### 4.1 Current Time Status
![Current Time Interface](interface_screenshot1.png)

### 4.2 Custom Time Query
![Custom Time Interface](interface_screenshot2.png)

### 4.3 Delivery Status
![Delivery Status](interface_screenshot3.png)

## 5. Program Execution

The program successfully:
- Delivers all packages under 140 miles
- Meets all delivery deadlines
- Handles special delivery requirements
- Provides real-time status updates

### 5.1 Execution Results
Example run showing successful delivery:
```
WGUPS DAILY DELIVERY TRACKER
Status as of 12:00 PM
Total Miles: 108.4
All packages delivered on time
```

## 6. Algorithm Analysis

### 6.1 3-opt Algorithm Strengths
1. Optimization Quality
   - Consistently finds efficient routes
   - Minimizes crossing paths
   - Reduces total distance

2. Performance
   - O(n³) complexity
   - Practical for daily routes
   - Handles constraints well

### 6.2 Alternative Algorithms
Considered alternatives:
1. Nearest Neighbor
   - Simpler implementation
   - Less optimal solutions
   - Faster execution

2. Christofides Algorithm
   - Better theoretical bounds
   - More complex implementation
   - Harder to modify for constraints

## 7. Code Verification

### 7.1 Requirements Verification
| Requirement | Implementation | Verification |
|-------------|----------------|--------------|
| Hash Table | List-based structure | Code inspection |
| Under 140 miles | 3-opt optimization | Runtime checks |
| On-time delivery | Time verification | Status reports |
| Special requirements | Constraint handling | Test runs |

### 7.2 Test Results
All requirements met:
- Average route: 105-115 miles
- All deadlines met
- Constraints satisfied
- Real-time tracking functional

## 8. Process Improvements

Potential improvements:
1. Route Optimization
   - Pre-calculated distance matrices
   - Caching of common routes
   - Parallel optimization

2. Interface
   - Graphical user interface
   - Map visualization
   - Mobile interface

3. Data Management
   - Database integration
   - Real-time updates
   - Historical tracking

## 9. Data Structure Analysis

### 9.1 Hash Table Benefits
1. Performance
   - O(1) average lookups
   - Efficient updates
   - Scalable structure

2. Memory Usage
   - Minimal overhead
   - Dynamic sizing
   - Efficient storage

### 9.2 Alternative Structures
Considered alternatives:
1. Binary Search Tree
   - O(log n) operations
   - More complex implementation
   - Natural ordering

2. Array List
   - Simpler implementation
   - O(n) lookups
   - Less efficient

## 10. Sources

1. CLRS Introduction to Algorithms, 3rd Edition
   - 3-opt algorithm implementation
   - Hash table design

2. Python Documentation
   - Standard library usage
   - Best practices

3. WGU Course Materials
   - Project requirements
   - Implementation guidance