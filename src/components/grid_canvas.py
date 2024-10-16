import tkinter as tk


class GridCanvas:
    """a canvas for the grid"""
    cells = []

    def __init__(self, main_window):
        """Initiat a canvas to put the grid in it"""
        self.main_window = main_window
        self.canvas = tk.Canvas(
            self.main_window.root,
            borderwidth=2,
            highlightbackground="black",
            background="#080717")
        # Allow canvas to expand and center in the window
        self.canvas.pack(side="left", fill="both", expand=True)
        # Bind the click event to cell_click
        self.canvas.bind("<Button-1>", self.main_window.cell_click)
        self.canvas.update()

    def draw_grid(self):
        """Draw the grid on the canvas"""
        self.canvas.delete("all")  # Clear the canvas before redrawing
        self.cells.clear()
        extra = self.main_window.settings["square_size"] / 20
        for row in range(self.main_window.grid_rows):
            cells_row = []
            for col in range(self.main_window.grid_cols):
                x1 = col * self.main_window.settings["square_size"]
                y1 = row * self.main_window.settings["square_size"]
                x2 = x1 + self.main_window.settings["square_size"]
                y2 = y1 + self.main_window.settings["square_size"]
                color = "#ff00e2" \
                    if self.main_window.game.grid[row][col] == 1 else "#16123a"
                cell = self.canvas.create_oval(
                    x1 + extra, y1 + extra, x2 - extra, y2 - extra, fill=color)
                cells_row.append(cell)
            self.cells.append(cells_row)

    def update_grid(self, changed_cells, grid):
        """Update the changedcells on the grid"""
        for r, c, status in changed_cells:
            color = "#ff00e2" if status == 1 else "#16123a"
            grid[r][c] = status
            self.canvas.itemconfig(self.cells[r][c], fill=color)

    def update_canvas_size(self, new_width, new_height):
        """Update teh canvas size"""
        self.canvas.config(width=new_width, height=new_height)
