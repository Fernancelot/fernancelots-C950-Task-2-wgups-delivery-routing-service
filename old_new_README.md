# WGUPS Route Optimization System

## Project Overview
The WGUPS (Western Governors University Parcel Service) Route Optimization System is a Python implementation that solves a variant of the Vehicle Routing Problem (VRP) with time windows and special delivery constraints. The system optimizes delivery routes for a fleet of three trucks and two drivers to efficiently deliver 40 packages while adhering to specific timing and delivery requirements.

### Key Features
- Custom hash table implementation for efficient package management
- 3-opt algorithm for route optimization
- Real-time status tracking and reporting
- Handling of special delivery constraints and time windows
- Command-line interface for monitoring deliveries

## Requirements
- Python 3.13.1 or higher
- No external libraries required (uses only Python standard library)

## Project Structure
```
wgups-routing/
├── data/
│   ├── distances.csv    # Distance matrix between locations
│   └── parcels.csv      # Parcel delivery information
├── src/
│   ├── core/
│   │   ├── routing.py   # Route optimization implementation
│   │   ├── locations.py # Location and distance management
│   │   ├── parcels.py   # Parcel management and hash table
│   │   └── trucks.py    # Truck and driver management
│   └── ui/
│       └── interface.py  # User interface implementation
└── main.py              # Program entry point
```

## Core Components

### Hash Table Implementation
- Custom implementation using chaining for collision resolution
- Dynamically resizes based on load factor
- O(1) average case lookup and insertion

### Route Optimization
- Uses 3-opt algorithm for route improvement
- Handles multiple delivery constraints:
  - Package grouping requirements
  - Truck-specific assignments
  - Delayed departure times
  - Address corrections
- Maintains total route distance under 140 miles

### Status Tracking
- Real-time delivery status monitoring
- Package location tracking
- Delivery time projections
- Cumulative mileage reporting

## Usage
1. Run the program:
   ```bash
   python main.py
   ```

2. Select time option:
   - Current time status
   - Custom time lookup

3. Choose report type:
   - All parcels status
   - Single parcel lookup
   - Truck status summary

## Delivery Constraints
- Maximum 16 packages per truck
- Trucks travel at 18 mph
- Delivery hours: 8:00 AM - 5:00 PM
- Special handling requirements:
  - Grouped deliveries
  - Delayed departures
  - Truck-specific assignments
  - Address corrections

## Implementation Details

### Data Structures
- **Hash Table**: Custom implementation for O(1) package lookups
- **Route Lists**: Dynamic route storage and optimization
- **Location Matrix**: Efficient distance calculations

### Algorithms
- **3-opt**: Route optimization with O(n³) complexity
- **Greedy Initial Sort**: Package assignment optimization
- **Dynamic Route Adjustment**: Handles delivery constraints

### Performance
- Average route completion: 11:45 AM - 2:45 PM
- Total mileage: 85-127 miles (varies by optimization run)
- All deadline constraints met
- O(n³) worst-case time complexity

## Testing and Verification
- All packages delivered within deadlines
- Total mileage consistently under 140 miles
- Special delivery constraints verified
- Status checking validated at multiple time points

## License
This project is part of the WGU Computer Science curriculum.
