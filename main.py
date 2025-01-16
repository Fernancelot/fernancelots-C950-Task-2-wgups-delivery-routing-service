"""
WGUPS (Western Governors University Parcel Service) main entry point.
Student ID: XXXXXXXX
"""

import routing
from interface import main_menu


def main():
    """Initialize delivery routes and start user interface."""
    # Initialize optimal routes
    routing.initialize_routes()
    
    # Start user interface
    main_menu()


if __name__ == "__main__":
    main()