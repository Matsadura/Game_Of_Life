import tkinter as tk

class GridCanvas:
    def __init__(self, main_window):
        self.main_window = main_window
        self.canvas = tk.Canvas(self.main_window.root)
        self.canvas.pack(expand=True)  # Allow canvas to expand and center in the window
        self.canvas.bind("<Button-1>", self.main_window.cell_click)  # Bind the click event to cell_click
        self.update_canvas_size()

    def draw_grid(self):
        self.canvas.delete("all")  # Clear the canvas before redrawing
        for row in range(self.main_window.settings["rows"]):
            for col in range(self.main_window.settings["cols"]):
                x1 = col * self.main_window.settings["square_size"]
                y1 = row * self.main_window.settings["square_size"]
                x2 = x1 + self.main_window.settings["square_size"]
                y2 = y1 + self.main_window.settings["square_size"]
                color = "black" if self.main_window.game.grid[row][col] == 1 else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def update_canvas_size(self):
        self.canvas.config(width=self.main_window.settings["square_size"] * self.main_window.settings["cols"],
                           height=self.main_window.settings["square_size"] * self.main_window.settings["rows"])
