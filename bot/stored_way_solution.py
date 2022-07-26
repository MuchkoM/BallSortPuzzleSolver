class StoredWaySolution:
    def __init__(self, way, field, solution):
        self.solution = solution
        self.field = field
        self.way = way

    def __hash__(self):
        return hash(self.field)
