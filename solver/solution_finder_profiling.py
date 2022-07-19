import cProfile

from solver.field import Field
from solver.palette import Palette
from solver.solution_finder import SolutionBuilder

if __name__ == "__main__":
    from examples.level2__.const import field_arr, palette_arr

    profiling_file = '/tmp/restats'

    field = Field(field_arr)
    palette = Palette(palette_arr)
    solver = SolutionBuilder(field)

    cProfile.run('solver.solve()', sort='cumtime')
