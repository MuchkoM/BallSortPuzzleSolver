from solver.screenshot_cv import ScreenshotCV
from solver.solution_finder import SolutionFinder
from solver.solution_printer_stepped import SolutionPrinterStepped
from solver.utils import get_file

if __name__ == "__main__":
    analyzer = ScreenshotCV(get_file())
    analyzer.analyze()

    solver = SolutionFinder(analyzer.field)
    solver.solve()

    if solver.is_solved:
        solution_printer = SolutionPrinterStepped(analyzer.field, solver.solved_way, analyzer.palette)
        solution_printer.interact()
    else:
        print('Solution is not found')
