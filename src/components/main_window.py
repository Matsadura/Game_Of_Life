import customtkinter as ctk
import tkinter as tk
import pygame
from tkinter import Toplevel, StringVar, simpledialog, messagebox
from .game_of_life import GameOfLife
from .grid_canvas import GridCanvas
from .stylish_button import StylishButton
from .patterns import Patterns
import json
import os
from PIL import Image

pygame.mixer.init()

class GameOfLifeMainWindow:
    """The main window of the game"""
    sound_volume_label = None
    speed_label_state = None
    PATTERNS_FILE = "data/patterns.json"
    patterns = {}
    changed_cells = []
    def __init__(self):
        """Initialize the main window and set default parameters.

        Sets the appearance mode, color theme, sound volume, and initializes
        the patterns. Calls methods to create widgets and show the intro window.
        """
        ctk.set_appearance_mode("System")  # Set to "Dark" or "Light" mode as needed
        ctk.set_default_color_theme("blue")  # Set the default color theme

        self.root = ctk.CTk()  # Change to CustomTkinter main window
        self.root.withdraw() 
        self.root.title("Game of Life")
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f'{self.width}x{self.height}')

        self.colors = {
            "background": "#100D28",
            "primary": "#ff00e2",
            "secondary": "#8906e6"
        }

        # Default settings
        self.settings = {
            "square_size": 20,
            "simulation_speed": 500
        }

        # load patterns
        self.patterns = Patterns.get_patterns()
        self.load_patterns()

        self.panel_size = self.width // 6

        # # Initialize volume settings
        self.volume = 0.5  # Initial volume (0.0 to 1.0)
        self.is_muted = False
        self.show_intro_window()

    def show_intro_window(self):
        """Display the introductory window with a welcome message.

        This window contains a "Play" button. The main window remains hidden
        until this window is closed.
        """
        # Create the introductory window
        self.intro_window = Toplevel(self.root)
        self.intro_window.title("Welcome to the Game of Life")
        self.intro_window.geometry("600x700")
        self.intro_window.configure(bg=self.colors.get("background"))
        image = ctk.CTkImage(dark_image=Image.open("assets/images/welcoming-window.png"), size=(450, 450))
        logo = ctk.CTkLabel(self.intro_window, image=image, text="")
        logo.pack(pady=10)

        # Play button
        play_button = ctk.CTkButton(self.intro_window,
            fg_color=self.colors["primary"],
            font=("System", 20),
            width=300,
            height=40,
            hover_color=self.colors["secondary"],
            text="PLAY",
            command=self.on_intro_window_close
        )
        play_button.pack(pady=10)

        # Center the introductory window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (400 / 2)
        y = (screen_height / 2) - (300 / 2)
        self.intro_window.geometry(f"+{int(x)}+{int(y)}")

        # Ensure that the main window is disabled until the intro window is closed
        self.intro_window.protocol("WM_DELETE_WINDOW", self.on_intro_window_close)


    def on_intro_window_close(self):
        """Handle the event when the intro window is closed.

        Shows the main window and initializes the game components.
        """
        # Show the main window again if the intro window is closed
        if self.intro_window:
            self.intro_window.destroy()
        self.root.deiconify()  # Show the main window
        self.init_game()
        pygame.mixer.music.unpause()  # Resume music if paused

    def init_game(self):
        """Initialize the game components.

        Sets up the grid canvas, control buttons, and background music.
        """
        # Initialize game and components
        self.grid_canvas = GridCanvas(self)
        self.grid_width = self.grid_canvas.canvas.winfo_width() - self.panel_size
        self.grid_height = self.grid_canvas.canvas.winfo_height()
        self.grid_rows = self.grid_height // self.settings['square_size']
        self.grid_cols = self.grid_width // self.settings['square_size']
        self.game = GameOfLife(self.grid_rows, self.grid_cols)
        self.game.load_pattern(self.patterns["glider_gun"], self.grid_rows, self.grid_cols)
        self.grid_canvas.draw_grid()  # Draw the initial grid

        # Load and play background music
        pygame.mixer.init()  # Initialize the mixer
        pygame.mixer.music.load('relaxing_piano.mp3')  # Adjust according to your file structure
        pygame.mixer.music.play(-1)  # -1 to loop the music

        # Create volume control button
        self.sound_volume_label = ctk.StringVar(value=f"Volume {int(self.volume * 100)}%")
        val = 501 - self.settings["simulation_speed"]
        self.speed_label_state = ctk.StringVar(value=f"Speed {val}")

        # Set up UI elements
        self.create_widgets()

    def set_speed(self, value):
        """Set the volume based on the slider value and update the label."""
        volume = int(value)  # Convert the string value to float
        # Update the sound volume label
        self.settings["simulation_speed"] = volume
        self.speed_label_state.set(value=f"Speed {501 - int(value)}")


    def set_volume(self, value):
        """Set the volume based on the slider value and update the label."""
        volume = float(value)  # Convert the string value to float
        pygame.mixer.music.set_volume(volume)  # Set the volume in pygame

        # Convert the volume to percentage for display (0% to 100%)
        volume_percentage = int(volume * 100)

        # Update the sound volume label
        self.sound_volume_label.set(f"Volume: {volume_percentage}%")

    def toggle_mute(self):
        """Toggle the sound volume between muted and the previous volume.

        When muted, the volume is set to 0. When unmuted, it restores the 
        volume to the level it was before muting. Updates the volume button 
        label accordingly.
        """
        if self.is_muted:
            pygame.mixer.music.set_volume(self.volume)  # Set back to the previous volume
            self.volume_button.configure(text="Mute")
        else:
            self.volume = pygame.mixer.music.get_volume()  # Store current volume
            pygame.mixer.music.set_volume(0)  # Mute
            self.volume_button.configure(text="Unmute")

        self.is_muted = not self.is_muted

    def create_widgets(self):
        """Create and pack the various UI elements.

        Includes control buttons, volume control, and a pattern selection dropdown.
        """
        # Control frame to hold buttons
        self.control_frame = ctk.CTkFrame(self.root, fg_color=self.colors["background"], border_color=self.colors['primary'], border_width=1, width=self.panel_size, corner_radius=10)
        self.control_frame.pack_propagate(False)
        self.control_frame.pack(side=ctk.RIGHT, expand=False, fill=ctk.Y)

        # Define button color

        # Control buttons
        # I did this to make the botton not stcking in the top
        StylishButton(
            self.control_frame,
            text="Start",
            fg_color=self.colors["primary"],
            width=200,
            height=40,
            font=("System", 20),
            hover_color=self.colors.get("secondary"),
            command=self.start_game,
        ).pack(padx=10, pady=(40, 5))

        for button_text, command in [
            # ("Start", self.start_game),
            ("Stop", self.stop_game),
            ("Reset", self.reset_game),
            ("Clear", self.clear),
            ("Save Pattern", self.save_pattern),
            ("Next Generation", self.next_gen)
        ]:
            StylishButton(
                self.control_frame,
                text=button_text,
                command=command,
                fg_color=self.colors["secondary"],
                width=200,
                height=40,
                font=("System", 20),
                hover_color=self.colors.get("primary"),
            ).pack(padx=10, pady=5)

        # Volume control button
        self.volume_button = StylishButton(self.control_frame, text="Mute", command=self.toggle_mute, fg_color=self.colors["secondary"], font=("System", 20), hover_color=self.colors.get("background"), width=200, height=40)
        self.volume_button.pack(side=ctk.TOP, padx=10, pady=5)

        # Volume slider
        self.volume_slider = ctk.CTkSlider(self.control_frame,
            fg_color=self.colors.get('secondary'),
            progress_color=self.colors.get("primary"),
            button_color=self.colors.get('primary'),
            button_hover_color='#ffffff',
            from_=0,
            to=1,
            command=self.set_volume
        )


        #  = Scale(self.control_frame, from_=0, to=1, resolution=0.1, orient='horizontal', command=self.set_volume)
        self.volume_slider.set(self.volume)  # Set initial volume
        self.volume_slider.pack(side=ctk.TOP, padx=10, pady=(30, 0))

        # Volume label
        self.volume_label = ctk.CTkLabel(self.control_frame, font=("System", 18), textvariable=self.sound_volume_label)
        self.volume_label.pack(side=ctk.TOP, padx=10, pady=5)


        # Speed slider logic
        self.speeed_slider = ctk.CTkSlider(
            self.control_frame,
            fg_color=self.colors.get('secondary'),
            progress_color=self.colors.get("primary"),
            button_color=self.colors.get('primary'),
            button_hover_color='#ffffff',
            from_=500,
            to=1,
            command=self.set_speed
        )
        self.speeed_slider.set(self.settings["simulation_speed"])  # Set initial volume
        self.speeed_slider.pack(side=ctk.TOP, padx=10, pady=(20, 0))

        self.speed_label = ctk.CTkLabel(self.control_frame, font=("System", 18), textvariable=self.speed_label_state)
        self.speed_label.pack(side=ctk.TOP, padx=10, pady=0)

        # Pattern selection dropdown
        self.pattern_var = StringVar(self.root)
        self.pattern_var.set("Select...")
        self.pattern_dropdown = ctk.CTkOptionMenu(
            self.control_frame,
            font=('System', 20),
            button_color=self.colors.get('primary'),
            button_hover_color=self.colors.get('secondary'),
            fg_color=self.colors.get('secondary'),
            width=200,
            height=40,
            variable=self.pattern_var,
            values=list(self.patterns.keys()),
            dropdown_fg_color=self.colors.get('background'),
            dropdown_hover_color=self.colors.get('primary'),
            dropdown_font=('System', 18),
            command=self.load_pattern
        )
        self.pattern_dropdown.pack(pady=30)  # Adjust padding as necessary
        # Optional: If you want to add a resolution entry below the dropdown
        # self.resolution_entry = ctk.CTkEntry(self.dropdown_frame, width=100)
        # self.resolution_entry.insert(0, "0.1")
        # self.resolution_entry.pack(pady=5)  # Adjust padding as necessary

        self.help_button = ctk.CTkButton(self.control_frame, text="?",
                                         width=50, height=50,
                                         corner_radius=25,
                                         fg_color="#007bff",
                                         hover_color="#0056b3",
                                         command=self.show_rules)
        self.help_button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)

    def next_gen(self):
        """Go to teh next generation"""
        changed_cells = self.game.update_game_grid(self.grid_canvas)
        if not changed_cells:
            return
        self.grid_canvas.update_grid(changed_cells, self.game.grid)

    def save_pattern(self):
        """Prompt the user to enter a name for the current pattern and save it.

        Checks for uniqueness of the name before saving the pattern to a file.
        """
        matrix_range = self.game.get_matrix_range(self.grid_rows, self.grid_cols)
        if not matrix_range:
            messagebox.showerror("Error", "The grid is empty, make sure you draw something first.")
            return

        pattern_name = simpledialog.askstring("Save Pattern", "Enter a name for your pattern:")
        if pattern_name == None or pattern_name.strip() == "":
            messagebox.showerror("Error", "Please enter a name for your pattern.")

        if pattern_name in self.patterns:
            # Check if the pattern name already exists
            messagebox.showerror("Error", f"Pattern '{pattern_name}' already exists. Please choose a different name.")
        else:
            self.patterns[pattern_name] = [
                row[matrix_range["left"]:matrix_range["right"] + 1]
                for row in
                self.game.grid[matrix_range["top"]:matrix_range["bottom"] + 1]
                ]
            self.save_patterns()
            self.pattern_dropdown.configure(values=list(self.patterns.keys()))

    def update_grid(self):
        """Update the grid dimensions based on settings specified in the settings window.

        Resizes the game grid accordingly to reflect the changes made by the user.
        """

        self.grid_canvas.update_canvas_size(self.grid_width, self.grid_height)
        self.game = GameOfLife(self.grid_rows, self.grid_cols)
        self.grid_canvas.draw_grid()

    def reset_game(self):
        """Reset the game state and reload the current pattern into the grid.

        Clears the grid and sets it to the initial configuration of the current pattern.
        """
        self.game.reset()
        self.grid_canvas.draw_grid()

    def clear(self):
        """Clear the current game grid.

        Removes all live cells from the grid, resetting it to an empty state.
        """
        self.game.reset()
        self.grid_canvas.draw_grid()

    def start_game(self):
        self.is_running = True
        self.run_game()

    def stop_game(self):
        """Start the game simulation if it is not already running.

        Begins the updating of the grid based on the simulation rules.
        """
        self.is_running = False

    def cell_click(self, event):
        """Stop the game simulation.

        Halts the updating of the grid and the game loop.
        """
        # Determine the cell that was clicked
        square_size = self.settings["square_size"]
        col = event.x // square_size
        row = event.y // square_size

        # Toggle the state of the clicked cell
        if 0 <= row < self.grid_rows and 0 <= col < self.grid_cols:
            current_cell = self.game.grid[row][col]
            color = "#ff00e2" if current_cell == 0 else "#191541"
            self.game.grid[row][col] = 1 if current_cell == 0 else 0
            self.grid_canvas.canvas.itemconfig(self.grid_canvas.cells[row][col], fill=color)

    def run(self):
        """Start the main event loop for the application.

        Keeps the application running and responsive to user inputs.
        """
        self.root.mainloop()  # Ensure this method exists to run the main loop

    def run_game(self):
        """Update the game grid and schedule the next update.

        Processes the game logic for the current simulation step and prepares for the next iteration.
        """
        if hasattr(self, 'is_running') and self.is_running:  # Check if is_running is defined
            changed_cells = self.game.update_game_grid(self.grid_canvas)
            self.grid_canvas.update_grid(changed_cells, self.game.grid)
            self.root.after(self.settings["simulation_speed"], self.run_game)
    
    def validate_data_direcory(self):
        """Check if the "data" directory exists.

        Creates the directory if it does not exist to ensure proper saving/loading of patterns.
        """
        if not os.path.exists("data"):
            os.makedirs("data")

    def load_patterns(self):
        """Save the current patterns to the specified JSON file.

        Excludes any default patterns and preserves user-created patterns for future use.
        """
        if not os.path.exists(self.PATTERNS_FILE):
            return
        with open(self.PATTERNS_FILE, "r") as file:
            self.patterns.update(json.load(file))
    
    def save_patterns(self):
        """Save the current patterns to the specified JSON file.

        Excludes any default patterns and preserves user-created patterns for future use.
        """
        new_patterns = self.patterns.copy()
        for pattern in Patterns.patterns_names():
            new_patterns.pop(pattern, None)
        
        if len(new_patterns) == 0:
            return

        self.validate_data_direcory()
        with open(self.PATTERNS_FILE, "w") as file:
            json.dump(new_patterns, file)
        
    def load_pattern(self, patt):
        """Load a specific pattern into the game.

        Updates the grid with the selected pattern from the available patterns.
        """
        self.game.reset()
        self.game.load_pattern(self.patterns[patt], self.grid_rows, self.grid_cols)
        self.grid_canvas.draw_grid()

    def show_rules(self):
        """The rules of Conway's Game of Life"""
        rules_window = ctk.CTkToplevel(self.root)
        rules_window.title("Conway's Game of Life Rules")
        rules_window.geometry("600x500")
        title = "Conway's Game of Life Rules:"

        rules_text = """1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.

2. Any live cell with two or three live neighbours lives on to the next generation.

3. Any live cell with more than three live neighbours dies, as if by overpopulation.

4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction."""

        rules_label = ctk.CTkLabel(rules_window, text=title, wraplength=550, justify=tk.CENTER, font=('System', 20))
        rules_label.pack(pady=20, padx=5)

        rules_label = ctk.CTkLabel(rules_window, text=rules_text, justify=tk.CENTER, font=('System', 20))
        rules_label.pack(pady=20, padx=5)

        close_button = ctk.CTkButton(rules_window, text="Close", command=rules_window.destroy)
        close_button.pack(side=tk.BOTTOM, pady=10)