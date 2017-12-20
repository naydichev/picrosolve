import sys
import re
import argparse
import pprint

import picrosolve.game.clues as clues
from picrosolve.game.board import Board
from picrosolve.solver import Solver

def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        prog="picrosolve",
        description="picross cli app"
    )
    parser.add_argument("mode", choices=["print", "solve", "play", "board"])
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("clues", type=argparse.FileType("r"))

    args = parser.parse_args(args)

    row_clues, col_clues = parse_clues(args.clues)

    board = Board(col_clues, row_clues)

    if args.mode == "board":
        return board
    elif args.mode == "print":
        print(board)
    elif args.mode == "solve":
        solver = Solver(board, debug=args.debug)
        solver.solve()
    elif args.mode == "play":
        print("{} coming soon!".format(args.mode))
        print("for now, enjoy this puzzle ")
        print(board)

def parse_clues(clues_file):
    rows = []
    cols = []

    ROW_MODE = "ROW"
    COL_MODE = "COL"
    mode = None
    for line in clues_file:
        line = line.strip()
        if not len(line) or not line:
            continue

        match = re.search("\[(\w+)\]", line)
        if match:
            if match.group(1) in ["rows", "ROWS"]:
                mode = ROW_MODE
            elif match.group(1) in ["cols", "COLS", "columns", "COLUMNS"]:
                mode = COL_MODE
            else:
                raise ValueError("Unsupported mode: {}".format(match.group(1)))

            continue


        parsed_clues = clues.ClueList([clues.Clue(int(item)) for item in re.split("\W+", line.strip())])
        if mode is ROW_MODE:
            rows.append(parsed_clues)
        elif mode is COL_MODE:
            cols.append(parsed_clues)
        else:
            raise ValueError("Mode is not set, invalid config file. Bad line: {}".format(line))

    return rows, cols
