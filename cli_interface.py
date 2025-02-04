import datetime
import sys
import locations
import parcels
import van
import shutil

# get the terminal size
terminal_width = shutil.get_terminal_size().columns

def handle_special_case_for_parcel_9(query_time=None):
    """
    Handles special status update for parcel 9 based on current or queried time.
    Time Complexity: O(1)
    """
    try:
        package_9 = parcels.delivery_registry.locate_parcel(9)
        if package_9:
            # Define time constraints
            time_0800 = datetime.datetime.strptime("08:20", "%H:%M").time()
            time_1020 = datetime.datetime.strptime("10:20", "%H:%M").time()
            time_1700 = datetime.datetime.strptime("17:00", "%H:%M").time()

            # Use current time if query_time is not provided
            current_time = query_time if query_time else datetime.datetime.now().time()

            # Update address based on time constraints
            if time_0800 <= current_time < time_1020:
                package_9.destination = "300 State St"
                package_9.dest_zip = "84103"
            elif time_1020 <= current_time:
                package_9.destination = "410 S State St"
                package_9.dest_zip = "84111"

    except LookupError:
        pass  # Package 9 not found

def format_package_info(package, query_time=None):
    """
    Formats package information into a consistent string display with table-like formatting.
    Time Complexity: O(1)
    """
    # Initialize delivery prediction time based on van assignment
    predicted_time = "🦉"
    if hasattr(package, 'delivery_time'):
        predicted_time += f" {package.delivery_time.strftime('%I:%M %p')}"

    # Determine status
    status = "at hub"
    van = f"VAN: {str(package.assigned_vehicle)}" if package.assigned_vehicle else ""

    if query_time:
        if package.start_time and query_time < package.start_time.time():
            status = "at hub"
        elif package.delivery_time and query_time >= package.delivery_time.time():
            status = "delivered"
            predicted_time = f"{package.delivery_time.strftime('%I:%M %p')}"
        else:
            status = "en route"

    # Format deadline for display
    deadline = (f"{package.deadline.strftime('%I:%M %p')}") if isinstance(package.deadline, datetime.datetime) else "04:59 PM"

    # Slice the 'destination' string to 25 characters
    destination_display = package.destination[:25]

    # Split the 'special_instructions' string at '---' and select the first part
    special_instructions = package.special_instructions.split('---')[0]

    # Fixed width formatting for clean table display
    return f"{str(package.tracking_id):<5} {destination_display:<30} {deadline:<20} {special_instructions:<35} {status:<15} {van:<10} {predicted_time:<20}"


def launch_welcome():
    """
    Displays the ASCII welcome screen and transitions to the main menu.
     Time Complexity: O(1)
    """
    print("\033[34;94m" + """
             ,╓▄▄▄▄▄▄▄╖,       ,,,╓╓╖╓,,,       ,,▄▄▄▄▄▄▄▄,
              ╙▀███████████▄████████████████▄████████████▀
                 ▀████████████████████████████████████▀
                    ▀██████████████████████████████▀"
                  ▄▄  "▀████████████████████████▀▀  ╓▓▄
                 ███╜ ╓██████████"-▀█████████████▄  ▀██▌
                ╟██▌ ▐██"╔██████▌   ██████'╔██████▌  ███
                ▓██⌐ ▓█▌ ╙████▒█▌   █████▌ ╙████╫██  ╟██C
                ▐██▌ ╙██▄    ╓██▌   ██████▄    ▄██▀  ███
                 ▀██▌  ▀██████▀"    ███▌ ▀██████▀` ,███╜
                  ▀███▄▄       ╓,   ████▄╖      ,▄████`
                    ╙▀████████████╖ ███████████████▀`
                        "╙▀▀▀▀▀██████████▀`╙▀▀▀"`
                                `▀█████▀
                                   ▀▀"\033[0m""")
    print("\033[34;94m" + "=" * 70 + "\033[0m")
    print("\033[33;93m{:^70}\033[0m".format("WGUPS Delivery Management System", terminal_width))
    print("\033[37;97m{:^70}\033[0m".format("Parcel Tracking & Reporting", terminal_width))
    print("\033[34;94m" + "=" * 70 + "\033[0m\n")

    input("\033[29;97;40m   Press Enter to continue...   " + "\033[0m")
    launch_interface()


