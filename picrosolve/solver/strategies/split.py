from . import SolverStrategy

class SplitSolverStrategy(SolverStrategy):
    @property
    def name(self):
        return "Split"

    def _apply_strategy(self, clues, cells):
        if not len(clues):
            return [(clues, cells)]
#        start, length = self.find_mark_run(cells)
#
#        if start == clues[0].length and any([c.filled for c in cells[0:start]]):
#            self.fill_cells(cells, 0, clues[0].length)

        cells = self.strip_marks_from_edges(cells)

        return [(clues, cells)]
        # return self.strip_solved_clues(clues, cells)

    def strip_marks_from_edges(self, cells):
        start, length = self.find_mark_run(cells)

        while start is not None:
            if start == 0:
                cells = cells[length:]
            elif start + length == len(cells):
                cells = cells[:start]

            start, length = self.find_mark_run(cells, start + 1)

        return cells

    def strip_solved_clues(self, clues, cells):
        start, length = self.find_run(cells)
        while start is not None:
            if start == 0 or cells[start - 1].marked:
                if start + length == len(cells):
                    return []
                else:
                    # figure out which clue we are
                    my_clue = list(filter(lambda x: x.length == length, clues))


            start, length = self.find_run(cells, start + 1)
