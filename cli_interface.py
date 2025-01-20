import datetime
import sys
import locations
import parcels
import van

def launch_welcome():
    """
    Displays the ASCII welcome screen and transitions to the main menu.
    """
    print("\033[1;34m" + """

   █████████   ▐████   ▓███████[  ╓▄███████████C █████████   ███████▌
   ▀▀█████▀▀   █████▌  ╙▀█████▀`▄██████▀▀▀▀████U ▀▀█████▀▀   ▀▀████▀"
     ▓████▌   ▐██████    ████  ▓█████"     ▐███U  ]█████       ████
     └█████   ███████▌  ▐███▌ ]█████C             ]█████       ████
      ▓████▌ ▐███▐████  ████  ▐█████     ╖╖╖╖╖╖╖╖ ]█████       ████
       █████µ███⌐ ████▌▐███▌  ▐█████U   ]████████ ]█████       ████
       ▐███████▌  ▐████████    ██████     ╟████▌   █████⌐      ████
        ███████    ███████Ü     ██████▄▄▄▄▓████▌   ▀█████▄▄▄▄▄████"
        ▐█████▌    ▐█████▌       '▀████████████▌     ▀██████████▀

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
                                   ▀▀"
 \033[0m
            \033[1;36;40m======= WGUPS Delivery Management System =======\033[0m
            \033[1;36;40m        Parcel Tracking & Reporting        \033[0m
                    """)
    input("Press any key to get started...")
    launch_interface()

def launch_interface():
    """
    Displays the main menu and routes user selections to appropriate options.
    """
    while True:
        print("""        
        
        Displaying main menu...

        
        ======= Real-Time Tracking & Reporting =======
        >>> Please choose an option to get started <<<
        
        1. View live delivery updates (real-time status of packages and trucks)
        2. Check past delivery status (query by time)
        3. Exit the system
        """)
        selection = input("Enter your selection (1-3): ")

        if selection == '1':
            live_updates_menu()
        elif selection == '2':
            past_delivery_menu()
        elif selection == '3':
            print('''
            
            
   █████████   ▐████   ▓███████[  ╓▄███████████C █████████   ███████▌
   ▀▀█████▀▀   █████▌  ╙▀█████▀`▄██████▀▀▀▀████U ▀▀█████▀▀   ▀▀████▀"
     ▓████▌   ▐██████    ████  ▓█████"     ▐███U  ]█████       ████
     └█████   ███████▌  ▐███▌ ]█████C             ]█████       ████
      ▓████▌ ▐███▐████  ████  ▐█████     ╖╖╖╖╖╖╖╖ ]█████       ████
       █████µ███⌐ ████▌▐███▌  ▐█████U   ]████████ ]█████       ████
       ▐███████▌  ▐████████    ██████     ╟████▌   █████⌐      ████
        ███████    ███████Ü     ██████▄▄▄▄▓████▌   ▀█████▄▄▄▄▄████"
        ▐█████▌    ▐█████▌       '▀████████████▌     ▀██████████▀
        
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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠀⠓⠀⠀⠀⠤⡭⢋⣺⡇


            Thank you for using the WGUPS Delivery Management System. Goodbye!
            ''')
            break
        else:
            print("Invalid selection. Please choose a valid option (1-3).")


def live_updates_menu():
    """
    Displays the live delivery updates menu and handles user input.
    """
    current_time = datetime.datetime.now().time()
    while True:
        print(
            f"\033[1;36;40m\n======= Live Delivery Updates =======\n"
            f"Current Time: {current_time.strftime('%I:%M %p')}\n\n"
            "\033[0;37;40mWhat would you like to do?\n"
            "1. View the status of all packages\n"
            "2. Look up a package by ID\n"
            "3. Check the location and mileage of all trucks\n"
            "4. Return to the main menu\n"
        )
        selection = input("\033[0;36;40mEnter selection (1-4): ")
        if selection == '1':
            package_status_menu(current_time)
        elif selection == '2':
            package_lookup(current_time)
        elif selection == '3':
            truck_status_menu(current_time)
        elif selection == '4':
            return
        else:
            print("\n\033[0;31;40mERROR: Invalid selection. Please choose 1-4.\n")


def past_delivery_menu():
    """
    Displays the past delivery status menu and handles user input.
    """
    query_time = input("\033[1;35;40mEnter the time to query delivery status (format: HH:MM am/pm): ")
    try:
        query_time = datetime.datetime.strptime(query_time, "%I:%M %p").time()
    except ValueError:
        print("\n\033[0;31;40mInvalid time format. Use 'HH:MM am/pm' (e.g., '09:30 am').\n")
        return

    while True:
        print(
            f"\033[0;35;40m\n======= Past Delivery Status =======\n"
            f"Status as of {query_time.strftime('%I:%M %p')}:\n\n"
            "\033[0;37;40m1. View the status of all packages\n"
            "2. Look up a package by ID\n"
            "3. Check the location and mileage of all trucks\n"
            "4. Return to the main menu\n"
        )
        selection = input("\033[0;36;40mEnter selection (1-4): ")
        if selection == '1':
            package_status_menu(query_time)
        elif selection == '2':
            package_lookup(query_time)
        elif selection == '3':
            truck_status_menu(query_time)
        elif selection == '4':
            return
        else:
            print("\n\033[0;31;40mERROR: Invalid selection. Please choose 1-4.\n")


def package_status_menu(query_time):
    """
    Displays the status of all packages at the specified time.
    """
    try:
        parcels.update_status(query_time)
        print(f"\n\033[1;36;40m======= Package Status =======\n")
        for pkg_id in range(1, 41):
            try:
                pkg = parcels.delivery_registry.locate_parcel(pkg_id)
                if pkg:
                    print(f"ID: {pkg.tracking_id}, Status: {pkg.status}, Delivery Time: {pkg.delivery_time.time()}")
            except LookupError:
                print(f"Package {pkg_id}: Not found in the system")
            except Exception as e:
                print(f"Error retrieving package {pkg_id}: {str(e)}")
    except Exception as e:
        print(f"\033[0;31;40mError generating package status report: {str(e)}\n")


def package_lookup(query_time):
    """
    Searches for a specific package by ID and displays its status.
    """
    try:
        pkg_id = int(input("\033[1;36;40mEnter Package ID: "))
        pkg = parcels.delivery_registry.locate_parcel(pkg_id)
        if pkg:
            print(
                f"\nPackage ID: {pkg.tracking_id}\n"
                f"Destination: {pkg.destination}\n"
                f"Status: {pkg.status}\n"
            )
        else:
            print("\033[0;31;40mPackage not found.\n")
    except ValueError:
        print("\033[0;31;40mPlease enter a valid numeric ID.\n")
    except LookupError:
        print("\033[0;31;40mPackage not found in system.\n")
    except Exception as e:
        print(f"\033[0;31;40mError looking up package: {str(e)}\n")


def truck_status_menu(query_time):
    """
    Displays the location and total mileage of all trucks at the specified time.
    """
    distances = locations.import_distances()
    total_mileage = 0
    for vehicle in van.fleet:
        loc, dist_traveled = van.calculate_progress(query_time, vehicle, distances)
        total_mileage += dist_traveled
        print(f"\nTruck {vehicle.id} at location {loc}, Distance traveled: {dist_traveled:.2f} miles")
    print(f"\033[1;32;40m\nTotal mileage for all trucks: {total_mileage:.2f} miles\n")
