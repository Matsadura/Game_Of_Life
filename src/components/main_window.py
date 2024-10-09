import tkinter as tk
from tkinter import Toplevel, Scale, Label, StringVar, OptionMenu, simpledialog
from .game_of_life import GameOfLife
from .game_controls import GameControls
from .grid_canvas import GridCanvas
from .settings_window import SettingsWindow
from .patterns import Patterns

class GameOfLifeMainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game of Life")

        # Default settings
        self.settings = {
            "rows": 20,
            "cols": 20,
            "square_size": 20,
            "simulation_speed": 500
        }

        self.min_grid_size = 5
        self.max_grid_size = 100
        self.min_square_size = 10
        self.max_square_size = 50

        self.min_speed = 50
        self.max_speed = 1000

        self.custom_patterns = {}
        self.patterns = {
            "Blinker": Patterns.blinker_pattern(),
            "Glider": Patterns.glider_pattern(),
        }

        # Initialize game and components
        self.game = GameOfLife(self.settings["rows"], self.settings["cols"])
        self.grid_canvas = GridCanvas(self)
        self.game_controls = GameControls(self)
        self.settings_window = SettingsWindow(self)

        self.grid_canvas.draw_grid()  # Draw the initial grid

        # Set up UI elements
        self.create_widgets()

        # Run the main loop
        self.root.mainloop()

    def create_widgets(self):
        # Control frame to hold buttons
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.TOP, pady=10)  # Add some padding to the top

        # Control buttons
        tk.Button(control_frame, text="Start", command=self.start_game).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Stop", command=self.stop_game).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Reset", command=self.reset_game).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Reset to Initial", command=self.reset_to_initial).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Settings", command=self.open_settings).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Save Pattern", command=self.save_pattern).pack(side=tk.LEFT)

        # Pattern selection dropdown
        self.pattern_var = StringVar(self.root)
        self.pattern_var.set("None")
        self.pattern_dropdown = OptionMenu(control_frame, self.pattern_var, *self.patterns.keys(), command=self.load_pattern)
        self.pattern_dropdown.pack(side=tk.LEFT)

    def load_pattern(self, selected_pattern):
        if selected_pattern in self.patterns:
            self.game.reset()
            self.game.load_pattern(self.patterns[selected_pattern], self.settings["rows"] // 2, self.settings["cols"] // 2)
            self.grid_canvas.draw_grid()

    def open_settings(self):
        self.settings_window.open()

    def save_pattern(self):
        pattern_name = simpledialog.askstring("Save Pattern", "Enter a name for your pattern:")
        if pattern_name:
            self.custom_patterns[pattern_name] = [row[:] for row in self.game.grid]  # Copy current grid state
            self.patterns[pattern_name] = self.custom_patterns[pattern_name]  # Add to patterns
            self.pattern_dropdown['menu'].add_command(label=pattern_name, command=lambda value=pattern_name: self.load_pattern(value))

    def update_grid(self):
        self.settings["rows"] = self.settings_window.rows_slider.get()
        self.settings["cols"] = self.settings_window.cols_slider.get()
        self.settings["square_size"] = self.settings_window.square_size_slider.get()
        
        self.grid_canvas.update_canvas_size()
        self.game = GameOfLife(self.settings["rows"], self.settings["cols"])
        self.grid_canvas.draw_grid()

    def update_speed(self):
        self.settings["simulation_speed"] = self.settings_window.speed_slider.get()

    def reset_game(self):
        self.game.reset()
        self.grid_canvas.draw_grid()

    def reset_to_initial(self):
        self.grid_canvas.draw_grid()

    def run_game(self):
        if hasattr(self, 'is_running') and self.is_running:  # Check if is_running is defined
            self.game.update()
            self.grid_canvas.draw_grid()
            self.root.after(self.settings["simulation_speed"], self.run_game)

    def start_game(self):
        self.is_running = True
        self.run_game()

    def stop_game(self):
        self.is_running = False

    def cell_click(self, event):
        # Determine the cell that was clicked
        square_size = self.settings["square_size"]
        col = event.x // square_size
        row = event.y // square_size

        # Toggle the state of the clicked cell
        if 0 <= row < self.settings["rows"] and 0 <= col < self.settings["cols"]:
            self.game.toggle_cell(row, col)
            self.grid_canvas.draw_grid()  # Redraw the grid after toggling

    def run(self):
        self.root.mainloop()  # Ensure this method exists to run the main loop
