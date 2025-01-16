"""
WGUPS (Western Governors University Parcel Service) user interface module.
Provides command-line interface for checking delivery status and progress.
"""

import datetime
import sys
import locations
import parcels
import trucks


def main_menu():
    """Display main menu and handle user input for time selection."""
    while True:
        print(
            '\033[1;36;40m------------------------------------------------\n'
            '          WGUPS Daily Delivery Tracker\n'
            '------------------------------------------------\n\n'
            '\033[1;36;40mSelect Time Option:\n'
            '\033[0;37;40m1: Current Time Status\n'
            '2: Custom Time Status\n'
        )

        choice = input('\033[0;36;40mEnter selection (1-2): ')
        if choice == '1':
            current_time_menu()
            break
        elif choice == '2':
            custom_time_menu()
            break
        else:
            print('\n\033[0;31;40mError: Please enter 1 or 2\n')


def current_time_menu():
    """Display menu for current time status updates."""
    current_time = datetime.datetime.now().time()

    while True:
        print(
            f'\033[1;36;40m\nCurrent Time: {current_time.strftime("%I:%M %p")}\n\n'
            '\033[0;37;40mSelect Report Type:\n'
            '1: All Parcels Status\n'
            '2: Single Parcel Lookup\n'
            '3: Truck Status Summary\n'
            '4: Exit Program\n'
        )

        choice = input('\033[0;36;40mEnter selection (1-4): ')
        if choice == '1':
            display_all_parcels(current_time)
        elif choice == '2':
            lookup_single_parcel(current_time)
        elif choice == '3':
            display_truck_status(current_time)
        elif choice == '4':
            print('\nThank you for using WGUPS Daily Delivery Tracker\n')
            sys.exit()
        else:
            print('\n\033[0;31;40mError: Please enter a number 1-4\n')


def custom_time_menu():
    """Handle custom time input and display appropriate menu."""
    while True:
        try:
            time_input = input('\n\033[1;35;40mEnter time (HH:MM AM/PM): ')
            query_time = datetime.datetime.strptime(time_input, '%I:%M %p').time()
            break
        except ValueError:
            print('\n\033[0;31;40mError: Use format "HH:MM AM/PM" (e.g., "10:30 AM")\n')
            continue

    while True:
        print(
            f'\n\033[0;35;40mSelected Time: {query_time.strftime("%I:%M %p")}\n\n'
            '\033[1;36;40mSelect Report Type:\n'
            '\033[0;36;40m1: All Parcels Status\n'
            '2: Single Parcel Lookup\n'
            '3: Truck Status Summary\n'
            '4: Exit Program\n'
        )

        choice = input('\033[0;36;40mEnter selection (1-4): ')
        if choice == '1':
            display_all_parcels(query_time)
        elif choice == '2':
            lookup_single_parcel(query_time)
        elif choice == '3':
            display_truck_status(query_time)
        elif choice == '4':
            print('\nThank you for using WGUPS Daily Delivery Tracker\n')
            sys.exit()
        else:
            print('\n\033[0;31;40mError: Please enter a number 1-4\n')


def display_all_parcels(query_time):
    """Display status of all parcels at specified time."""
    parcels.update_parcel_status(query_time)

    print('\n\033[1;36;40m{:=^120}'.format(' WGUPS PARCEL STATUS REPORT '))
    print('\033[0;36;40m{:^120}'.format(f'Status as of {query_time.strftime("%I:%M %p")}'))
    print('\033[1;36;40m{:=^120}\n'.format(''))
    
    print('\033[0;37;40mNote: Projected delivery times shown with "~" for undelivered parcels\n')
    
    # Header row
    print('\033[1;36;40m{:<5} {:<35} {:<12} {:<25} {:<12} {:<8} {:<15}'
          .format('ID', 'Address', 'Deadline', 'Notes', 'Status', 'Truck', 'Delivery'))

    # Parcel data rows
    for i in range(1, 41):
        p = parcels.wgups_parcels.lookup(i)
        delivery_time = p.delivery_time.time()
        delivery_info = ''
        
        if query_time < delivery_time:
            delivery_info = f'~{delivery_time.strftime("%I:%M %p")}'
        else:
            delivery_info = f'{delivery_time.strftime("%I:%M %p")}'

        print('\033[0;36;40m{:<5} {:<35} {:<12} {:<25} {:<12} {:<8} {:<15}'
              .format(
                  p.parcel_id,
                  p.address[:32],
                  p.deadline.time().strftime('%I:%M %p'),
                  p.notes[:22],
                  p.status,
                  p.truck,
                  delivery_info
              ))

    _handle_next_action()


