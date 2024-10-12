import customtkinter as ctk

class GridCanvas:
    def __init__(self, main_window):
        self.main_window = main_window
        
        # Create a frame to hold the canvas, and use layout managers on the frame
        self.frame = ctk.CTkFrame(self.main_window.root)
        self.frame.grid(row=0, column=0, padx=10, pady=10)  # Adjust as needed

        # Create the canvas inside the frame
        self.canvas = ctk.CTkCanvas(self.frame, bg="grey")
        self.canvas.pack(fill="both", expand=True)

        # Bind left click for cell toggling
        self.canvas.bind("<Button-1>", self.cell_click)

    def draw_grid(self):
        # Clear the canvas before redrawing
        self.canvas.delete("all")

        # Iterate over the grid and draw each cell
        for row in range(self.main_window.settings["rows"]):
            for col in range(self.main_window.settings["cols"]):
                x0 = col * self.main_window.settings["square_size"]
                y0 = row * self.main_window.settings["square_size"]
                x1 = x0 + self.main_window.settings["square_size"]
                y1 = y0 + self.main_window.settings["square_size"]
                color = "lightgreen" if self.main_window.game.grid[row][col] else "white"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

        # Update the canvas size based on new grid settings
        self.update_canvas_size()

    def update_canvas_size(self):
        self.canvas.config(
            width=self.main_window.settings["cols"] * self.main_window.settings["square_size"],
            height=self.main_window.settings["rows"] * self.main_window.settings["square_size"]
        )

    def cell_click(self, event):
        # Handle cell click events
        square_size = self.main_window.settings["square_size"]
        col = int(event.x // square_size)
        row = int(event.y // square_size)

        if 0 <= row < self.main_window.settings["rows"] and 0 <= col < self.main_window.settings["cols"]:
            self.main_window.game.toggle_cell(row, col)
            self.draw_grid()
