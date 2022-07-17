from solver.screenshot_cv import ScreenshotCV
from solver.solution_finder import SolutionBuilder
from solver.solution_printer import SolutionPrinter
from solver.utils import get_file

if __name__ == "__main__":
    analyzer = ScreenshotCV(get_file())
    field, palette = analyzer.analyze()

    solver = SolutionBuilder(field)

    is_solved, way = solver.solve()
    if is_solved:
        solution_printer = SolutionPrinter(field, way, palette)
        solution_printer.print_way()
    else:
        print('Solution is not found', way.way)
