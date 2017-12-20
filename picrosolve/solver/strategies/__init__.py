from picrosolve.game.cell import CellList

class SolverStrategy(object):
    def __init__(self, debug=False):
        self._marks = 0
        self._fills = 0

        self.EMPTY = []

        self._repeats = {}

        self._debug = debug
        if debug:
            self.apply_strategy = self._apply_strategy_debug

    @property
    def name(self):
        raise NotImplementedError("You must implement this")

    @property
    def debug(self):
        return self._debug

    @property
    def marks(self):
        return self._marks

    @property
    def fills(self):
        return self._fills

    @property
    def repeats(self):
        return self._repeats

    def find_run(self, cells, start=0):
        is_filled = lambda x: x.filled
        return self._find_run(is_filled, cells, start)

    find_fill_run = find_run

    def find_mark_run(self, cells, start=0):
        is_marked = lambda x: x.marked
        return self._find_run(is_marked, cells, start)

    def find_empty_run(self, cells, start=0):
        is_empty = lambda x: x.empty
        return self._find_run(is_empty, cells, start)

    def _find_run(self, act, cells, start=0):
        for i in range(start, len(cells)):
            if act(cells[i]):
                return i, self._get_run(act, cells, i)
        return None, None

    def find_max(self, find_func, cells):
        max_run = (None, None)
        start = 0
        length = 0

        while start is not None:
            start, length = find_func(cells, start + length)

            if start:
                if not max_run[1] or length > max_run[1]:
                    max_run = (start, length)

        return max_run

    def get_run(self, cells, start=0):
        is_filled = lambda x: x.filled
        return self._get_run(is_filled, cells, start)

    get_fill_run = get_run

    def get_mark_run(self, cells, start=0):
        is_marked = lambda x: x.marked
        return self._get_run(is_marked, cells, start)

    def _get_run(self, act, cells, start=0):
        length = 0
        for i in range(start, len(cells)):
            if act(cells[i]):
                length += 1
            else:
                break
        return length

    def mark_cells(self, cells, start, n=1):
        def _mark(cell):
            if not cell.marked:
                cell.mark()
                self._marks += 1

        self._perform_on_cells(_mark, cells, start, n)

    def fill_cells(self, cells, start, n=1):
        def _fill(cell):
            if not cell.filled:
                cell.fill()
                self._fills += 1

        self._perform_on_cells(_fill, cells, start, n)

    def _perform_on_cells(self, act, cells, start, n):
        while n > 0:
            if start < 0 or start >= len(cells):
                break
            act(cells[start])
            start += 1
            n -= 1

    def _p(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def _apply_strategy_debug(self, clues, cells):
        print("#" * 40)
        print("Strategy {}; Clues: {}".format(self.name, clues))
        print(u"Before: {}".format(CellList(cells)))

        result = self._apply_strategy_normal(clues, cells)

        print(u"After:  {}".format(CellList(cells)))
        print("Result ({}): ".format(len(result)))
        for row in result:
            print("\tClues: {}, Cells: {}".format(row[0], CellList(row[1])))
        print("%" * 40)

        return result

    def should_reverse(self, clues, cells):
        return True

    def _apply_strategy_normal(self, clues, cells):
        def should_process(seq):
            if len(seq[0]) == 0:
                self.mark_cells(seq[1], 0, len(seq[1]))
                return False

            if len(seq[0]) == 1:
                start, length = self.find_run(seq[1])
                if start == 0 and len(seq[1]) == length:
                    assert seq[0][0].length == length
                    return False

            return True

        forward_result = self._apply_strategy(clues, cells)
        if not self.should_reverse(clues, cells):
            return forward_result

        reverse_result = []
        for row in forward_result:
            if should_process(row):
                reverse_result.extend(
                    self._apply_strategy(
                        list(reversed(row[0])),
                        list(reversed(row[1]))
                    )
                )

        result = []
        for row in reverse_result:
            if should_process(row):
                result.append((
                    list(reversed(row[0])),
                    list(reversed(row[1]))
                ))

        s = u"|".join([str(c.length) for c in clues]) + u"#" + str(CellList(cells))
        n = self.repeats.get(s, 0)
        self.repeats[s] = n + 1
        if n % 5 == 0 and n > 0:
            self._p("Repeated this sequence {} times.".format(n))

        return result

    apply_strategy = _apply_strategy_normal

    def _apply_strategy(self, clues, cells):
        raise NotImplementedError("You must implement this")
