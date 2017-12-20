from . import SolverStrategy

class SolvedSolverStrategy(SolverStrategy):
    @property
    def name(self):
        return "Solved"

    def _apply_strategy(self, clues, cells):
        my_cells = cells[::]
        if len(clues) == 0:
            self.mark_cells(cells, 0, len(cells))
            return []

        for clue in clues:
            start, length = self.find_fill_run(my_cells)

            if length == clue.length:
                my_cells = my_cells[length + 1:]
            else:
                return [(clues, cells)]

        return []

