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

## Project Overview

The Western Governors University Parcel Service (WGUPS) Routing System is a Python application that optimizes daily local deliveries in Salt Lake City downtown area. The system handles:

- Route optimization for 3 delivery trucks
- Management of 40 packages with specific delivery requirements
- Real-time status tracking and reporting
- Delivery constraint compliance
- Total mileage optimization (under 140 miles)

## Core Features

- Custom hash table implementation for package management
- 3-opt algorithm for route optimization
- Status checking interface for real-time updates
- Time-based delivery tracking
- Delivery constraint management

## Project Structure

```
Fernancelots WGUPS - Routing Service/
├── data/
│   ├── distances.csv     # Location distances
│   └── parcels.csv      # Package information
├── src/
│   ├── core/
│   │   ├── routing.py   # Route optimization
│   │   ├── locations.py # Distance calculations
│   │   ├── parcels.py   # Package management
│   │   └── trucks.py    # Truck operations
│   └── ui/
│       └── interface.py  # User interface
└── main.py              # Application entry point
```

## Key Requirements

### Delivery Constraints
- Maximum 16 packages per truck
- Two drivers available
- Three trucks total
- 18 mph constant speed
- Hub-only loading
- No departures before 8:00 AM

### Special Package Requirements
- Package #9 address correction at 10:20 AM
- Packages #13, #14, #15, #16, #19, #20 must be delivered together
- Packages #3, #18, #36, #38 must be on truck 2
- Packages #6, #25, #28, #32 delayed until 9:05 AM

## Running the Application

1. Ensure Python 3.12+ is installed
2. Verify CSV files are in data/ directory
3. Run: `python main.py`
4. Follow interface prompts for:
   - Time selection (current/custom)
   - Report type selection
   - Package status queries

## Features

### Route Optimization
- 3-opt algorithm implementation
- Distance minimization
- Constraint satisfaction
- Deadline adherence

### Status Tracking
- Real-time package status
- Location tracking
- Delivery projections
- Total mileage monitoring

### User Interface
- Time-based queries
- Package status lookup
- Truck status reports
- Delivery projections