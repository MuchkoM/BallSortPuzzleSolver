import cProfile

from solver.field import Field
from solver.solution_finder import SolutionFinder

if __name__ == "__main__":
    from examples.const import field_arr

    field = Field(field_arr)
    solver = SolutionFinder(field)

    cProfile.run('solver.solve()', sort='cumtime')
