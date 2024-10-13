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
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f'{self.width}x{self.height}')

        # Default settings
        self.settings = {
            "square_size": 20,
            "simulation_speed": 500
        }

        self.panel_size = self.width // 6

        self.grid_width = self.width - self.panel_size
        self.grid_height = self.height

        self.grid_rows = self.grid_height // self.settings['square_size']
        self.grid_cols = self.grid_width // self.settings['square_size']

        # self.max_grid_size = 100
        self.min_square_size = 10
        self.max_square_size = 50

        self.min_speed = 1
        self.max_speed = 1000

        self.custom_patterns = {}
        self.patterns = {
            "Blinker": Patterns.blinker_pattern(),
            "Glider": Patterns.glider_pattern(),
            "Glider gun": Patterns.glider_gun(),
        }

        # Initialize game and components
        self.grid_canvas = GridCanvas(self)
        self.game = GameOfLife(self.grid_rows, self.grid_cols)
        
        self.game_controls = GameControls(self)
        self.settings_window = SettingsWindow(self)

        self.grid_canvas.draw_grid()  # Draw the initial grid

        # Set up UI elements
        self.create_widgets()
        # self.root.update_idletasks()
        # self.on_resize(event=None)
        # self.root.bind("<Configure>", self.on_resize)
        # Run the main loop
        # self.root.mainloop()
    
    def on_resize(self, event):
        # Get the updated window dimensions
        if not event:
            return 
        self.width = event.width
        self.height = event.height

        # Recalculate the panel and grid dimensions
        self.panel_size = self.width // 6
        self.grid_width = self.width - self.panel_size
        self.grid_height = self.height

        self.grid_rows = self.grid_height // self.settings["square_size"]
        self.grid_cols = self.grid_width // self.settings["square_size"]

        # Resize control frame and grid canvas
        self.control_frame.config(width=self.panel_size, height=self.height)
        self.grid_canvas.update_canvas_size(self.grid_width, self.grid_height)

        # Redraw the grid with new dimensions
        self.grid_canvas.draw_grid()


    def create_widgets(self):
        # Control frame to hold buttons
        self.control_frame = tk.Frame(self.root, width=self.panel_size, borderwidth=20, highlightbackground="black",  highlightthickness=2)
        self.control_frame.pack_propagate(False)
        self.control_frame.pack(side=tk.RIGHT ,expand=False, fill=tk.Y)

        # Control buttons
        tk.Button(self.control_frame, text="Start", command=self.start_game).pack(side=tk.TOP)
        tk.Button(self.control_frame, text="Stop", command=self.stop_game).pack(side=tk.TOP)
        tk.Button(self.control_frame, text="Reset", command=self.reset_game).pack(side=tk.TOP)
        tk.Button(self.control_frame, text="Reset to Initial", command=self.reset_to_initial).pack(side=tk.TOP)
        tk.Button(self.control_frame, text="Settings", command=self.open_settings).pack(side=tk.TOP)
        tk.Button(self.control_frame, text="Save Pattern", command=self.save_pattern).pack(side=tk.TOP)

        # Pattern selection dropdown
        self.pattern_var = StringVar(self.root)
        self.pattern_var.set("None")
        self.pattern_dropdown = OptionMenu(self.control_frame, self.pattern_var, *self.patterns.keys(), command=self.load_pattern)
        self.pattern_dropdown.pack(side=tk.LEFT)

    def load_pattern(self, selected_pattern):
        if selected_pattern in self.patterns:
            self.game.reset()
            self.game.load_pattern(self.patterns[selected_pattern], self.grid_rows // 2, self.grid_cols // 2)
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
        self.grid_rows = self.settings_window.rows_slider.get()
        self.grid_cols = self.settings_window.cols_slider.get()
        self.settings["square_size"] = self.settings_window.square_size_slider.get()
        
        self.grid_canvas.update_canvas_size(self.grid_width, self.grid_height)
        self.game = GameOfLife(self.grid_rows, self.grid_cols)
        self.grid_canvas.draw_grid()

    def update_speed(self):
        self.settings["simulation_speed"] = self.settings_window.speed_slider.get()

    def reset_game(self):
        self.game.reset()
        self.grid_canvas.draw_grid()

    def reset_to_initial(self):
        self.grid_canvas.draw_grid()

    # def run_game(self):
    #     if hasattr(self, 'is_running') and self.is_running:  # Check if is_running is defined
    #         self.game.update()
    #         self.grid_canvas.draw_grid()
    #         self.root.after(self.settings["simulation_speed"], self.run_game)

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
        if 0 <= row < self.grid_rows and 0 <= col < self.grid_cols:
            self.game.toggle_cell(row, col)
            self.grid_canvas.draw_grid()  # Redraw the grid after toggling

    def run(self):
        self.root.mainloop()  # Ensure this method exists to run the main loop

    def run_game(self):
        if hasattr(self, 'is_running') and self.is_running:  # Check if is_running is defined
            changed_cells = self.game.update_game_grid()
            self.grid_canvas.update_grid(changed_cells, self.game.grid)
            self.root.after(self.settings["simulation_speed"], self.run_game)