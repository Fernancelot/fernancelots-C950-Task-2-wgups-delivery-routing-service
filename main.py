"""
WGUPS (Western Governors University Parcel Service) main entry point.
# Western Governor University's Parcel Service
---
Task 2 : Implementation Phase of the WGUPS Routing Program
Christopher D Powell
[...]
Student ID 001307071
WGU Email: cpow181@wgu.edu
Completed in the Year of 2025, in the month of 1, upon the 15th day
C950 Data Structures and Algorithms II - Task 2
Course Version NHP3
Python Version: 3.13.1
IDE: PyCharm 2024.1.4 (Professional Edition)
Build #PY-241.18034.82
---
This program implements a delivery route optimization system that:
- Handles 40 packages with specific delivery requirements
- Utilizes 3 trucks and 2 drivers
- Maintains total mileage under 140
- Provides real-time status checking
- Uses a self-adjusting algorithm for route optimization

Running this program:
1. Ensures you are in the root directory /fernancelots-wgups-delivery-routing-service
2. Run with: python main.py
3. Follow interface prompts for status checks

Time Complexity:
- Overall program: O(n³) due to 3-opt algorithm
- Hash table operations: O(1) average case
- Status checking: O(n) where n is number of packages
"""

from src.core.routing import initialize_routes
from src.ui.interface import main_menu

def main():
    """
    Main function to initialize routes and display the main menu.
    Time Complexity: O(n³) for route initialization
    """
    initialize_routes.initialize_routes()
    main_menu()

if __name__ == "__main__":
    main()