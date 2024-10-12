class GameOfLife:
    def __init__(self, rows, cols):
        self.rows = int(rows)
        self.cols = int(cols)
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.initial_grid = [row[:] for row in self.grid]  # Keep track of the initial state

    def toggle_cell(self, row, col):
        self.grid[row][col] = 1 - self.grid[row][col]

    def reset(self):
        self.grid = [row[:] for row in self.initial_grid]

    def update(self):
        # Logic to update the grid for the next generation
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                live_neighbors = sum(self.grid[i][j]
                                     for i in range(max(0, row - 1), min(self.rows, row + 2))
                                     for j in range(max(0, col - 1), min(self.cols, col + 2))
                                     if (i != row or j != col))
                if self.grid[row][col] == 1 and live_neighbors in (2, 3):
                    new_grid[row][col] = 1
                elif self.grid[row][col] == 0 and live_neighbors == 3:
                    new_grid[row][col] = 1
        self.grid = new_grid

    def load_pattern(self, pattern, start_row, start_col):
        for r_offset, row in enumerate(pattern):
            for c_offset, cell in enumerate(row):
                if cell == 1:
                    self.grid[start_row + r_offset][start_col + c_offset] = 1
