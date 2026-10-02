from board import ConnectFourBoard, InvalidMoveError
from matplotdisplayLab02 import MatplotlibGame
from perfect_solver import SolverUnavailableError
from player import ConsolePlayer, CPUPlayer, PerfectCPUPlayer


class ConnectFourGame:
    """Represent a Connect Four game and manage its players."""

    def __init__(
        self,
        rows=6,
        cols=7,
        p1_type=ConsolePlayer,
        p2_type=ConsolePlayer,
    ):
        self.board = ConnectFourBoard(rows, cols)

        p1_symbol = self.get_player_symbol("Player 1")
        p2_symbol = self.get_player_symbol("Player 2")

        while p2_symbol == p1_symbol:
            print("Player 2 can't have the same symbol as Player 1!")
            p2_symbol = self.get_player_symbol("Player 2")

        self.player_1 = p1_type(name="Player 1", symbol=p1_symbol)
        self.player_2 = p2_type(name="Player 2", symbol=p2_symbol)
        self.turn = 0

    def start(self):
        """Play a new console game."""
        self.board.clear()
        self.turn = 0

        while not self.board.is_full():
            if self.turn % 2 == 0:
                current_player = self.player_1
            else:
                current_player = self.player_2

            print(f"{current_player.name}'s turn.")
            self.board.display()

            move_is_invalid = True
            while move_is_invalid:
                try:
                    col = current_player.move(board=self.board)
                    self.board.add_piece(col, current_player.symbol)
                    move_is_invalid = False
                except InvalidMoveError as err:
                    print(err)
                except SolverUnavailableError as err:
                    print(err)
                    return

            self.turn += 1

            if self.board.check_winner():
                self.board.display()
                print(f"{current_player.name} wins!")
                return

        self.board.display()
        print("No winner!")

    @staticmethod
    def get_player_symbol(player_name):
        """Request a valid one-character symbol for a player."""
        while True:
            symbol = input(
                f"Enter a character to use as a symbol for {player_name}: "
            ).strip()

            if not symbol:
                print("Symbol must not be a whitespace character!")
                continue

            symbol = symbol[0]
            confirmation = input(
                f'Use "{symbol}" for {player_name}? (y/N): '
            )

            if confirmation.lower().startswith("y"):
                return symbol


def choose_game_mode():
    """Return the two player classes selected by the user."""
    print("Choose game mode:")
    print("1. Human vs Human")
    print("2. Human vs Random CPU")
    print("3. Human vs Perfect CPU")
    print("4. Perfect CPU vs Perfect CPU")

    choice = input("Select game mode (1-4): ")
    while choice not in ("1", "2", "3", "4"):
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
        choice = input("Select game mode (1-4): ")

    modes = {
        "1": (ConsolePlayer, ConsolePlayer),
        "2": (ConsolePlayer, CPUPlayer),
        "3": (ConsolePlayer, PerfectCPUPlayer),
        "4": (PerfectCPUPlayer, PerfectCPUPlayer),
    }
    return modes[choice]


def choose_display_mode():
    """Ask whether to display the board in the console or matplotlib."""
    print()
    print("Choose display mode:")
    print("1. Console")
    print("2. Matplotlib")

    choice = input("Select display mode (1 or 2): ")
    while choice not in ("1", "2"):
        print("Invalid choice. Please enter 1 or 2.")
        choice = input("Select display mode (1 or 2): ")

    return choice


if __name__ == "__main__":
    p1_type, p2_type = choose_game_mode()
    display_mode = choose_display_mode()

    game = ConnectFourGame(p1_type=p1_type, p2_type=p2_type)

    if display_mode == "1":
        keep_playing = True
        while keep_playing:
            game.start()
            keep_playing = input(
                "Play again? (y/N): "
            ).lower().startswith("y")
    else:
        matplotlib_game = MatplotlibGame(
            game.board,
            game.player_1,
            game.player_2,
        )
        matplotlib_game.start()
