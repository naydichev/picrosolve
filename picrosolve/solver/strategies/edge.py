from . import SolverStrategy

class EdgeSolverStrategy(SolverStrategy):
    @property
    def name(self):
        return "Edge"

    def _apply_strategy(self, clues, cells):
        if not len(clues) or not len(cells):
            return [(clues, cells)]

        return self.handle_edge(clues, cells)

    def handle_edge(self, clues, cells):
        first_clue = clues[0]
        fcl = first_clue.length
        my_cells = cells[::]

        while my_cells[0].marked:
            my_cells.pop(0)

        start, length = self.find_run(my_cells)
        if start is None:
            return [(clues, my_cells)]

        if start == 0:
            self.fill_cells(my_cells, 0, fcl)
            self.mark_cells(my_cells, fcl)

            clues = clues[1:]
            my_cells = my_cells[fcl + 1:]

            if len(clues):
                return self.handle_edge(clues, my_cells)

        elif start <= fcl:
            self.fill_cells(my_cells, start, fcl - start)
            mstart, mlength = self.find_mark_run(my_cells, start)

            if mstart and mstart - start - length == 0:
                mstart - length
                self.fill_cells(my_cells, mstart - fcl, fcl)
                self.mark_cells(my_cells, 0, mstart - fcl)
                clues = clues[1:]
                my_cells = my_cells[mstart + 1:]
            elif fcl == 1:
                self.mark_cells(my_cells, 0, start)
                self.mark_cells(my_cells, start + fcl)
                clues = clues[1:]
                my_cells = my_cells[start + fcl + 1:]

        return [(clues, my_cells)]
