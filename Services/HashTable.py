class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * self.size

    def _hash(self, key):
        key = int(key) - 1
        return key % self.size

    def map_package(self, package):
        key = package['Package ID']
        value = {k: v for k, v in package.items()}
        self.put(key, value)

    def put(self, key, value):
        index = self._hash(key)
        self.table[index] = (key, value)

    def get(self, key):
        index = self._hash(key)
        if int(self.table[index][0]) == key:
            return self.table[index][1]
    # added this shortly before submission
    # was trying to think of a way to use this in the sorting portion of the algorithm instead of my lists
    def remove(self, key):
        index = self._hash(key)
        if self.table[index] is not None and int(self.table[index][0]) == key:
            self.table[index] = None
        else:
            print(f"Key {key} not found or no value at {key}.")

    def __iter__(self):
        for key_value in self.table:
            if key_value is not None:
                yield key_value

    def status(self):
        return [item[1] for item in self.table if item is not None]

    def print(self):
        for package in self.table:
            print(f'Package: {package}')

