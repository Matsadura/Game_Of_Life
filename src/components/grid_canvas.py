import tkinter as tk

class GridCanvas:
    cells = []
    def __init__(self, main_window):
        self.main_window = main_window
        self.canvas = tk.Canvas(
            self.main_window.root,
            borderwidth=2,
            highlightbackground="black"
        )
        self.canvas.pack(side="left", fill="both", expand=True)  # Allow canvas to expand and center in the window
        self.canvas.update()
        self.canvas.bind("<Button-1>", self.main_window.cell_click)  # Bind click event to cell_click

        # Track panning offsets
        self.offset_x = 0
        self.offset_y = 0

        # Variables to track dragging state
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0

        # Bind events for dragging
        self.canvas.bind("<ButtonPress-1>", self.start_drag)  # Middle mouse button or touchpad click to start dragging
        self.canvas.bind("<B1-Motion>", self.do_drag)  # While holding the middle mouse button, drag
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)  # Stop dragging when the button is released

    def start_drag(self, event):
        """Start the drag movement."""
        self.is_dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def do_drag(self, event):
        """Handle dragging of the grid."""
        if self.is_dragging:
            move_x = event.x - self.drag_start_x
            move_y = event.y - self.drag_start_y

            # Redraw the grid with the new offset
            self.draw_grid(offset_x=move_x, offset_y=move_y, preserve_state=True)

            # Update the drag start position
            self.drag_start_x = event.x
            self.drag_start_y = event.y

    def stop_drag(self, event):
        """Stop dragging once the mouse button is released."""
        self.is_dragging = False

    def draw_grid(self, offset_x=0, offset_y=0, preserve_state=False):
        square_size = self.main_window.settings["square_size"]
        self.cells.clear()
        # Update offsets for panning
        self.offset_x += offset_x
        self.offset_y += offset_y

        if not preserve_state:
            # If not preserving state, start with a clean grid
            self.canvas.delete("all")

        # Determine how much of the grid is visible within the canvas bounds
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Calculate the range of rows and columns to be drawn based on the offsets and zoom level
        start_col = max(0, -self.offset_x // square_size)
        start_row = max(0, -self.offset_y // square_size)
        end_col = min(self.main_window.grid_cols, (canvas_width - self.offset_x) // square_size + 1)
        end_row = min(self.main_window.grid_rows, (canvas_height - self.offset_y) // square_size + 1)

        for row in range(start_row, end_row):
            cells_row = []
            for col in range(start_col, end_col):
                x1 = col * square_size + self.offset_x
                y1 = row * square_size + self.offset_y
                x2 = x1 + square_size
                y2 = y1 + square_size

                # Check the state of the cell in the GameOfLife object
                if self.main_window.game.grid[row][col] == 1:
                    fill_color = "black"  # Alive cells
                else:
                    fill_color = "white"  # Dead cells

                # Draw the cell
                cell = self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill=fill_color)
                cells_row.append(cell)
            self.cells.append(cells_row)

    def update_grid(self, changed_cells, grid):
        for r, c, status in changed_cells:
            color = "black" if status == 1 else "white"
            grid[r][c] = status
            self.canvas.itemconfig(self.cells[r][c], fill=color)


    def update_canvas_size(self, new_width, new_height):
        """Update the size of the canvas when the window is resized."""
        self.canvas.config(width=new_width, height=new_height)

    def reset_view(self):
        """Reset the grid view to the original (no panning or zooming)."""
        self.offset_x = 0
        self.offset_y = 0
        self.main_window.settings["square_size"] = self.main_window.default_square_size
        self.draw_grid(preserve_state=True)
