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

    # def update_game_grid(self):
    #     # new_grid = self.create_grid()
    #     # TODO: add a start and end points in grid update
    #     new = []
    #     for r in range(**self.r_range):
    #         for c in range(self.c_range):
    #             alive_neighbors = self.count_alive_neighbors(r, c)
    #             if self.grid[r][c] == 1 and alive_neighbors not in (2, 3):  # Cell is alive and has too few or too many neighbors
    #                 new.append((r, c, 0))
    #             elif self.grid[r][c] == 0 and alive_neighbors == 3:  # Cell is dead and has exactly 3 neighbors
    #                 new.append((r, c, 1))
    #     self.reset_range()
    #     return new

    def update_game_grid(self):
        # new_grid = self.create_grid()
        # TODO: add a start and end points in grid update
        new = []
        for r in range(self.rows):
            for c in range(self.cols):
                alive_neighbors = self.count_alive_neighbors(r, c)
                if self.grid[r][c] == 1 and alive_neighbors not in (2, 3):  # Cell is alive and has too few or too many neighbors
                    new.append((r, c, 0))
                elif self.grid[r][c] == 0 and alive_neighbors == 3:  # Cell is dead and has exactly 3 neighbors
                    new.append((r, c, 1))
        return new

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

    def load_pattern(self, pattern, start_row, start_col):
        for r_offset, row in enumerate(pattern):
            for c_offset, cell in enumerate(row):
                if cell == 1:
                    self.grid[start_row + r_offset][start_col + c_offset] = 1


class QuadTree:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.alive = False
        self.subquadrants = None

    def divide(self):
        half_size = self.size // 2
        self.subquadrants = [
            QuadTree(self.x, self.y, half_size),
            QuadTree(self.x + half_size, self.y, half_size),
            QuadTree(self.x, self.y + half_size, half_size),
            QuadTree(self.x + half_size, self.y + half_size, half_size)
        ]

    def update(self):
        # Recursively update each quadrant
        if self.subquadrants:
            for quad in self.subquadrants:
                quad.update()
        # If all subquadrants are alive or dead, collapse them
        if self.all_alive() or self.all_dead():
            self.collapse()

    def all_alive(self):
        return all(quad.alive for quad in self.subquadrants)

    def all_dead(self):
        return all(not quad.alive for quad in self.subquadrants)

    def collapse(self):
        # Collapse subquadrants back into a single node
        self.subquadrants = None
        self.alive = self.all_alive()


    # def __init__(self, rows, cols):
    #     self.rows = rows
    #     self.cols = cols
    #     self.grid = self.create_grid()
    #
    # def create_grid(self):
    #     return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    # def update(self):
    #     new_grid = self.create_grid()
    #     for r in range(self.rows):
    #         for c in range(self.cols):
    #             alive_neighbors = self.count_alive_neighbors(r, c)
    #             if self.grid[r][c] == 1:  # Cell is alive
    #                 new_grid[r][c] = 1 if alive_neighbors in (2, 3) else 0
    #             else:  # Cell is dead
    #                 new_grid[r][c] = 1 if alive_neighbors == 3 else 0
    #     self.grid = new_grid

    # def count_alive_neighbors(self, row, col):
    #     directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    #     count = 0
    #     for d in directions:
    #         r, c = row + d[0], col + d[1]
    #         if 0 <= r < self.rows and 0 <= c < self.cols:
    #             count += self.grid[r][c]
    #     return count
    
    def reset(self):
        self.grid = self.create_grid()

    def toggle_cell(self, row, col):
        self.grid[row][col] = 1 - self.grid[row][col]  # Flip between 0 and 1

    def load_pattern(self, pattern, start_row, start_col):
        for r_offset, row in enumerate(pattern):
            for c_offset, cell in enumerate(row):
                if cell == 1:
                    self.grid[start_row + r_offset][start_col + c_offset] = 1
