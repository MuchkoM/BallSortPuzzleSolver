from typing import List, Tuple

from solver.utils import cie76


class Palette:
    def __init__(self, palette: List[Tuple[int, int, int]] = None, familiarity: int = 20):
        self.familiarity: int = familiarity
        self.palette: List[Tuple[int, int, int]] = palette or []

    def get_color_by_index(self, index: int) -> Tuple[int, int, int]:
        return self.palette[index]

    def get_index_by_color(self, color: Tuple[int, int, int]) -> int:
        for know_index, know_color in enumerate(self.palette):
            if cie76(know_color, color) < self.familiarity:
                return know_index
        self.palette.append(color)
        return len(self.palette) - 1

    def __repr__(self):
        return str(self.palette)
