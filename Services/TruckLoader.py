import HashTable

# on truck 2 (3, 18, 36, 38)
#delayed packages until 905 (6, 25, 28, 32)
# wrong address correction at 1020 9
# package 15 must be on truck one and delivered before 9 am
# 10:30 am delivery deadline packages 6 13 14 16 20 25 29 30 31 34 37
# each truck can only hold 16 packages     there are 3 trucks and only two drivers  loading trucks takes 0 time

class SortTruck:
    def __init__(self, packages, address_map, distance_table):
        self.packages = packages
        self.address_map = address_map
        self.distance_table = distance_table
        self.package_set = set()
        self.sorted_packages = []
        self.number_of_packages = len(packages)

    def nearest_neighbor(self, current_address):
        #chose an arbitrary longest distance that was greater than any distance in d matrix
        min_distance = float(15)
        nearest = None
        nearest_package = None

        for package in self.packages:
            package_address = package[1]['Address']
            if package_address in self.address_map:
                index = self.address_map[package_address]
                current_index = self.address_map[current_address]
                # since I only build out half of the distance matrix and since any position [n][m] == [m][n] in the complete matrix I simply check to see if n > m and swap if so which pivots to the same position mirrored across the diagonal
                if current_index < index:
                    temp = current_index
                    current_index = index
                    index = temp
                if self.distance_table[current_index][index] < min_distance:
                    min_distance = self.distance_table[current_index][index]
                    nearest = current_address
                    nearest_package = package


        return nearest_package









    def same_address(self, nearest_package):
        same_address_list = []
        for package in self.packages:
            if package[1]['Address'] == nearest_package[1]['Address']:
                self.sorted_packages.append(package)
                same_address_list.append(package)
        for package in same_address_list:
            self.packages.remove(package)



    def sort_packages(self):


        current_address = "4001 South 700 East"  # replace this with your hub address

        while len(self.sorted_packages) < self.number_of_packages:
            current_package = self.nearest_neighbor(current_address)
            current_address = current_package[1]['Address']
            self.sorted_packages.append(current_package)
            self.packages.remove(current_package)
            self.same_address(current_package)

        return self.sorted_packages

def same_address_loader(current_truck_packages, other_packages):
    package_id_set = set()
    for pkg in current_truck_packages:
        package_id_set.add(pkg[0])
    packages_on_truck = current_truck_packages.copy()
    for pkg in current_truck_packages:
        for package in other_packages:
            if pkg[1]['Address'] == package[1]['Address'] and package[0] not in package_id_set:
                packages_on_truck.append(package)
                if len(package_id_set) >= 16:
                    return packages_on_truck

                package_id_set.add(package[0])

    return packages_on_truck

def remove_used_packages(packages_on_truck, other_packages):
    for pkg in packages_on_truck:
        if pkg in other_packages:
            other_packages.remove(pkg)

    return other_packages

def load_trucks(packages, address_map, distance_table):
    preset_packages_truck2 = [(3, packages.get(3)),(18, packages.get(18)),(36, packages.get(36)),(38, packages.get(38))]
    delayed_packages = [(6, packages.get(6)),(25, packages.get(25)),(28, packages.get(28)),(32, packages.get(32))]
    deadline_packages = [(13, packages.get(13)),(14, packages.get(14)),(16, packages.get(16)),(20, packages.get(20)),(29, packages.get(29)),
                         (30, packages.get(30)),(31, packages.get(31)),(34, packages.get(34)),(37, packages.get(37))]
    wrong_address_package = (9, packages.get(9))

    # All other packages that don't fall into any constraints
    all_packages = [(i, packages.get(i)) for i in range(1, 41)]
    other_packages = [pkg for pkg in all_packages if
                      pkg not in preset_packages_truck2 + delayed_packages + deadline_packages + [wrong_address_package,(15, packages.get(15))]]
    # future enhancement: check to see if any preloaded packages share an address with any remaining packages, load those on to the same truck
    # Load Truck 1 with packages that need to be delivered before 0930, then fill with random other packages from other_packages without discrimination
    truck1 = [(15, packages.get(15))] + deadline_packages[:min(len(deadline_packages), 15)]

    truck1 = same_address_loader(truck1, other_packages)
    other_packages = remove_used_packages(truck1, other_packages)
    deadline_packages = remove_used_packages(truck1, deadline_packages)
    #left_space_truck1 = 16 - len(truck1)
    #truck1 += other_packages[:left_space_truck1]

    # Load Truck 2
    truck2 = preset_packages_truck2
    truck2.append(wrong_address_package)

    truck2 = same_address_loader(truck2, other_packages)
    other_packages = remove_used_packages(truck2, other_packages)
    #left_space_truck2 = 16 - len(truck2)
    #truck2 += other_packages[:left_space_truck2]


    # Load Truck 3
    truck3 = delayed_packages + deadline_packages
    truck3 = same_address_loader(truck3, other_packages)
    other_packages = remove_used_packages(truck3, other_packages)

    space_left_truck1 = 16 - len(truck1)
    truck1 += other_packages[:space_left_truck1]
    other_packages = remove_used_packages(truck1, other_packages)
    space_left_truck2 = 16 - len(truck2)
    truck2 += other_packages[:space_left_truck2]
    other_packages = remove_used_packages(truck2, other_packages)
    space_left_truck3 = 16 -len(truck3)
    truck3 += other_packages[:space_left_truck3]
    print(other_packages)
    truck1_sorted = SortTruck(truck1, address_map, distance_table).sort_packages()
    truck2_sorted = SortTruck(truck2, address_map, distance_table).sort_packages()
    truck3_sorted = SortTruck(truck3, address_map, distance_table).sort_packages()
    print(other_packages)
    print('REMAINING PACKAGES')
    print(other_packages)
    return truck1_sorted, truck2_sorted, truck3_sorted