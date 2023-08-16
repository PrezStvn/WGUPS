
import csv
import HashTable
from io import StringIO


class WeightedGraph:
    def __init__(self):
        self.graph = {}  # Initialize an empty dictionary to hold the adjacency list

    def add_edge(self, u, v, weight):
        # Add an edge between nodes u and v with the given weight
        # Since the graph is undirected, we add (v, weight) to u's list and (u, weight) to v's list

        # If u is not already in the graph, add it with an empty list
        if u not in self.graph:
            self.graph[u] = []

        # If v is not already in the graph, add it with an empty list
        if v not in self.graph:
            self.graph[v] = []

        self.graph[u].append((v, weight))  # Add (v, weight) to u's list
        self.graph[v].append((u, weight))  # Add (u, weight) to v's list

    def print_graph(self):
        for node, neighbors in self.graph.items():
            neighbors_str = ', '.join([f'({neighbor}, {weight})' for neighbor, weight in neighbors])
            print(f"{node}: {neighbors_str}")



def read_packages(file_name):
    packages = []
    x = 0
    with open(file_name, 'r') as file:
        # Skip irrelevant lines until headers are found
        for line in file:
            if line.startswith('Package ID'):
                headers = line.strip().split(',')
                x = len(headers)
                print(headers)
                break

        # Read the package data lines
        for line in file:
            values = line.strip().split(',')[:x]
            package = {header: value for header, value in zip(headers, values)}
            packages.append(package)
            # creating and setting the status key, value for the CLI visualization later on.
            package['Status'] = 'At the hub'
    return packages

def read_distances(file_name):
    distances = WeightedGraph()
    addressMap = {}
    with open(file_name, 'r') as file:
        for line in file:
            if line.startswith('DISTANCE BETWEEN HUBS'): break
        x = 0
        for line in file:
            if line.startswith(' STOP'): break
            values = line.strip().split(',')
            addressMap[values[0].strip('"')] = x
            x+=1
        y = 0
        m = len(addressMap)
        m_iterator = 1
        key_value_1 = ''
        for line in file:
                # if m_iterator > the number of addresses we have
            if m_iterator >= m: break
                # the csv by default was split into 3 lines for each excel entry so created this instead of reformatting the csv for some reason
            if y == 0:
                y += 1
                continue
            elif y==1:
                values = line.strip().split(',')
                key_value_1 = values[0].strip('"')
                y += 1
            elif y==2:
                if m_iterator == 1:
                    distances.add_edge(key_value_1, 0, 0.0)
                    y = 0
                    m_iterator += 1
                    continue

                values = line.strip().split(',')
                for i in range(m_iterator):
                   distances.add_edge(key_value_1, i, float(values[i+1]))
                   if i + 2 > (len(values) - 1): break

                m_iterator += 1
                y = 0

    return distances, addressMap


def csv_to_distance_matrix(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        matrix = []
        for row in reader:
            # Convert the empty strings to a specific distance value (e.g., float('inf') for infinity)
            # and convert others to float values
            matrix_row = [float(cell) if cell else float('inf') for cell in row]
            matrix.append(matrix_row)
    return matrix

# Example usage:











