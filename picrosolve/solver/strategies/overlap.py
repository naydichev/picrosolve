from . import SolverStrategy

from picrosolve.game.cell import CellList
from picrosolve.decorators import memoize

class OverlapSolverStrategy(SolverStrategy):
    @property
    def name(self):
        return "Overlap"

    def should_attempt(self, clues, cells):
        return self.empty_overlap_likely(clues, cells) \
               or self.has_runs(clues, cells)

    def has_marks(self, cells):
        start, _ = self.find_mark_run(cells)

        return start is not None

    def has_runs(self, clues, cells):
        max_start, max_length = self.find_max(self.find_run, cells)

        self._p("max_start = {}; max_length = {}, min(clues) = {}".format(
            max_start, max_length, min(clues)
        ))
        return max_start and max_length > min(clues)

    def should_reverse(self, clues, cells):
        return self.should_attempt([c.length for c in clues], cells)

    def empty_overlap_likely(self, clues, cells):
        empty_cell_len = len([c for c in cells if c.empty])

        return empty_cell_len - sum(clues)  - len(clues) + 1 < max(clues)

    def _apply_strategy(self, clues, cells):
        new_clues = [c.length for c in clues]
        if not self.should_attempt(new_clues, cells):
            self._p("skipped")
            return [(clues, cells)]

        overlap = self.find_overlaps(
            self.generate_possible_sequences(new_clues, CellList(cells))
        )

        for i in range(len(overlap)):
            if overlap[i] == 1:
                self.fill_cells(cells, i)
            elif overlap[i] is not None:
                self.mark_cells(cells, i)

        return [(clues, cells)]

    @memoize
    def generate_possible_sequences(self, clues, cells):
        possible = []
        empty_likely = self.empty_overlap_likely(clues, cells)
        max_clue_start, max_clue_length = self.find_max(self.find_run, cells)
        max_clue_end = None
        if not empty_likely:
            max_clue_end = max_clue_start + max_clue_length

        def get_cell_state(cell):
            if cell.filled:
                return 1
            elif cell.marked:
                return 0
            else:
                return None

        current = [get_cell_state(cell) for cell in cells]

        def p(s, n, c, l=[]):
            if s == 0 and n == 0:
                possible.append(l)
                return
            elif s < 0 or n == 0:
                return
            elif max_clue_end and len(l) >= max_clue_end:
                possible.append(l + [None] * (len(current) - len(l)))
                return

            start = 1
            if len(l) == 0 or n == 1:
                start = 0

            for i in range(start, s + 1):
                next_poss = [0] * i
                my_c = c
                if my_c:
                    next_poss += [1] * my_c[0]
                    my_c = my_c[1:]

                if is_possible(next_poss, current[len(l):]):
                    p(s - i, n - 1, my_c, l + next_poss)

        def is_possible(l, section):
            for i in range(len(l)):
                if section[i] is not None:
                    if l[i] != section[i]:
                        return False

            return True

        w = len(cells)
        c = sum(clues)
        p(w - c, len(clues) + 1, clues)

        return possible

    def find_overlaps(self, possibles):
        def get_val(x):
            if all(x):
                return 1
            elif all([1 if z == 0 else 0 for z in x]):
                return 0
            else:
                return None
        return [get_val(x) for x in zip(*possibles)]
