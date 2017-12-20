from . import SolverStrategy

class FewCluesSolverStrategy(SolverStrategy):
    @property
    def name(self):
        return "FewClues"

    def _apply_strategy(self, clues, cells):
        clue_len = len(clues)
        if clue_len == 0:
            return self.zero_clues(clues, cells)
        elif clue_len == 1:
            return self.one_clue(clues, cells)
        elif clue_len == 2:
            return self.two_clues(clues, cells)

        return [(clues, cells)]

    def zero_clues(self, clues, cells):
        self.mark_cells(cells, 0, len(cells))

        return self.EMPTY

    def one_clue(self, clues, cells):
        clue = clues[0]
        start, length = self.find_run(cells)

        if start:
            if length == clue.length:
                self.mark_cells(cells, 0, start)
                self.mark_cells(cells, start + length, len(cells))
                return []

            diff = clue.length - length
            poss_start = max(0, start - diff)
            poss_end = min(len(cells), start + clue.length)

            self.mark_cells(cells, 0, poss_start)
            self.mark_cells(cells, poss_end, len(cells) - poss_end)
            self.fill_cells(cells, start, length - diff)

            return [(clues, cells[poss_start:poss_end])]

        return [(clues, cells)]

    def two_clues(self, clues, cells):
        return [(clues, cells)]
