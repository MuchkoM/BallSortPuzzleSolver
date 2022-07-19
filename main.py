from solver.screenshot_cv import ScreenshotCV
from solver.solution_finder import SolutionBuilder
from solver.solution_printer import SolutionPrinter
from solver.utils import get_file

if __name__ == "__main__":
    analyzer = ScreenshotCV(get_file())
    analyzer.analyze()

    solver = SolutionBuilder(analyzer.field)
    solver.solve()

    if solver.is_solved():
        solution_printer = SolutionPrinter(analyzer.field, solver.fast_way(), analyzer.palette)
        solution_printer.print_way()
    else:
        print('Solution is not found')
