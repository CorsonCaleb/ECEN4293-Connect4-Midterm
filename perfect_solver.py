"""Client for Pascal Pons's exact Connect Four solver.

The public solver evaluates every legal move under perfect play.  This module
converts the local 0-based move history to the solver's 1-based position
string and returns the highest-scoring legal move.

Source/algorithm background:
    https://connect4.gamesolver.org/
    https://github.com/PascalPons/connect4
"""

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class SolverUnavailableError(RuntimeError):
    """Raised when the exact online solver cannot be reached."""


class PerfectConnectFourSolver:
    """Use the gamesolver.org exact solver to choose an optimal move."""

    BASE_URL = "https://connect4.gamesolver.org/solve"
    CENTER_ORDER = (3, 4, 2, 5, 1, 6, 0)

    def __init__(self, timeout=15):
        self.timeout = timeout
        self._cache = {}

    @staticmethod
    def _position_string(move_history):
        """Convert 0-based local columns to the solver's 1-based format."""
        return "".join(str(col + 1) for col in move_history)

    def analyze(self, move_history):
        """Return the seven exact move scores for the supplied position."""
        position = self._position_string(move_history)

        if position in self._cache:
            return self._cache[position]

        query = urlencode({"pos": position})
        url = f"{self.BASE_URL}?{query}"
        request = Request(
            url,
            headers={"User-Agent": "OSU-ECEN4293-Connect4-Project/1.0"},
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as err:
            raise SolverUnavailableError(
                "Could not contact the perfect Connect Four solver. "
                "Check your internet connection and try again."
            ) from err

        scores = data.get("score")
        if not isinstance(scores, list) or len(scores) != 7:
            raise SolverUnavailableError(
                "The solver returned an unexpected response."
            )

        self._cache[position] = scores
        return scores

    def best_move(self, board):
        """Return the optimal legal 0-based column for the current player."""
        if board.num_rows != 6 or board.num_cols != 7:
            raise ValueError(
                "The perfect solver is designed for the standard 7x6 board."
            )

        valid_columns = board.valid_columns()
        if not valid_columns:
            raise ValueError("There are no valid moves remaining.")

        scores = self.analyze(board.move_history)
        best_score = max(scores[col] for col in valid_columns)

        # Prefer center-most columns when several moves have equal exact score.
        for col in self.CENTER_ORDER:
            if col in valid_columns and scores[col] == best_score:
                return col

        # This line should never be reached, but keeps the method total.
        return valid_columns[0]