def launch_interface():
    """
    Displays the main menu and routes user selections to appropriate options.
    Time Complexity: O(1)
    """
    while True:
        print("\033[34;94m" + """






█████████   ▐████   ▓███████[  ╓▄███████████C █████████   ███████▌
▀▀█████▀▀   █████▌  ╙▀█████▀`▄██████▀▀▀▀████U ▀▀█████▀▀   ▀▀████▀"
  ▓████▌   ▐██████    ████  ▓█████"     ▐███U  ]█████       ████
  └█████   ███████▌  ▐███▌ ]█████C             ]█████       ████
   ▓████▌ ▐███▐████  ████  ▐█████     ╖╖╖╖╖╖╖╖ ]█████       ████
    █████µ███⌐ ████▌▐███▌  ▐█████U   ]████████ ]█████       ████
    ▐███████▌  ▐████████    ██████     ╟████▌   █████⌐      ████
     ███████    ███████Ü     ██████▄▄▄▄▓████▌   ▀█████▄▄▄▄▄████"
     ▐█████▌    ▐█████▌       '▀████████████▌     ▀██████████▀
     """ "\033[0m")
        print("\n\n\n\033[34;94m" + "=" * 70 + "\033[0m")
        print("\033[33;93m" + "{:^70}".format(" Real-Time Tracking & Reporting ") + "\033[0m")
        print("\033[37;97m" + "{:^70}".format(" Displaying main menu") + "\033[0m")
        print("\033[34;94m" + "=" * 70 + "\n\033[0m")

        print("\n\033[37;97;40m" + "{:^66}".format("🦉 Please choose an option to get started 🦉") + "\033[0m" + "\n")
        print("\n\033[33;93;40m" + " 1. View current package status and van mileage " + "\033[0m")
        print("\n\033[33;93;40m" + " 2. Check package status at specific time " + "\033[0m")
        print("\n\033[33;93;40m" + " 3. View all package status at specific time " + "\033[0m")
        print("\n\033[0;47;40m" + " 4. EXIT PROGRAM " + "\033[0m")

        selection = input("\n\033[34;94;40m 🦉  Enter your selection (1-4): 🦉 \033[0m")

        if selection == '1':
            show_current_status()
            # After executing the user choice, prompt them to either return to the main menu or exit
            user_next_step = input(
                "\n\033[37;97m   Type 0 to return to the main menu or press any other key to exit the program: \033[0m")
            # If user_next_step is not '0', exit the program
            if user_next_step != '0':
                break
        elif selection == '2':
            check_specific_package()
            # After executing the user choice, prompt them to either return to the main menu or exit
            user_next_step = input(
                "\n\033[37;97m   Type 0 to return to the main menu or press any other key to exit the program: \033[0m")
            # If user_next_step is not '0', exit the program
            if user_next_step != '0':
                break
        elif selection == '3':
            check_all_packages_at_time()
            # After executing the user choice, prompt them to either return to the main menu or exit
            user_next_step = input(
                "\n\033[37;97m   Type 0 to return to the main menu or press any other key to exit the program: \033[0m")
            # If user_next_step is not '0', exit the program
            if user_next_step != '0':
                break
        elif selection == '4':
            print("\033[34;94m" + """
        ⠀⠀⠀⠀⠀⠀⢠⣾⣼⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⢸⣿⣿⡌⢢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣄⡀
        ⠀⠀⠀⠀⠀⠀⢸⣿⣾⣷⢀⠱⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⣿⣿⣷
        ⠀⠀⠀⠀⠀⠀⠘⣿⣿⣜⡟⡇⢳⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⣰⡟⣺⣿⣿⡟
        ⠀⠀⠀⠀⠀⢀⣠⣼⣿⣿⣾⣷⡒⢿⣿⠿⠛⢛⣛⣛⡷⠶⡴⡾⢏⣵⡿⣿⡿⠁
        ⠀⠀⠀⢀⣴⣟⣟⡿⣻⢿⣟⣱⡿⠆⣠⣒⡮⠉⡠⢤⣢⣨⡍⠈⢻⣭⣿⠟⠁⠀
        ⠀⠀⢠⣿⣽⣿⡟⢀⣼⠛⢭⣻⣾⣦⡀⠁⠊⠑⠙⠒⠲⠜⣽⠒⠉⣿⣿⡄⠀⠀
        ⠀⣰⣿⣿⡣⡋⢠⡿⠴⠞⣩⡞⢁⣤⣍⠳⣤⣴⡄⠀⠀⠁⢁⣗⠳⡿⢥⡇⠀⠀
        ⢀⣿⡟⣼⡗⠀⣿⣅⠀⢘⣛⣇⠈⠻⠟⢀⣿⡇⠈⠒⠈⠁⢾⡿⠀⣿⡍⠃⠀⠀
        ⢸⡟⣷⠛⠀⠀⠻⣦⢿⣭⣟⣯⡕⣒⣾⠽⠋⠁⠐⣾⡄⠀⠘⢤⡞⡳⠵⡇⠀⠀
        ⢸⣿⡉⠀⠀⠈⣿⣿⣶⣬⣭⣎⠉⠁⠀⠀⠀⢀⣠⣿⣿⠀⠀⠀⣙⢟⢭⡇⠀⠀
        ⡄⠋⠀⠀⠀⠀⠘⠁⠛⠻⢰⢤⡍⣁⠀⠸⢴⣿⣿⣿⡎⠆⠀⠦⠙⣹⣾⡀⠀⠀
        ⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠬⣫⢷⢄⠉⢛⠿⡟⠀⣀⣀⣼⡃⠈⡇⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⡶⣄⠀⠀⠈⠳⠳⣴⣶⠀⣤⣿⣷⣾⣯⡀⠍⣳⡄⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠿⠇⠀⠀⡑⢦⣄⡀⠈⣻⣶⠝⡭⡀⠈⣨⣩⠪⢃⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠲⢾⣿⡟⠁⢐⣷⣿⢅⢪⣎⠛⢻⣿⡤⢼⡀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠆⠉⠂⠀⠉⣛⡗⠋⠈⠱⠖⠊⡾⠶⠯⡇
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠀⠓⠀⠀⠀⠤⡭⢋⣺⡇ """ + "\033[0m")
            print("\033[32;92;40mThank you for using the WGUPS Delivery Management System. Goodbye! 🦉🦉🦉 \033[0m")
            break
        else:
            print("\033[31;91;40mInvalid selection. Please choose a valid option (1-4).\033[0m")


