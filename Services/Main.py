# Steven Perez 004439406

import FileReader
from DeliverySimulator import DeliverySim
import HashTable
import TruckLoader
import csv
from DeliveryCalculator import calculate_delivery_times
from DeliveryCalculator import calculate_total_distance
# this should be moved   i wrote this later after realizing it would be easier to just rep the distances in a 2d matrix and not require address headers for reference.
#if the layout of the project changes this will also have to change obviously.  this potentially is not necessary if using some external api for address/distance calculation.
# I imagine a real world solution would probably incorporate such methods.


def csv_to_distance_matrix(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        matrix = []
        for row_num, row in enumerate(reader):
            curr_row = []
            # Convert the empty strings to a specific distance value (e.g., float('inf') for infinity)
            # and convert others to float values
            # matrix_row = [float(cell) if cell else '' for cell in row]

            for i in range(row_num + 1):

                curr_row.append(float(row[i]))

            matrix.append(curr_row)
    return matrix


def calculate_trucks_miles(truck, addressMap, distance_table):
    total_distance = 0
    last_address_index = 0
    delivery_route = []
    for package in truck:
        this_leg = float('inf')
        curr_address_index_in_distance_table = addressMap[package[1]['Address']]
        # check to see if first index is less than second. if true we swap to avoid index out of bounds.  this is the n x m --> m x n switch I discuss above.
        # some implementations elsewhere use the temp value switch to swap n and m instead of writing an if else.
        if last_address_index < curr_address_index_in_distance_table:
            this_leg = distance_table[curr_address_index_in_distance_table][last_address_index]
        else:
            this_leg = distance_table[last_address_index][curr_address_index_in_distance_table]
        total_distance = total_distance + this_leg
        package_delivery_info = (package[0], this_leg)
        delivery_route.append(package_delivery_info)
        # print(f"'package #' {package[0]} ' last address' {last_address_index} 'curr address' {curr_address_index_in_distance_table} 'distance between them' {this_leg} 'total distance at present' {total_distance}")
        last_address_index = curr_address_index_in_distance_table
    return delivery_route


def wrapperClass(callback, addressMap, distance_table):
    def inner_function(truck):
        return callback(truck, addressMap, distance_table)
    return inner_function


def main():

    # creating my data structures from the excel export csv's (I did minimal editing to the csv's)
    file_name = 'packages.csv'
    #packages is the python native hashtable representation of the packages.
    packages = FileReader.read_packages(file_name)
    file_name2 = 'wgups_distance_table.csv'
    distances, addressMap = FileReader.read_distances(file_name2)
    # used the built in python dictionary to then make my dictionary.  I do not know if this will be considered cheating. I personally thing it does not change much as I am passing the 'value' or package object to
    # my own hashtable.  I could rewrite to either create a list of package objects then iterate through that adding them to my own hashtable.  or create an obj from the csv then add to my hashtable.
    package_table = HashTable.HashTable(len(packages))
    for package in packages:
        package_table.map_package(package)

    # creating my 2d matrix for distances   only one half of the matrix is populated so logic is written for all functions accessing it to switch n x m -- > m x n if m > n since the complete table is symmetric across the diagonal
    file_path = 'distances.csv'
    distance_table = csv_to_distance_matrix(file_path)
    print(distance_table)
    # creating a data structure for each truck in use today and "loading" packages onto them
    truck1, truck2, truck3 = TruckLoader.load_trucks(package_table, addressMap, distance_table)

    # calculating trucks miles and the distance traveled for each "leg" of the journey. Meaning the distance traveled since the last package was delivered.  If this_leg == 0 then the last package was at the same address
    # hard coded the return trip for driver 2 on truck 3.  using -1 to dynamically access whatever his last stop was. and add the return trip to the 'HUB'
    truck3_last_stop = truck3[-1]
    last_stop_address = addressMap[truck3_last_stop[1]['Address']]
    distance_from_truck3_last_stop = distance_table[last_stop_address][0]
    return_leg = ('HUB', distance_from_truck3_last_stop)
    driver_route = wrapperClass(calculate_trucks_miles, addressMap, distance_table)
    first_driver_route = driver_route(truck1)
    second_driver_route = driver_route(truck2)
    second_driver_route.append(return_leg)
    second_driver_route = second_driver_route + driver_route(truck3)

    # total_miles = calculate_trucks_miles(truck1) + calculate_trucks_miles(truck2) + calculate_trucks_miles(truck3) + distance_from_truck3_last_stop
    # can do a for loop of both routes and accumulate the second value of each to add total mileage now that both driver routes are complete
    # note that at the end of each route neither driver returns to hub.  only time a driver returns to hub is when driver 2 finished truck 3 route and must return to switch to truck 2
    #technically only 2 trucks are needed since package load times are 0s at hub


    print(first_driver_route)
    print(second_driver_route)
    # setting a workday start time for the truck that can leave immediately
    start_time = '8:00'
    # turning the miles for each leg into time taken by using the avg speed of 18mph
    first_truck_delivery_times = calculate_delivery_times(first_driver_route, start_time)
    delayed_start_time = '9:05'
    second_driver_delivery_times = calculate_delivery_times(second_driver_route, delayed_start_time)
    print(first_truck_delivery_times)
    print(second_driver_delivery_times)

    total_wgups_miles_traversed = calculate_total_distance(first_driver_route) + calculate_total_distance(second_driver_route)
    print("Total miles driven for todays packages : ", total_wgups_miles_traversed)
    stay_in_loop = True
    while stay_in_loop:
        print("Type exit or EXIT instead of a time to end the program")
        target_time = input("Status of packages at what time? format: HH:MM \n")
        if target_time.lower() == 'exit':
            print("Exiting simulation")
            stay_in_loop = False
            continue
        else:
            current_sim = DeliverySim(package_table, first_truck_delivery_times, second_driver_delivery_times, target_time)
            status = current_sim.check_package_status()

if __name__ == '__main__':
    main()