def lookup_single_parcel(query_time):
    """Look up and display status of a single parcel."""
    parcels.update_parcel_status(query_time)

    while True:
        try:
            parcel_id = int(input('\033[1;36;40mEnter Parcel ID number: '))
            if parcel_id not in range(1, 41):
                raise ValueError
            break
        except ValueError:
            print('\033[0;31;40mError: Please enter a valid Parcel ID (1-40)')
            continue

    parcel = parcels.wgups_parcels.lookup(parcel_id)
    
    print('\n\033[1;36;40m{:=^60}'.format(' PARCEL DETAILS '))
    print('\033[0;36;40m{:^60}'.format(f'Status as of {query_time.strftime("%I:%M %p")}'))
    print('\033[1;36;40m{:=^60}'.format(''))
    
    print(f'\n\033[0;36;40mParcel ID: {parcel.parcel_id}')
    print(f'Address: {parcel.address}')
    print(f'City: {parcel.city}')
    print(f'State: {parcel.state}')
    print(f'ZIP: {parcel.zip_code}')
    print(f'Weight: {parcel.weight} kg')
    print(f'Deadline: {parcel.deadline.time().strftime("%I:%M %p")}')
    print(f'Status: {parcel.status}')
    print(f'Truck: {parcel.truck}')
    
    if query_time < parcel.delivery_time.time():
        print(f'Expected Delivery: {parcel.delivery_time.time().strftime("%I:%M %p")}')
    else:
        print(f'Delivered At: {parcel.delivery_time.time().strftime("%I:%M %p")}')

    distance_matrix = locations.load_distance_data()
    total_miles = _calculate_total_miles(query_time, distance_matrix)
    print(f'\nTotal Fleet Mileage: {round(total_miles, 1)} miles\n')

    _handle_next_action()


def display_truck_status(query_time):
    """Display status summary for all trucks."""
    distance_matrix = locations.load_distance_data()
    location_list = locations.load_location_data()
    
    print('\n\033[1;36;40m{:=^100}'.format(' TRUCK STATUS SUMMARY '))
    print('\033[0;36;40m{:^100}'.format(f'Status as of {query_time.strftime("%I:%M %p")}'))
    print('\033[1;36;40m{:=^100}\n')

    total_miles = 0.0
    
    for truck in trucks.delivery_trucks:
        print(f'\033[1;36;40m{"=" * 20} TRUCK {truck.id} {"=" * 20}')
        print('\033[0;34;40mOperational Details:')
        print(f'\033[0;37;40mDeparture Time: {truck.departure_time.time().strftime("%I:%M %p")}')
        print(f'Driver: {truck.driver}')
        
        # Get parcel IDs assigned to this truck
        parcel_ids = sorted([str(p.parcel_id) for p in truck.parcels])
        print(f'Assigned Parcels: {", ".join(parcel_ids)}')
        
        # Calculate current progress
        location_idx, miles = trucks.calculate_route_progress(query_time, truck, distance_matrix)
        print('\n\033[0;34;40mCurrent Status:')
        print(f'\033[0;37;40mCurrent Location: {location_list[location_idx]}')
        print(f'Miles Traveled: {round(miles, 1)}')
        
        if location_idx == truck.route[-1]:
            print('\033[0;35;40mRoute Completed')
            
        print()
        total_miles += miles

    print(f'\033[1;34;40mTotal Fleet Mileage: {round(total_miles, 1)} miles\n')
    
    _handle_next_action()


def _calculate_total_miles(query_time, distance_matrix):
    """Calculate total miles traveled by all trucks."""
    total = 0.0
    for truck in trucks.delivery_trucks:
        _, miles = trucks.calculate_route_progress(query_time, truck, distance_matrix)
        total += miles
    return total


def _handle_next_action():
    """Handle user choice to return to menu or exit."""
    choice = input('\n\033[1;37;40mEnter 0 for main menu, any other key to exit: ')
    if choice == '0':
        main_menu()
    else:
        print('\nThank you for using WGUPS Daily Delivery Tracker\n')
        sys.exit()
