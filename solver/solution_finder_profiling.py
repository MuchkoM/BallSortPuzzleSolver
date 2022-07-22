import cProfile

from solver.field import Field
from solver.palette import Palette
from solver.solution_finder import SolutionFinder

if __name__ == "__main__":
    from examples.level2__.const import field_arr, palette_arr

    field = Field(field_arr)
    palette = Palette(palette_arr)
    solver = SolutionFinder(field)

    cProfile.run('solver.solve()', sort='cumtime')