def show_current_status():
    """
    Displays current status of all packages and total van mileage in a table format.
    Time Complexity: O(n) where n is number of packages
    """
    current_time = datetime.datetime.now().time()

    # Handle special case for parcel 9
    handle_special_case_for_parcel_9(current_time)

    # Print header
    print("\n" + "\033[34;94m" + "*" * 142 + "\033[0m")
    print("\033[33;93m" + "{:^142}".format("SUMMARY OF TODAY\'S DELIVERIES") + "\033[0m")
    print("\033[37;97m" + "{:^146}".format(f"Time Queried:  {current_time.strftime('%I:%M %p')}" + "  🦉" + "\033[0m"))
    print("\033[34;94m" + "*" * 142 + "\033[0m\n")

    # Print note about delivery times
    print("\033[37;97mNOTE: Expected delivery times are indicated with 🦉 for packages not yet delivered.\n\033[0m")

    # Print table headers
    headers = ["ID", "DELIVERY ADDRESS", "DEADLINE", "SPECIAL NOTES", "STATUS", "VAN",
               "TIME OF DELIVERY"]

    print("\033[33;93;40m" +
          f"{headers[0]:<5} {headers[1]:<30} {headers[2]:<20} {headers[3]:<35} {headers[4]:<15} {headers[5]:<10} {headers[6]:<21}"
          + "\033[0m")
    print("")

    # Show package statuses
    for i in range(1, 41):
        try:
            package = parcels.delivery_registry.locate_parcel(i)
            if package:
                print("\033[34;94m" + format_package_info(package, current_time) + "\033[0m")
        except Exception as e:
            print(f"\033[0;31;40mError retrieving package {i}: {str(e)}\033[0m")

    # Calculate and display total mileage
    distances = locations.import_distances()
    total_mileage = 0
    # Strings for comparison
    time_format = "%H:%M"
    after_hours = datetime.datetime.strptime("17:00", time_format).time()
    before_hours = datetime.datetime.strptime("08:00", time_format).time()

    for vehicle in van.fleet:
        loc, miles = van.calculate_progress(current_time, vehicle, distances)
        total_mileage += miles
    if current_time > after_hours or current_time < before_hours:
        print("\n\033[31;91;40m   NO MILEAGE TO REPORT | TIME OF QUERY IS OUTSIDE OF NORMAL BUSINESS HOURS   \033[0m")
    else:
        print("\n\033[1;34;40mTotal fleet mileage: {:.1f} miles\033[0m".format(total_mileage))
    

