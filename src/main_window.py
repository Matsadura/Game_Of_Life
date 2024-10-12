""" Main Window Class """

import tkinter
from random import randint
from time import sleep, time
from src.components.grid_canvas import GridCanvas
import json
import os
import numpy as np


from customtkinter import *


class MainWindow(CTk):
    """Main Window Class"""

    screen_width = 0
    screen_height = 0
    display_window_width = 0
    cell_size = 10
    grid = None
    start = 0
    pattern_file = "patterns.json"
    patterns = None
    current_pattern = "glider_gun"
    ALIVE = "black"
    DEAD = "white"
    new_grid = []

    def load_patterns(self):
        """Load patterns from json file"""
        if not os.path.exists(self.pattern_file):
            self.patterns = {}
            return

        with open(self.pattern_file, "r") as file:
            self.patterns = json.load(file)

    def save_patterns(self):
        """Save patterns to json file"""
        with open(self.pattern_file, "w") as file:
            json.dump(self.patterns, file, indent=4)

    def __init__(self):
        """Intatianize Main Window"""
        super().__init__()
        # load the patterns
        self.load_patterns()

        # create the app window
        self.create_window()

        # create teh grid
        self.create_grid()

        # 
        self.draw_grid()
        self.play()
        self.start = time()

    def create_window(self):
        self.title("John Conway's Game Of Life")
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(width=True, height=True)
        self.display_window = CTkFrame(
            master=self, border_width=2, border_color="black"
        )
        self.display_window.pack(side="left", fill="both", expand=True)
        self.options_window = CTkFrame(
            master=self,
            border_width=2,
            border_color="black",
            width=(self.width * 2 // 12),
        )
        self.options_window.pack(side="right", fill="both")
        self.update()
        self.display_window_width = self.display_window.winfo_width()

    def create_grid(self):
        self.cols = self.display_window_width // self.cell_size
        self.rows = self.height // self.cell_size
        print(f"the grid specs are [{self.cols},{self.rows}]")

        # Initialize the grid with all DEAD cells
        self.grid = np.zeros((self.rows, self.cols), dtype=int)

        # Coordinates of the center of the grid
        mid_row = self.rows // 2
        mid_col = self.cols // 2

        # Define the Gosper Glider Gun pattern
        glider_gun = self.patterns[self.current_pattern]

        glider_gun_rows = len(glider_gun)
        glider_gun_cols = len(glider_gun[0])
        
        start_row = mid_row - glider_gun_rows // 2
        start_col = mid_col - glider_gun_cols // 2

        # Place the glider gun in the middle of the grid
        for i in range(glider_gun_rows):
            for j in range(glider_gun_cols):
                self.grid[start_row + i][start_col + j] = glider_gun[i][j]

        # Create the canvas to display the grid
        self.canvas = tkinter.Canvas(
            self.display_window,
        )
        self.canvas.pack(fill="both", expand=True)
        
        self.draw_grid()

    def draw_grid(self):
        self.cells = []
        for i in range(self.rows):
            cells_row = []
            for j in range(self.cols):
                fill = self.ALIVE if self.grid[i][j] == 1 else self.DEAD
                cell = self.canvas.create_rectangle(
                    j * self.cell_size,
                    i * self.cell_size,
                    (j + 1) * self.cell_size,
                    (i + 1) * self.cell_size,
                    fill=fill,
                    outline="black",
                )
                cells_row.append(cell)
            self.cells.append(cells_row)

    def get_surrounding(self, i, j, cell):
        r_start = max(i - 1, 0)
        c_start = max(j - 1, 0)
        r_end = min(i + 1, self.rows - 1)
        c_end = min(j + 1, self.cols - 1)

        count = -1 if cell == 1 else 0

        for row in range(r_start, r_end + 1):
            for col in range(c_start, c_end + 1):
                if self.grid[row][col] == 1:
                    count += 1
                if count > 3:
                    break

        if cell == 1 and (count < 2 or count > 3):
                self.new_grid.append((i, j, 0))
        elif cell == 0 and count == 3:
                self.new_grid.append((i, j, 1))

    def update_grid(self):
        """Randomly update the grid state and redraw it"""
        self.new_grid.clear()
        for i in range(self.rows):
            for j in range(self.cols):
                self.get_cell_state(i, j)

        for i, j, new_state in self.new_grid:
            self.grid[i][j] = new_state
            fill = self.ALIVE if new_state == 1 else self.DEAD
            self.canvas.itemconfig(self.cells[i][j], fill=fill)
    
    def get_cell_state(self, i, j):
        self.get_surrounding(i, j, self.grid[i][j])

    # def get_surrending(self, i, j, cell):
    #     r_start = max(i - 1, 0)
    #     c_start = max(j - 1, 0)
    #     r_end = min(i + 1, self.rows - 1)
    #     c_end = min(j + 1, self.cols - 1)

    #     count = -1 if cell == 1 else 0

    #     for row in range(r_start, r_end + 1):
    #         for col in range(c_start, c_end + 1):
    #             if self.grid[row][col] == 1:
    #                 count += 1

    #     return count

    # def get_cell_state(self, i, j):
    #     cell = self.grid[i][j]
    #     neighbours_count = self.get_surrending(i, j, cell)
    #     if cell == 1 and (neighbours_count > 3 or neighbours_count < 2):
    #         return 0
    #     elif cell == 0 and neighbours_count == 3:
    #         return 1

    #     return cell

    # def update_grid(self):
    #     """Randomly update the grid state and redraw it"""
    #     print("creating grid:", time() - self.start)
    #     new_grid = [
    #         [self.get_cell_state(row, col) for col in range(self.cols)]
    #         for row in range(self.rows)
    #     ]
    #     print("grid created:", time() - self.start)
    #     print("grid is been updated:", time() - self.start)
    #     for i in range(self.rows):
    #         for j in range(self.cols):
    #             if new_grid[i][j] != self.grid[i][j]:
    #                 self.grid[i][j] = new_grid[i][j]
    #                 fill = self.ALIVE if self.grid[i][j] == 1 else self.DEAD
    #                 self.canvas.itemconfig(self.cells[i][j], fill=fill)

    def play(self):
        """Run the game of life updates using Tkinter's after method"""
        self.update_grid()
        self.after(10, self.play)
