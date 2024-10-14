from random import randint


class GameOfLife:
    """The GameOfLife class simulates Conway's Game of Life.

    Attributes:
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        grid (list of lists): The current grid representing
        the state of the game.
        r_range (tuple): Range of rows where cells are alive.
        c_range (tuple): Range of columns where cells are alive.
    """

    def __init__(self, rows, cols):
        """Initializes the GameOfLife with a grid of dead cells.

        Args:
            rows (int): Number of rows in the grid.
            cols (int): Number of columns in the grid.
        """
        self.rows = rows
        self.cols = cols
        self.reset_range()
        self.grid = self.create_grid()

    def create_grid(self):
        """Creates an empty grid (all cells dead).

        Returns:
            list of lists: A grid with all cells set to 0 (dead).
        """
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def reset_range(self):
        """Resets the row and column range of the live cells."""
        self.r_range = (0, self.rows)
        self.c_range = (0, self.cols)

    def update_game_grid(self, canvas):
        """Updates the game grid on the canvas by checking
        which cells should change.

        Args:
            canvas: The canvas on which the game grid is drawn.

        Returns:
            list: A list of cells that have changed state.
        """
        range_d = self.get_matrix_range(self.rows, self.cols)
        if not range_d:
            return None
        new = []
        rs = range_d["top"]
        re = range_d["bottom"]
        cs = range_d["left"]
        ce = range_d["right"]
        if rs > 0:
            rs -= 1
        if re < self.rows - 1:
            re += 1
        if cs > 0:
            cs -= 1
        if ce < self.cols - 1:
            ce += 1
        for r in range(rs, re + 1):
            for c in range(cs, ce + 1):
                alive_neighbors = self.count_alive_neighbors(r, c)
                if self.grid[r][c] == 1:
                    if alive_neighbors not in (2, 3):
                        new.append((r, c, 0))
                    else:
                        canvas.canvas.itemconfig(
                            canvas.cells[r][c], fill="#ff00e8")
                # Cell is dead and has exactly 3 neighbors
                elif self.grid[r][c] == 0 and alive_neighbors == 3:
                    new.append((r, c, 1))
        return new

    def count_alive_neighbors(self, row, col):
        """Counts the number of alive neighbors for a given cell.

        Args:
            row (int): Row index of the cell.
            col (int): Column index of the cell.

        Returns:
            int: Number of alive neighbors.
        """
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for d in directions:
            r, c = row + d[0], col + d[1]
            if 0 <= r < self.rows and 0 <= c < self.cols:
                count += self.grid[r][c]
        return count

    def reset(self):
        """Resets the grid to an all-dead state."""
        self.grid = self.create_grid()

    def load_pattern(self, pattern, rows, cols):
        """Loads a pattern into the center of the grid.

        Args:
            pattern (list of lists): A 2D pattern to be placed in the grid.
            rows (int): Number of rows in the grid.
            cols (int): Number of columns in the grid.
        """
        if not pattern:
            return
        patt_rows = len(pattern)
        patt_cols = len(pattern[0])

        row_start = (rows // 2) - (patt_rows // 2)
        col_start = (cols // 2) - (patt_cols // 2)

        for row_n, row in enumerate(pattern):
            for col_n, cell in enumerate(row):
                if cell == 1:
                    self.grid[row_start + row_n][col_start + col_n] = 1

    def get_matrix_range(self, rows, cols):
        """Gets the range of the grid that contains live cells.

        Args:
            rows (int): Number of rows in the grid.
            cols (int): Number of columns in the grid.

        Returns:
            dict or None: A dictionary containing the range of rows and columns
                          where live cells are located,
                          or None if no live cells exist.
        """
        self.matrix_range = {"top": -1, "bottom": -1, "left": -1, "right": -1}

        for r in range(rows):
            if 1 in self.grid[r]:
                self.matrix_range["top"] = r
                break

        for r in range(rows - 1, -1, -1):
            if 1 in self.grid[r]:
                self.matrix_range["bottom"] = r
                break

        if self.matrix_range["top"] == -1 or self.matrix_range["bottom"] == -1:
            return None

        self.matrix_range["left"] = self.grid[self.matrix_range["top"]].index(
            1)
        for r in range(
                self.matrix_range["top"] + 1,
                self.matrix_range["bottom"] + 1):
            try:
                index = self.grid[r].index(1)
                if index < self.matrix_range["left"]:
                    self.matrix_range["left"] = index
            except ValueError:
                continue

        for r in range(
                self.matrix_range["top"],
                self.matrix_range["bottom"] + 1):
            for c in range(cols - 1, self.matrix_range["left"] - 1, -1):
                if self.grid[r][c] == 1 and c > self.matrix_range["right"]:
                    self.matrix_range["right"] = c
                    break
        return self.matrix_range
