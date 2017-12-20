from .cell import Cell, CellList
from .sequence import Sequence
from .printer import BoardPrinter

class Board(object):
    ROW = "row"
    COL = "column"

    def __init__(self, column_clues, row_clues):
        self._width = len(column_clues)
        self._height = len(row_clues)

        self._clues = {
            Board.COL: column_clues,
            Board.ROW: row_clues
        }

        self._cells = [[Cell(x, y) for x in range(self._width)] for y in range(self._height)]

    @property
    def clues(self):
        return self._clues

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def solved(self):
        for sequence in self.rows + self.cols:
            if not sequence.solved:
                return False

        return True

    @property
    def cells(self):
        return self._cells

    @property
    def rows(self):
        return list(map(
            Sequence,
            self.cells,
            self.clues[Board.ROW],
            [Board.ROW] * len(self.cells),
            range(len(self.cells))
        ))

    @property
    def cols(self):
        cell_inverse = list(zip(*self.cells))
        return list(map(
            Sequence,
            cell_inverse,
            self.clues[Board.COL],
            [Board.COL] * len(cell_inverse),
            range(len(cell_inverse))
        ))

    def __str__(self):
        return str(BoardPrinter(self))
