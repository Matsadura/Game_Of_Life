import customtkinter as ctk
import time
import random

ROWS = 50
COLS = 50

CELL_SIZE = 10

class Cell:
    def __init__(self, row, col, is_alive):
        self.row = row
        self.col = col
        self.is_alive = is_alive

    def toggle_state(self):
        self.is_alive = not self.is_alive

class GameOfLife(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid = self.create_grid()
        self.live_cells_count = 0
        self.dead_cells_count = 0
        self.steps = 0

    def create_grid(self):
        grid = []
        for row in range(ROWS):
            grid_row = []
            for col in range(COLS):
                is_alive = random.random() < 0.2
                cell = Cell(row, col, is_alive)
                grid_row.append(cell)
                if is_alive:
                    self.live_cells_count += 1
                else:
                    self.dead_cells_count += 1
            grid.append(grid_row)
        return grid