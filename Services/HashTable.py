class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * self.size

    def _hash(self, key):
        key = int(key) - 1
        return key % self.size

    def map_package(self, package):
        key = package['Package ID']
        value = {k: v for k, v in package.items() if k != 'Package ID'}
        self.put(key, value)

    def put(self, key, value):
        index = self._hash(key)
        self.table[index] = (key, value)

    def get(self, key):
        index = self._hash(key)
        if int(self.table[index][0]) == key:
            return self.table[index][1]

    def __iter__(self):
        for key_value in self.table:
            if key_value is not None:
                yield key_value

    def print(self):
        for package in self.table:
            print(f'Package: {package}')

