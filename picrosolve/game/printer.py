class BoardPrinter(object):
    def __init__(self, board):
        self._board = board

    @property
    def board(self):
        return self._board

    def __str__(self):
        board = self.board
        row_len = max([
            sum(map(lambda x: len(str(x)) + 1, seq.clues))
            for seq in board.rows
        ])

        p_width = (board.width * 3) + row_len + 3
        col_height = max([len(seq.clues) for seq in board.cols])
        whole_line = u"-" * p_width
        row_fmt = u"|{{row_contents:>{row_len}}}|{{cells}}|\n".format(row_len=row_len)

        rendered_str = whole_line + u"\n"
        col_line_start = u"|" + u" " * row_len + u"|"

        cols = []
        # build this in reverse
        for col_row_index in range(col_height):
            row = col_line_start
            for seq in board.cols:
                col = list(reversed(seq.clues))
                value = u"  "
                if col_row_index < len(col):
                    value = u"{:>2}".format(col[col_row_index].length)

                row += value + u"|"

            cols.append(row)

        rendered_str += u"\n".join(reversed(cols))
        rendered_str += u"\n" + whole_line + u"\n"

        for row in board.rows:
            row_contents = u" ".join([str(clue) for clue in row.clues])
            rendered_str += row_fmt.format(
                row_contents=row_contents,
                cells=row.cells
            )

        rendered_str += whole_line

        return rendered_str
