# write method that takes the starting hub and iterates through every package on the truck to determine which  point is closest to the starting point
# continue to do this until a route is made
# each time the next point (address or package to deliver) is picked it must be added to a set to track the packages we have used already.

class SortTruck:
    def __init__(self, packages, address_map, distance_table):
        self.packages = packages
        self.address_map = address_map
        self.distance_table = distance_table
        self.visited = set()

    def nearest_neighbor(self, current_address):
        """Find the nearest unvisited neighbor for the current address."""
        min_distance = float('inf')
        nearest_address = None

        current_index = self.address_map[current_address]

        for address, index in self.address_map.items():
            # Check if the address is unvisited and not the current address
            if address not in self.visited and current_address != address:
                if self.distance_table[current_index][index] < min_distance:
                    min_distance = self.distance_table[current_index][index]
                    nearest_address = address

        return nearest_address

    def sort_packages(self):
        """Sort the packages using the nearest neighbor algorithm."""

        current_address = 0
        sorted_packages = []

        while len(self.visited) < len(self.packages):
            if current_address in self.packages:
                for pkg_id in self.packages[current_address]:
                    sorted_packages.append((current_address, pkg_id))
                self.visited.add(current_address)

            current_address = self.nearest_neighbor(current_address)

        return sorted_packages