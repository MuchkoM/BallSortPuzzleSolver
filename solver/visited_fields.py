from solver.field import Field
from solver.way import Way


class VisitedFields:
    def __init__(self):
        self.visited = dict()

    def is_known(self, cur: Field, way: Way):
        cur_t = hash(cur)
        cur_len = len(way)
        if cur_t in self.visited and cur_len >= self.visited[cur_t]:
            return True

        self.visited[cur_t] = cur_len

    def __repr__(self):
        return str(self.visited)

    def __len__(self):
        return len(self.visited)


class VisitedFieldsSimple:
    def __init__(self):
        self.visited = set()

    def is_known(self, cur: Field, way: Way):
        if cur in self.visited:
            return True
        self.visited.add(cur)
