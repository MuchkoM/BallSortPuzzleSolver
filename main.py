from solver.screenshot_cv import ScreenshotCV
from solver.solution_finder import SolutionFinder
from solver.solution_printer import SolutionPrinter
from solver.solution_printer_stepped import SolutionPrinterStepped

if __name__ == "__main__":
    from examples.const import image_name

    analyzer = ScreenshotCV(image_name)
    analyzer.analyze()

    solver = SolutionFinder(analyzer.field)
    solver.solve()

    print_step_list = SolutionPrinter(solver.field, solver.solved_way, analyzer.palette)
    print_step_list.build()

    solution_printer = SolutionPrinterStepped(print_step_list)
    solution_printer.interact()
