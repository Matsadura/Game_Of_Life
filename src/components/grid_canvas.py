import tkinter as tk
from customtkinter import CTk, CTkFrame, CTkCanvas
from src.components.quad_tree import QuadTree

class GridCanvas(CTkFrame):
    """Class for creating an infinite grid canvas."""

    def __init__(self, master=None, cell_size=40):
        """Initialize the GridCanvas."""
        super().__init__(master)
        self.cell_size = cell_size
        self.zoom_factor = 1.2  # Zoom factor for each zoom in/out action
        self.current_zoom = 1.0  # Current zoom level
        self.max_zoom = 5.0      # Maximum zoom level
        self.min_zoom = 0.2      # Minimum zoom level

        # Create a canvas for the grid
        self.canvas = CTkCanvas(master=self, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create the Quadtree for alive cells
        self.quad_tree = QuadTree((0, 0, master.winfo_width(), master.winfo_height()), 4)

        # Bind the canvas to mouse events
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)  # For scrolling with the mouse wheel
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Key>", self.on_key_press)  # Bind key press events
        self.canvas.focus_set()  # Set focus to the canvas to capture key events

        # Draw the grid
        self.draw_grid()

        # Bind the resize event to update the grid
        self.canvas.bind("<Configure>", lambda e: self.draw_grid())

        # Update scroll region
        self.update_scroll_region()
    
    def on_click(self, event):
        """Handle mouse click to toggle cell state."""
        # Calculate the cell indices based on click position
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        # Toggle the state of the clicked cell
        if row < self.master.rows and col < self.master.cols:
            if self.master.grid[row][col] == 1:
                # Change from alive to dead
                self.master.grid[row][col] = 0
                self.canvas.itemconfig(self.master.cells[row][col], fill=self.master.DEAD)
                self.quad_tree.insert((col * self.cell_size, row * self.cell_size))  # Optionally, remove from QuadTree
            else:
                # Change from dead to alive
                self.master.grid[row][col] = 1
                self.canvas.itemconfig(self.master.cells[row][col], fill=self.master.ALIVE)
                self.quad_tree.insert((col * self.cell_size, row * self.cell_size))

        self.update_scroll_region()

    def draw_grid(self):
        """Draw the grid lines on the canvas."""
        self.canvas.delete("grid")  # Clear previous grid lines

        # Calculate the visible area
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Adjust cell size based on zoom
        self.adjusted_cell_size = int(self.cell_size * self.current_zoom)

        # Draw vertical lines
        for x in range(0, width + self.adjusted_cell_size, self.adjusted_cell_size):
            self.canvas.create_line(x, 0, x, height, fill="gray", tags="grid")

        # Draw horizontal lines
        for y in range(0, height + self.adjusted_cell_size, self.adjusted_cell_size):
            self.canvas.create_line(0, y, width, y, fill="gray", tags="grid")

        # Ensure the last grid lines at the edge
        self.canvas.create_line(width, 0, width, height, fill="gray", tags="grid")
        self.canvas.create_line(0, height, width, height, fill="gray", tags="grid")

    def on_mouse_wheel(self, event):
        """Zoom the canvas with the mouse wheel."""
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def on_key_press(self, event):
        """Zoom in or out with key presses."""
        if event.char == "+":
            self.zoom_in()
        elif event.char == "-":
            self.zoom_out()

    def zoom_in(self):
        """Zoom in the grid."""
        if self.current_zoom < self.max_zoom:  # Limit the zoom in
            self.current_zoom *= self.zoom_factor
            self.update_grid()

    def zoom_out(self):
        """Zoom out the grid."""
        if self.current_zoom > self.min_zoom:  # Limit the zoom out
            self.current_zoom /= self.zoom_factor
            self.update_grid()

    def update_grid(self):
        """Redraw the grid based on the current zoom level."""
        self.draw_grid()  # Redraw the grid
        self.update_scroll_region()  # Update scroll region

    def update_scroll_region(self):
        """Update the scroll region to encompass the entire grid."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

