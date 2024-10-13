import customtkinter as ctk
import tkinter as tk
import pygame
from tkinter import Toplevel, Scale, Label, StringVar, OptionMenu, simpledialog
from .game_of_life import GameOfLife
from .game_controls import GameControls
from .grid_canvas import GridCanvas
from .settings_window import SettingsWindow
from .patterns import Patterns
import json

pygame.mixer.init()


class StylishButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.default_background = self.cget("fg_color")
        self.default_foreground = self.cget("text_color")
        self.hover_color = "#3CBBB1"  # Color when hovered
        self.transition_steps = 20  # Number of steps for the transition
        self.current_step = 0  # Track the current step of the transition
        self.after_id = None  # Track the after call

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.current_step = 0  # Reset step on enter
        self.transition_color(self.default_background, self.hover_color)

    def on_leave(self, e):
        self.current_step = 0  # Reset step on leave
        self.transition_color(self.hover_color, self.default_background)

    def transition_color(self, start_color, end_color):
        # Split the color into RGB components
        start_rgb = self.hex_to_rgb(start_color)
        end_rgb = self.hex_to_rgb(end_color)

        # Calculate the difference between the two colors
        step_r = (end_rgb[0] - start_rgb[0]) / self.transition_steps
        step_g = (end_rgb[1] - start_rgb[1]) / self.transition_steps
        step_b = (end_rgb[2] - start_rgb[2]) / self.transition_steps

        # Update the button color
        if self.current_step <= self.transition_steps:
            new_color = f'#{int(start_rgb[0] + step_r * self.current_step):02x}{int(start_rgb[1] + step_g * self.current_step):02x}{int(start_rgb[2] + step_b * self.current_step):02x}'
            self.configure(fg_color=new_color)
            self.current_step += 1
            self.after_id = self.after(int(20), lambda: self.transition_color(start_color, end_color))  # Schedule the next color update
        else:
            self.after_cancel(self.after_id)  # Cancel the after call if it exists

    def hex_to_rgb(self, hex_color):
        """Convert a hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


class GameOfLifeMainWindow:
    sound_volume_label = None
    PATTERNS_FILE = "patterns.json"
    patterns = {}
    def __init__(self):
        ctk.set_appearance_mode("System")  # Set to "Dark" or "Light" mode as needed
        ctk.set_default_color_theme("blue")  # Set the default color theme

        self.root = ctk.CTk()  # Change to CustomTkinter main window
        self.root.title("Game of Life")
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f'{self.width}x{self.height}')

        # Default settings
        self.settings = {
            "square_size": 20,
            "simulation_speed": 500
        }

        # load patterns
        self.load_patterns()

        self.panel_size = self.width // 6

        # # Initialize volume settings
        self.volume = 0.5  # Initial volume (0.0 to 1.0)
        self.is_muted = False

        # Initialize game and components
        self.grid_canvas = GridCanvas(self)
        self.grid_width = self.grid_canvas.canvas.winfo_width() - self.panel_size
        self.grid_height = self.grid_canvas.canvas.winfo_height()
        self.grid_rows = self.grid_height // self.settings['square_size']
        self.grid_cols = self.grid_width // self.settings['square_size']
        self.game = GameOfLife(self.grid_rows, self.grid_cols)

        self.game_controls = GameControls(self)
        self.settings_window = SettingsWindow(self)

        self.grid_canvas.draw_grid()  # Draw the initial grid

        # Load and play background music
        pygame.mixer.init()  # Initialize the mixer
        pygame.mixer.music.load('relaxing_piano.mp3')  # Adjust according to your file structure
        pygame.mixer.music.play(-1)  # -1 to loop the music

        # Set up UI elements
        self.create_widgets()

        # Create volume control button
        self.volume_button = StylishButton(self.control_frame, text="Mute", command=self.toggle_mute)
        self.volume_button.pack(side=ctk.TOP, padx=10, pady=5)
        self.sound_volume_label = ctk.StringVar()
        self.sound_volume_label.set("Volume: 50%")


    def set_volume(self, value):
        """Set the volume based on the slider value and update the label."""
        volume = float(value)  # Convert the string value to float
        pygame.mixer.music.set_volume(volume)  # Set the volume in pygame

        # Convert the volume to percentage for display (0% to 100%)
        volume_percentage = int(volume * 100)

        # Update the sound volume label
        self.sound_volume_label.set(f"Volume: {volume_percentage}%")

    def toggle_mute(self):
        if self.is_muted:
            pygame.mixer.music.set_volume(self.volume)  # Set back to the previous volume
            self.volume_button.configure(text="Mute")
        else:
            self.volume = pygame.mixer.music.get_volume()  # Store current volume
            pygame.mixer.music.set_volume(0)  # Mute
            self.volume_button.configure(text="Unmute")

        self.is_muted = not self.is_muted

    def create_widgets(self):
        # Control frame to hold buttons
        self.control_frame = ctk.CTkFrame(self.root, width=self.panel_size, corner_radius=10)
        self.control_frame.pack_propagate(False)
        self.control_frame.pack(side=ctk.RIGHT, expand=False, fill=ctk.Y)

        # Define button color
        button_color = "#3CBBB1"

        # Control buttons
        StylishButton(self.control_frame, text="Start", command=self.start_game, fg_color=button_color, hover_color="#FFFFFFF").pack(side=ctk.TOP, padx=10, pady=5)
        StylishButton(self.control_frame, text="Stop", command=self.stop_game, fg_color=button_color, hover_color="#329C94").pack(side=ctk.TOP, padx=10, pady=5)
        StylishButton(self.control_frame, text="Reset", command=self.reset_game, fg_color=button_color, hover_color="#329C94").pack(side=ctk.TOP, padx=10, pady=5)
        StylishButton(self.control_frame, text="Reset to Initial", command=self.reset_to_initial, fg_color=button_color, hover_color="#329C94").pack(side=ctk.TOP, padx=10, pady=5)
        StylishButton(self.control_frame, text="Settings", command=self.open_settings, fg_color=button_color, hover_color="#329C94").pack(side=ctk.TOP, padx=10, pady=5)
        StylishButton(self.control_frame, text="Save Pattern", command=self.save_pattern, fg_color=button_color, hover_color="#329C94").pack(side=ctk.TOP, padx=10, pady=5)

        # Volume control button
        self.volume_button = StylishButton(self.control_frame, text="Mute", command=self.toggle_mute, fg_color=button_color, hover_color="#329C94")
        self.volume_button.pack(side=ctk.TOP, padx=10, pady=5)

        # Volume slider
        self.volume_slider = ctk.CTkSlider(self.control_frame, from_=0, to=1, command=self.set_volume)

        #  = Scale(self.control_frame, from_=0, to=1, resolution=0.1, orient='horizontal', command=self.set_volume)
        self.volume_slider.set(self.volume)  # Set initial volume
        self.volume_slider.pack(side=ctk.TOP, padx=10, pady=5)

        self.resolution_entry = ctk.CTkEntry(self.control_frame, width=100)
        self.resolution_entry.insert(0, "0.1")

        self.volume_label = ctk.CTkLabel(self.control_frame, textvariable=self.sound_volume_label)
        self.volume_label.pack()

        # Pattern selection dropdown
        self.pattern_var = StringVar()
        self.pattern_var.set("Select a Pattern")
        self.pattern_dropdown = OptionMenu(self.control_frame, self.pattern_var, *self.patterns.keys(), command=self.load_pattern)
        self.pattern_dropdown.pack(side=ctk.LEFT, padx=10, pady=5)

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

    def reset_game(self):
        self.game.reset()
        self.grid_canvas.draw_grid()

    def reset_to_initial(self):
        self.grid_canvas.draw_grid()

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
    
    def load_patterns(self):
        with open(self.PATTERNS_FILE, "r") as file:
            self.patterns = json.load(file)
    
    def save_patterns(self):
        with open(self.PATTERNS_FILE, "w") as file:
            json.dump(self.patterns, file, indent=4)
        
    def load_pattern(self, patt):
        self.game.reset()
        self.game.load_pattern(self.patterns[patt], self.grid_rows, self.grid_cols)
        self.grid_canvas.draw_grid()