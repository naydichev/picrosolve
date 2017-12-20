class SequenceAnalyzer(object):
    def __init__(self, clues, cells):
        self._clues = clues
        self._cells = cells

        self._marks = 1 # hack to get the first loop to run
        self._fills = 0

    @property
    def clues(self):
        return self._clues

    @property
    def cells(self):
        return self._cells

    @property
    def marks(self):
        return self._marks

    @property
    def fills(self):
        return self._fills

    def reset(self):
        self._marks = 0
        self._fills = 0

    def process(self):
        seq_str = lambda x: u"".join([y.symbol for y in x])

        while self.fills + self.marks > 0:
            self.reset()
            self.process_sequence(self.clues, self.cells)

    def perform_on_cell_range(self, act, cells, start, stop):
        for i in range(max(0, start), min(stop, len(self.cells))):
            act(cells[i])

    def fill_sequence(self, cells, start, stop):
        def fill(cell):
            if not cell.filled:
                self._fills += 1
                cell.fill()

        self.perform_on_cell_range(fill, cells, start, stop)

    def mark_sequence(self, cells, start, stop):
        def mark(cell):
            if not cell.marked:
                self._marks += 1
                cell.mark()
        self.perform_on_cell_range(mark, cells, start, stop)

    def process_beginning_boundary(self, clues, cells):
        c = clues[0]
        self.fill_sequence(cells, 0, c.length)
        m = c.length

        if m > 0 and m < len(cells):
            cells[m].mark()

        return self.process_sequence(clues[1:], cells[m + 1:])

    def process_ending_boundary(self, clues, cells):
        c = clues[-1]
        self.fill_sequence(cells, len(cells) - c.length, len(cells))
        m = len(cells) - c.length - 1

        if m > 0 and m < len(cells):
            cells[m].mark()

        print(clues)
        print(u"".join([c.symbol for c in cells]))
        return self.process_sequence(clues[:-1], cells[:m])

    def get_run(self, cells, start):
        i = start
        count = 0
        while i < len(cells):
            if cells[i].filled:
                count += 1
            else:
                return count

            i += 1

    def find_run(self, cells, start=0):
        while start < len(cells):
            if cells[start].filled:
                return start, self.get_run(cells, start)

            start += 1
        return None, None

    def process_single_clue(self, clue, cells):
        if cells[0].filled:
            return self.process_beginning_boundary([clue], cells)
        elif cells[-1].filled:
            return self.process_ending_boundary([clue], cells)

        start, run_len = self.find_run(cells)

        print("> {} <".format(clue))
        print(u"".join([c.symbol for c in cells]))
        if start and run_len == clue.length:
            self.mark_sequence(cells, 0, start)
            self.mark_sequence(cells, start + run_len, len(cells))
            return
        elif start and run_len - start > 0:
            self.fill_sequence(cells, start, run_len)

    def process_sequence(self, clues, cells):
        if len(cells) == 0:
            return

        if len(clues) == 0:
            return self.mark_sequence(cells, 0, len(cells))

        i = 0
        while i < len(cells):
            cell = cells[i]
            if cell.filled:
                if i == 0:
                    return self.process_beginning_boundary(clues, cells)
                elif i + 1 == len(cells):
                    print(clues)
                    print(u"".join([c.symbol for c in cells]))
                    return self.process_ending_boundary(clues, cells)

                length = self.get_run(cells, i)

                if length == max([c.length for c in clues]):
                    self.mark_sequence(cells, i - 1, i)

                    mark_square = i + length + 1
                    if len(cells) < mark_square:
                        self.mark_sequence(cells, mark_square, mark_square + 1)
                        i = marks_square + 1
                        continue

                if i - clues[0].length < clues[0].length:
                    if length == clues[0].length:
                        mark_square = i + length + 1
                        print(
                            u"[clues: {}, length: {}, i: {}, cells: {}]".format(
                                clues,
                                length,
                                i,
                                u"".join([c.symbol for c in cells[slice(i - 1, mark_square + 1)]])
                            )
                        )
                        # mark before and after if possible
                        self.mark_sequence(cells, i - 1, i)
                        if len(cells) < mark_square:
                            self.mark_square(cells, mark_sequence, mark_square + 1)

                        return self.process_sequence(clues[1:], cells[mark_square + 1:])

            elif cell.marked:
                print(u"> {} <".format(cell.symbol))
                print(clues[0])
                print(i)
                if i > 0 and cells[i - 1].filled:
                    if clues[0] == i - 1:
                        self.fill_sequence(cells, 0, i - 1)

            i += 1
