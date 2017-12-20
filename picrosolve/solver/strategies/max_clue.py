from . import SolverStrategy

class MaxClueSolveStrategy(SolverStrategy):
    @property
    def name(self):
        return "MaxClues"

    def _apply_strategy(self, clues, cells):
        start, length = self.find_max_run(cells)

        if not start or not len(clues):
            return [(clues, cells)]

        max_clue_length = max([c.length for c in clues])

        max_clues = list(filter(lambda x: x.length == max_clue_length, clues))
        max_clue_count = len(max_clues)
        next_list = [c.length for c in clues if c.length != max_clue_length]
        next_max = None if not len(next_list) else max(next_list)

        if max_clue_length == length:
            self.mark_cells(cells, start - 1, 1)
            self.mark_cells(cells, start + length, 1)

            left_distance = start - 1
            right_distance = len(cells) - start + length + 1

            if max_clue_count == 1:
                left_clues, right_clues = self.split_clues(clues, max_clue_length)
                max_clue_index = clues.index(max_clues[0])
                left_cells = cells[0 : start - 1]
                right_cells = cells[start + length + 1 :]

                result = []
                if len(left_cells):
                    result.append((left_clues, left_cells))
                if len(right_cells):
                    result.append((right_clues, right_cells))

                return result
        elif next_max and length > next_max:
            # our run is for this, it's just not complete yet
            # check for a mark on either side?
            split = False
            l_end = r_start = None
            if start == 0 or cells[start - 1].marked:
                self.fill_cells(cells, start, max_clue_length)
                self.mark_cells(cells, start + max_clue_length)
                split = True
                l_end = start
                r_start = start + max_clue_length + 1
            elif len(cells) == start + length or cells[start + length].marked:
                a_start = start + length - max_clue_length
                self.fill_cells(cells, a_start, max_clue_length)
                self.mark_cells(cells, a_start - 1)
                split = True
                l_end = a_start
                r_start = start + length

            if max_clue_length == 1 and split:
                left_clues, right_clues = self.split_clues(clues, max_clue_length)
                left_cells = cells[:l_end]
                right_cells = cells[r_start:]

                result = []
                if len(left_cells):
                    result.append((left_clues, left_cells))
                if len(right_cells):
                    result.append((right_clues, right_cells))

                return result

        return [(clues, cells)]

    def split_clues(self, clues, clue_val):
        clue_idx = None
        for i in range(len(clues)):
            if clues[i].length == clue_val:
                clue_idx = i
                break
        return clues[:clue_idx], clues[clue_idx + 1:]

    def find_all_runs(self, cells):
        runs = []
        start, length = self.find_run(cells)

        while start is not None:
            runs.append((start, length))

            start = start + length + 1

            start, length = self.find_run(cells, start)

        return runs

    def find_max_run(self, cells):

        runs = self.find_all_runs(cells)

        if not runs:
            return None, None

        max_run = runs.pop(0)

        for run in runs:
            if run[1] > max_run[1]:
                max_run = run

        return max_run
