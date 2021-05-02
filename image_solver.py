import glob
import os

import task_finder
import task_solver
import copy
from task_solver import Solver


class ImageSolver:
    def __init__(self, image_name):
        self._image_name = image_name
        self._task = []
        self._way = []

    def solve(self):
        self._task = task_finder.analise(self._image_name)
        solver = Solver(self._task)
        solver.solve()
        self._way = solver.way

    @property
    def task(self):
        return copy.deepcopy(self._task)

    @property
    def way(self):
        return copy.deepcopy(self._way)

    def print(self):
        task_solver.print_solution(self._task, self._way)


if __name__ == '__main__':
    files = glob.glob('*.jpg')
    files.sort(key=lambda x: os.path.getctime(x))

    image_solver = ImageSolver(files[-1])
    image_solver.solve()
    image_solver.print()
