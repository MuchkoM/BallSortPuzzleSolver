import pickle

from solver.field import Field
from solver.way import Way


class SolutionCache:
    def __init__(self):
        self.store = dict()

    def add(self, key, value):
        self.store[hash(key)] = value

    def get(self, key):
        return self.store.get(hash(key))

    def save(self, file):
        pickle.dump(self.store, file)

    def load(self, file):
        self.store = pickle.load(file)

    def __len__(self):
        return len(self.store)


if __name__ == "__main__":
    cache = SolutionCache()

    from examples.level297.const import field_arr, way_arr

    filed = Field(field_arr)
    way = Way(way_arr)

    cache.add(filed, way)
    with open('./Cache.save', 'bw') as f:
        cache.save(f)

    del cache

    cache = SolutionCache()

    with open('./Cache.save', 'br') as f:
        cache.load(f)

    print(len(cache))
