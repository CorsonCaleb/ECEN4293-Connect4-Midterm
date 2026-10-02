import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

from board import InvalidMoveError
from player import CPUPlayer
from perfect_solver import SolverUnavailableError


class MatplotlibGame:
    """Display and control the Connect Four game using matplotlib."""

    def __init__(self, board, player_1, player_2):
        self.board = board
        self.player_1 = player_1
        self.player_2 = player_2
        self.current_player = self.player_1
        self.game_over = False

        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.draw_board()

    def draw_board(self):
        """Draw the current board state."""
        self.ax.clear()

        rows = self.board.num_rows
        cols = self.board.num_cols

        self.ax.set_xlim(0, cols)
        self.ax.set_ylim(0, rows)
        self.ax.set_aspect("equal")

        board_rect = Rectangle(
            (0, 0), cols, rows, facecolor="blue"
        )
        self.ax.add_patch(board_rect)

        for row in range(rows):
            for col in range(cols):
                symbol = self.board.rows[row][col]
                y = rows - row - 1

                if symbol == self.player_1.symbol:
                    piece_color = "red"
                elif symbol == self.player_2.symbol:
                    piece_color = "yellow"
                else:
                    piece_color = "white"

                piece = Circle(
                    (col + 0.5, y + 0.5),
                    0.4,
                    facecolor=piece_color,
                    edgecolor="black",
                )
                self.ax.add_patch(piece)

        self.ax.set_xticks([col + 0.5 for col in range(cols)])
        self.ax.set_xticklabels([str(col) for col in range(cols)])
        self.ax.set_yticks([])

        if not self.game_over:
            if isinstance(self.current_player, CPUPlayer):
                instruction = "CPU is choosing a move..."
            else:
                instruction = "Click a column to place your piece"

            self.ax.set_title(
                f"{self.current_player.name}'s turn "
                f"({self.current_player.symbol})\n{instruction}"
            )

        self.fig.canvas.draw_idle()

    def on_click(self, event):
        """Handle a mouse click on the board."""
        if self.game_over or event.xdata is None:
            return

        if isinstance(self.current_player, CPUPlayer):
            return

        column = int(event.xdata)
        if column < 0 or column >= self.board.num_cols:
            return

        try:
            self.board.add_piece(column, self.current_player.symbol)
        except InvalidMoveError as err:
            self.ax.set_title(f"{err}\nClick another column.")
            self.fig.canvas.draw_idle()
            return

        self.finish_turn()

    def finish_turn(self):
        """Check game status and advance to the next player."""
        if self.board.check_winner():
            self.game_over = True
            self.draw_board()
            self.ax.set_title(f"{self.current_player.name} wins!")
            self.fig.canvas.draw_idle()
            return

        if self.board.is_full():
            self.game_over = True
            self.draw_board()
            self.ax.set_title("No winner!")
            self.fig.canvas.draw_idle()
            return

        if self.current_player == self.player_1:
            self.current_player = self.player_2
        else:
            self.current_player = self.player_1

        self.draw_board()

        if isinstance(self.current_player, CPUPlayer):
            plt.pause(0.15)
            self.cpu_move()

    def cpu_move(self):
        """Allow a CPU player to automatically choose a column."""
        if self.game_over:
            return

        try:
            column = self.current_player.move(board=self.board)
            self.board.add_piece(column, self.current_player.symbol)
        except SolverUnavailableError as err:
            self.game_over = True
            self.ax.set_title(str(err))
            self.fig.canvas.draw_idle()
            return
        except InvalidMoveError:
            return

        self.draw_board()
        plt.pause(0.15)
        self.finish_turn()

    def start(self):
        """Start the matplotlib version of the game."""
        self.board.clear()
        self.current_player = self.player_1
        self.game_over = False
        self.draw_board()

        if isinstance(self.current_player, CPUPlayer):
            plt.pause(0.25)
            self.cpu_move()

        plt.show()
