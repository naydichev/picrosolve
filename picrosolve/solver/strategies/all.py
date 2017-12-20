from .edge import EdgeSolverStrategy
from .overlap import OverlapSolverStrategy
from .max_clue import MaxClueSolveStrategy

__ALL_STRATEGIES__ = [
    EdgeSolverStrategy,
    MaxClueSolveStrategy,
    OverlapSolverStrategy,
]

ALL_STRATEGIES = lambda debug=False: [ strat(debug) for strat in __ALL_STRATEGIES__ ]
