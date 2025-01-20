'''
# main.py
# created by Christopher Powell
# Student #001307071
'''

import parcels
import routing
from cli_interface import launch_welcome

def main():
    """
    Entry point for the Delivery Management System.
    Initializes delivery coordination and launches user interface.
    """
    # Load package data
    parcels.import_parcels()

    # Initialize delivery routes and vehicle assignments
    total_mileage = routing.coordinate_deliveries()  # Return total mileage but don't print it yet

    # Launch the interactive monitoring interface
    launch_welcome()

if __name__ == "__main__":
    main()
