from .cell import CellList


class Sequence(object):
    ROW = "row"
    COL = "col"
    def __init__(self, list_of_cells, cluelist, dimension, coordinate):
        self._cells = CellList(list_of_cells)
        self._clues = cluelist
        self._dimension = dimension
        self._coordinate = coordinate

    @property
    def cells(self):
        return self._cells

    @property
    def clues(self):
        return self._clues

    @property
    def dimension(self):
        return self._dimension

    @property
    def coordinate(self):
        return self._coordinate

    def fill_cell(self, index):
        self.cells[index].fill()

    def mark_cell(self, index):
        self.cells[index].mark()

    @property
    def runs(self):
        runs = []
        filled_count = 0
        for cell in self.cells:
            if cell.filled:
                filled_count +=1
            if filled_count and cell.marked:
                runs.append(filled_count)
                filled_count = 0

        if filled_count:
            runs.append(filled_count)

        return runs

    @property
    def solved(self):
        if len(self.runs) != len(self.clues):
            return False

        for i in range(len(self.runs)):
            if self.runs[i] != self.clues[i].length:
                return False

        return True

    def __str__(self):
        return str(dict(
            clues=self.clues,
            dimension=self.dimension,
            coordinate=self.coordinate,
            solved=self.solved,
            cells=u"".join([cell.symbol for cell in self.cells]),
        )).encode("utf-8")

    __repr__ = __str__
