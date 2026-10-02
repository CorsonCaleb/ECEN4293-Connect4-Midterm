from abc import ABC, abstractmethod
import random

from perfect_solver import PerfectConnectFourSolver


class AbstractPlayer(ABC):
    def __init__(self, symbol, name):
        self.name = name
        self.symbol = symbol

    @abstractmethod
    def move(self, **kwargs):
        """Return the 0-based column where this player wants to move."""


class ConsolePlayer(AbstractPlayer):
    def move(self, **kwargs):
        """Get a move from a human player through the text console."""
        while True:
            try:
                return int(input("Enter which column to play in: "))
            except ValueError:
                print("Please enter a column number from 0 through 6.")


class CPUPlayer(AbstractPlayer):
    def move(self, **kwargs):
        """Select a random valid column automatically."""
        board = kwargs["board"]
        return random.choice(board.valid_columns())


class PerfectCPUPlayer(CPUPlayer):
    """CPU player that chooses an optimal move from an exact solver."""

    def __init__(self, symbol, name):
        super().__init__(symbol=symbol, name=name)
        self.solver = PerfectConnectFourSolver()

    def move(self, **kwargs):
        board = kwargs["board"]
        column = self.solver.best_move(board)
        print(f"{self.name} chooses column {column}.")
        return column
