from . import SolverStrategy

class EmptySolverStrategy(SolverStrategy):
    @property
    def name(self):
        return "Empty"

    def _apply_strategy(self, clues, cells):
        if not len(clues):
            self.mark_cells(cells, 0, len(cells))
            return []

        min_clue = min([c.length for c in clues])
        if min_clue == 1:
            return [(clues, cells)]

        start, length = self.find_empty_run(cells)
        while start is not None:
            if length < min_clue:
                if (start == 0 or cells[start - 1].marked) and (
                   start + length == len(cells) or cells[start + length].marked):
                    self.mark_cells(cells, start, length)

            start, length = self.find_empty_run(cells, start + length)
        return [(clues, cells)]
