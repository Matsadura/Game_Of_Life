from random import randint
class GameOfLife:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.reset_range()
        self.grid = self.create_grid()
        self.alive_cells = set()

    def create_grid(self):
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        # return [[randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]

    def toggle_cell(self, row, col):
        self.grid[row][col] = 1 - self.grid[row][col]

    def update(self):
        new_grid = self.create_grid()
        for r in range(self.rows):
            for c in range(self.cols):
                alive_neighbors = self.count_alive_neighbors(r, c)
                if self.grid[r][c] == 1:  # Cell is alive
                    new_grid[r][c] = 1 if alive_neighbors in (2, 3) else 0
                else:  # Cell is dead
                    new_grid[r][c] = 1 if alive_neighbors == 3 else 0
        self.grid = new_grid

    def reset_range(self):
        self.r_range = (0, self.rows)
        self.c_range = (0, self.cols)

    def update_game_grid(self, canvas):
        # TODO: add a start and end points in grid update
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
                if self.grid[r][c] == 1:  # Cell is alive and has too few or too many neighbors
                    if alive_neighbors not in (2, 3):
                        new.append((r, c, 0))
                    else:
                        canvas.canvas.itemconfig(canvas.cells[r][c], fill="#ff00e8")
                elif self.grid[r][c] == 0 and alive_neighbors == 3:  # Cell is dead and has exactly 3 neighbors
                    new.append((r, c, 1))
        return new

    # def update_game_grid(self):
    #     # new_grid = self.create_grid()
    #     # TODO: add a start and end points in grid update
    #     new = []
    #     for r in range(self.rows):
    #         for c in range(self.cols):
    #             alive_neighbors = self.count_alive_neighbors(r, c)
    #             if self.grid[r][c] == 1 and alive_neighbors not in (2, 3):  # Cell is alive and has too few or too many neighbors
    #                 new.append((r, c, 0))
    #             elif self.grid[r][c] == 0 and alive_neighbors == 3:  # Cell is dead and has exactly 3 neighbors
    #                 new.append((r, c, 1))
    #     return new

    def count_alive_neighbors(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for d in directions:
            r, c = row + d[0], col + d[1]
            if 0 <= r < self.rows and 0 <= c < self.cols:
                count += self.grid[r][c]
        return count

    def reset(self):
        self.grid = self.create_grid()

    def load_pattern(self, pattern, rows, cols):
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
        self.matrix_range = {"top": -1, "bottom": -1, "left": -1, "right": -1}

        for r in range(rows):
            if 1 in self.grid[r]:
                self.matrix_range["top"] = r
                break

        for r in range(rows - 1, -1, -1):
            if 1 in self.grid[r]:
                self.matrix_range["bottom"] = r
                break

        if  self.matrix_range["top"] == -1 or self.matrix_range["bottom"] == -1:
            return None

        self.matrix_range["left"] = self.grid[self.matrix_range["top"]].index(1)
        for r in range(self.matrix_range["top"] + 1, self.matrix_range["bottom"] + 1):
            try:
                index = self.grid[r].index(1)
                if index < self.matrix_range["left"]:
                    self.matrix_range["left"] = index
            except ValueError:
                continue
        
        for r in range(self.matrix_range["top"], self.matrix_range["bottom"] + 1):
            for c in range(cols - 1, self.matrix_range["left"] - 1, -1):
                if self.grid[r][c] == 1 and c > self.matrix_range["right"]:
                    self.matrix_range["right"] = c
                    break
        return self.matrix_range