from collections.abc import Sequence

class Cell(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._filled = False
        self._marked = False

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def filled(self):
        return self._filled

    def fill(self):
        if self.marked:
            raise ValueError("Cell is already marked, cannot fill")
        self._filled = True

    @property
    def marked(self):
        return self._marked

    def mark(self):
        if self.filled:
            raise ValueError("Cell is already filled, cannot mark")
        self._marked = True

    @property
    def empty(self):
        return not (self.filled or self.marked)

    @property
    def symbol(self):
        if self.filled:
            return u"\u2b1b"
        elif self.marked:
            return u"\u274c"
        else:
            return u"\u2b1c"

    def __hash__(self):
        return hash((self.x, self.y, self.symbol))

    def __str__(self):
        return self.symbol

class CellList(Sequence):
    def __init__(self, init=[]):
        self.sequence = list(init)

    def __getitem__(self, k):
        if isinstance(k, slice):
            return CellList(self.sequence[k])

        return self.sequence[k]

    def __len__(self):
        return len(self.sequence)

    def __str__(self):
        return u"{}".format(u"|".join([c.symbol for c in self.sequence]))

    def pop(self, i=-1):
        return self.sequence.pop(i)
