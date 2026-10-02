_EMPTY = " "  # Used to indicate empty spaces in the board


class InvalidMoveError(ValueError):
    """Raised when a player attempts an invalid Connect Four move."""


class ConnectFourBoard:
    """Represent a Connect Four board and its move history."""

    def __init__(self, num_rows=6, num_cols=7):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.clear()

    def clear(self):
        """Replace all pieces with empty spaces and reset move history."""
        self.rows = [
            [_EMPTY for _ in range(self.num_cols)]
            for _ in range(self.num_rows)
        ]
        self.move_history = []

    def display(self):
        """Display the current board state in the console."""
        for row in range(self.num_rows):
            print(f'\t|{"|".join(self.rows[row])}|')

        print("\t " + " ".join(str(col) for col in range(self.num_cols)))

    def check_winner(self):
        """Return True when any player has four connected pieces."""
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                symbol = self.rows[row][col]

                if symbol == _EMPTY:
                    continue

                # Horizontal
                if col <= self.num_cols - 4:
                    if all(
                        self.rows[row][col + offset] == symbol
                        for offset in range(1, 4)
                    ):
                        return True

                # Vertical
                if row <= self.num_rows - 4:
                    if all(
                        self.rows[row + offset][col] == symbol
                        for offset in range(1, 4)
                    ):
                        return True

                # Diagonal down-right
                if row <= self.num_rows - 4 and col <= self.num_cols - 4:
                    if all(
                        self.rows[row + offset][col + offset] == symbol
                        for offset in range(1, 4)
                    ):
                        return True

                # Diagonal up-right
                if row >= 3 and col <= self.num_cols - 4:
                    if all(
                        self.rows[row - offset][col + offset] == symbol
                        for offset in range(1, 4)
                    ):
                        return True

        return False

    def is_full(self):
        """Return True when there are no playable cells remaining."""
        return all(cell != _EMPTY for cell in self.rows[0])

    def valid_columns(self):
        """Return a list of columns that can accept another piece."""
        return [
            col
            for col in range(self.num_cols)
            if self.rows[0][col] == _EMPTY
        ]

    def add_piece(self, col, symbol):
        """Drop a piece into a column and record the move."""
        if col < 0 or col >= self.num_cols:
            raise InvalidMoveError("Column is outside the board.")

        if self.rows[0][col] != _EMPTY:
            raise InvalidMoveError("That column is full.")

        for row in reversed(range(self.num_rows)):
            if self.rows[row][col] == _EMPTY:
                self.rows[row][col] = symbol
                self.move_history.append(col)
                return