def check_specific_package():
    """
    Allows user to check status of specific package at specific time.
    Time Complexity: O(1)
    """
    try:
        print("\n" + "\033[1;36;40m" + "-" * 90)
        print("{:^90}".format("PACKAGE LOOKUP"))
        print("-" * 90 + "\033[0m\n")

        pkg_id = int(input("\033[0;36;40mEnter package ID (1-40): \033[0m"))
        if pkg_id < 1 or pkg_id > 40:
            print("\033[0;31;40mInvalid package ID. Please enter a number between 1 and 40.\033[0m")
            return

        time_str = input("\033[0;36;40mEnter time to check (format: HH:MM am/pm): \033[0m")
        query_time = parse_time_input(time_str)
        if not query_time:
            return

        # Handle special case for parcel 9
        handle_special_case_for_parcel_9(query_time)

        package = parcels.delivery_registry.locate_parcel(pkg_id)
        if package:
            print("\n\033[1;36;40m=== Package Status ===\033[0m")
            print("\033[0;36;40m" + format_package_info(package, query_time) + "\033[0m")
        else:
            print(f"\033[0;31;40mPackage {pkg_id} not found.\033[0m")

    except ValueError:
        print("\033[0;31;40mInvalid input. Package ID must be a number.\033[0m")
    except Exception as e:
        print(f"\033[0;31;40mError: {str(e)}\033[0m")

def check_all_packages_at_time():
    """
    Shows status of all packages at specified time.
    Time Complexity: O(n) where n is number of packages
    """
    print("\n" + "\033[1;36;40m" + "-" * 90)
    print("{:^90}".format("PACKAGE STATUS LOOKUP"))
    print("-" * 90 + "\033[0m\n")

    time_str = input("\033[0;36;40mEnter time to check (format: HH:MM am/pm): \033[0m")
    query_time = parse_time_input(time_str)
    if not query_time:
        return

    # Handle special case for parcel 9
    handle_special_case_for_parcel_9(query_time)

    print("\n" + "\033[1;36;40m" + "-" * 105)
    print("{:^105}".format("PACKAGE STATUS SUMMARY"))
    print("{:^105}".format(f"query time: {query_time.strftime('%I:%M %p')}"))
    print("-" * 105 + "\033[0m\n")

    # Print note about delivery times
    print("\033[0;37;40mNOTE: Expected TOD (Time of Delivery) indicated by 🦉 for undelivered packages.\n\033[0m")

    # Print table headers
    headers = ["ID", "DELIVERY ADDRESS", "DEADLINE", "NOTES", "STATUS", "VAN", "DELIVERY DETAILS"]
    print("\033[1;36;40m" +
          f"{headers[0]:<2} {headers[1]:<25} {headers[2]:<10} {headers[3]:<32} {headers[4]:<12} {headers[5]:<8} {headers[6]}" +
          "\033[0m")

    # Update package statuses
    parcels.update_status(query_time)

    # Display all package info
    for i in range(1, 41):
        try:
            package = parcels.delivery_registry.locate_parcel(i)
            if package:
                print("\033[0;36;40m" + format_package_info(package, query_time) + "\033[0m")
        except Exception as e:
            print(f"\033[0;31;40mError retrieving package {i}: {str(e)}\033[0m")

    # Show van mileage
    distances = locations.import_distances()
    total_mileage = 0
    print("\n\033[1;36;40m=== Van Mileage ===\033[0m")
    for vehicle in van.fleet:
        loc, miles = van.calculate_progress(query_time, vehicle, distances)
        total_mileage += miles
        print(f"\033[0;36;40mVan {vehicle.id}: {miles:.1f} miles\033[0m")
    print(f"\n\033[1;34;40mTotal fleet mileage: {total_mileage:.1f} miles\033[0m")

    # Menu options
    print("\n\033[0;37;40mEnter 0 to return to the main menu.")
    print("Enter any other key to exit.\033[0m")

def parse_time_input(time_str):
    """
    Parses time input in 'HH:MM am/pm' format.
    Time Complexity: O(1)
    """
    try:
        return datetime.datetime.strptime(time_str, "%I:%M %p").time()
    except ValueError:
        print("\n\033[0;31;40mInvalid time format. Please use 'HH:MM am/pm' (e.g. '09:30 am')\033[0m")
        return None
