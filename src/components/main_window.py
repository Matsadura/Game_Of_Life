import customtkinter as ctk
import random
from .game_of_life import GameOfLife
from .grid_canvas import GridCanvas
from .settings_window import SettingsWindow
from .patterns import Patterns

class GameOfLifeMainWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Game of Life")
        ctk.set_appearance_mode("System")  # System default (dark/light mode)

        # Default settings
        self.settings = {
            "rows": 20,
            "cols": 20,
            "square_size": 20,
            "simulation_speed": 500,
        }

        self.min_square_size = 10
        self.max_square_size = 50

        self.patterns = {
            "Blinker": Patterns.blinker_pattern(),
            "Glider": Patterns.glider_pattern(),
        }

        # Initialize game and components
        self.game = GameOfLife(self.settings["rows"], self.settings["cols"])
        self.grid_canvas = GridCanvas(self)
        self.settings_window = SettingsWindow(self)
        self.game_started = False

        # Set up UI elements
        self.create_widgets()

    def create_widgets(self):
        self.side_panel = ctk.CTkFrame(self.root, width=200)
        self.side_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Control buttons in the side panel using grid layout
        self.start_button = ctk.CTkButton(self.side_panel, text="Start", command=self.start_game)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = ctk.CTkButton(self.side_panel, text="Stop", command=self.stop_game)
        self.stop_button.grid(row=1, column=0, padx=5, pady=5)

        self.reset_button = ctk.CTkButton(self.side_panel, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=2, column=0, padx=5, pady=5)

        self.clear_button = ctk.CTkButton(self.side_panel, text="Clear", command=self.clear_grid)
        self.clear_button.grid(row=3, column=0, padx=5, pady=5)

        # self.settings_button = ctk.CTkButton(self.side_panel, text="Settings", command=self.open_settings)
        # self.settings_button.grid(row=4, column=0, padx=5, pady=5)

        # Zoom buttons
        self.zoom_in_button = ctk.CTkButton(self.side_panel, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.grid(row=5, column=0, padx=5, pady=5)

        self.zoom_out_button = ctk.CTkButton(self.side_panel, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.grid(row=6, column=0, padx=5, pady=5)

        self.mute = ctk.CTkButton(self.side_panel, text="MUTE", command=self.mute)
        self.mute.grid(row=6, column=0, padx=5, pady=5)

        # Create grid canvas
        self.grid_canvas.draw_grid()

    def draw_grid(self):
        self.grid_canvas.draw_grid()

    def zoom_in(self):
        if self.settings["square_size"] < self.max_square_size:
            self.settings["square_size"] += 1
            self.draw_grid()

    def zoom_out(self):
        if self.settings["square_size"] > self.min_square_size:
            self.settings["square_size"] -= 1
            self.draw_grid()

    def start_game(self):
       self.game_started = True
       self.
       

    def stop_game(self):
        # Implementation to stop the game
        pass

    def reset_game(self):
        self.game.reset()
        self.draw_grid()

    def clear_grid(self):
        self.game.clear_grid()
        self.draw_grid()

    # def open_settings(self):
    #     self.settings_window.open()

    def run(self):
        self.root.mainloop()
