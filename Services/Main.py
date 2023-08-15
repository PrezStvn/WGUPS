import FileReader
import HashTable
import TruckLoader
import csv
from DeliveryCalculator import calculate_delivery_times
from DeliveryCalculator import calculate_total_distance

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

file_name = 'packages.csv'
packages = FileReader.read_packages(file_name)
file_name2 = 'wgups_distance_table.csv'
distances, addressMap = FileReader.read_distances(file_name2)

package_table = HashTable.HashTable(len(packages))
for package in packages:
    package_table.map_package(package)

mapSet = set()
for package in package_table:
    mapSet.add(addressMap[package[1]['Address']])
for i in range(28):
    if i not in mapSet:
        print(i)
print(addressMap)



file_path = 'ditances.csv'
distance_table = csv_to_distance_matrix(file_path)
print(distance_table)

truck1, truck2, truck3 = TruckLoader.load_trucks(package_table, addressMap, distance_table)
print(truck1)
print(len(truck1))
print(truck2)
print(len(truck2))
print(truck3)
print(len(truck3))


def calculate_trucks_miles(truck):
    total_distance = 0
    last_address_index = 0
    delivery_route = []
    for package in truck:
        this_leg = float('inf')
        curr_address_index_in_distance_table = addressMap[package[1]['Address']]
        # check to see if first index is less than second. if true we swap to avoid index out of bounds
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

truck3_last_stop = truck3[-1]
last_stop_address = addressMap[truck3_last_stop[1]['Address']]
distance_from_truck3_last_stop = distance_table[last_stop_address][0]
first_driver_route = calculate_trucks_miles(truck1)
return_leg = ('HUB', distance_from_truck3_last_stop)


second_driver_route = calculate_trucks_miles(truck3)
second_driver_route.append(return_leg)
second_driver_route = second_driver_route + calculate_trucks_miles(truck2)
first_driver_route = first_driver_route
# total_miles = calculate_trucks_miles(truck1) + calculate_trucks_miles(truck2) + calculate_trucks_miles(truck3) + distance_from_truck3_last_stop



print(first_driver_route)
print(second_driver_route)
start_time = '8:00'
first_truck_delivery_times = calculate_delivery_times(first_driver_route, start_time)
delayed_start_time = '9:05'
second_driver_delivery_times = calculate_delivery_times(second_driver_route, delayed_start_time)
print(first_truck_delivery_times)
print(second_driver_delivery_times)

total_wgups_miles_traversed = calculate_total_distance(first_driver_route) + calculate_total_distance(second_driver_route)
print(total_wgups_miles_traversed)