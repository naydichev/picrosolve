import signal
import sys
import time
from collections import deque
import traceback

from picrosolve.game.cell import CellList

from .strategies.all import ALL_STRATEGIES

class Solver(object):
    def __init__(self, board, strategies=None, debug=False):
        self._board = board

        if not strategies:
            strategies = ALL_STRATEGIES(debug)

        self._strategies = strategies
        self._queue = deque()
        self._debug = debug
        self.working = None
        self.working_strat_name = None

    @property
    def board(self):
        return self._board

    @property
    def strategies(self):
        return self._strategies

    @property
    def queue(self):
        return self._queue

    @property
    def debug(self):
        return self._debug

    def dump_status(self, message):
        self.print_status(message)
        print("=== Dumping Queue ===")
        for seq in self.queue:
            print(u"> Clues: {}, Cells: {}".format(seq[0], CellList(seq[1])))

        if self.working:
            print(u"> Working Strategy: {}, Clue: {}, Cells: {}".format(self.working_strat_name, self.working[0], CellList(self.working[1])))

    def solve(self):
        signal.signal(
            signal.SIGUSR1,
            lambda x, y: self.dump_status(signal.getsignal(x))
        )
        signal.signal(
            signal.SIGUSR2,
            lambda x, y: print(x, y)
        )

        try:
            self._solve()
        except (Exception, KeyboardInterrupt) as e:
            self.dump_status("Caught Exception")
            print(str(e))
            traceback.print_tb(sys.exc_info()[2])

    def d(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def _solve(self):
        all_sequences = self.board.rows + self.board.cols
        solved_sequences = lambda: sum([1 if seq.solved else 0 for seq in all_sequences])
        solved_l = len(all_sequences)
        solved = lambda: (solved_sequences() - solved_l) == 0

        self.queue.extend([(s.clues, s.cells) for s in all_sequences])

        while len(self.queue) > 0:
            self.d("Queue depth: {}".format(len(self.queue)))
            self.working = self.queue.popleft()

            for strat in self.strategies:
                self.working_strat_name = strat.name
                new_seqs = strat.apply_strategy(*self.working)

                if len(new_seqs):
                    self.working = new_seqs[0]
                    if len(new_seqs) > 1:
                        self.queue.extend(new_seqs[1:])
                else:
                    self.working = None
                    self.working_strat_name = None
                    break

            if self.working:
                self.queue.append(self.working)

        if solved():
            self.d("Queue: ")
            for row in self.queue:
                self.d(">> Clues: {}, Cells: {}".format(row[0], CellList(row[1])))
        self.print_status("Solved")

    def print_status(self, message):
        solved = sum([1 if s.solved else 0 for s in self.board.rows + self.board.cols])
        len_seq = len(self.board.rows) + len(self.board.cols)

        print(" ==== {} ====".format(message))
        print(self.board)
        print("There are {}/{} solved sequences".format(solved, len_seq))
