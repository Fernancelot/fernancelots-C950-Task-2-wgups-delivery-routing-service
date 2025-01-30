'''
main.py
Created by Christopher Powell
Student #001307071
'''

import parcels
import routing
from cli_interface import launch_welcome

def main():
    """
    Entry point for the WGUPS Delivery Management System.
    Initializes delivery coordination and launches user interface.
    Time Complexity: O(n³) where n is number of delivery points
    """
    try:
        # Load package data and initialize registry
        # print("Initializing package data...")
        parcels.import_parcels()

        # Coordinate deliveries and optimize routes
        # print("Optimizing delivery routes...")
        total_mileage = routing.coordinate_deliveries()

        # Launch interactive interface
        # print("Starting user interface...")
        launch_welcome()

    except Exception as e:
        print(f"\nError initializing delivery system: {str(e)}")
        print("Please ensure all data files are present in the /data directory and try again.")
        exit(1)

if __name__ == "__main__":
    main()
