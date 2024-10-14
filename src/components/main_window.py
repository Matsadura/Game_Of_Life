import customtkinter as ctk
import tkinter as tk
import pygame
from tkinter import Toplevel, Scale, Label, StringVar, OptionMenu, simpledialog, messagebox
from .game_of_life import GameOfLife
from .game_controls import GameControls
from .grid_canvas import GridCanvas
from .patterns import Patterns
import json
import os
from PIL import Image

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

        # self.bind("<Enter>", self.on_enter)
        # self.bind("<Leave>", self.on_leave)

    # def on_enter(self, e):
    #     self.current_step = 0  # Reset step on enter
    #     self.transition_color(self.default_background, self.hover_color)

    # def on_leave(self, e):
    #     self.current_step = 0  # Reset step on leave
    #     self.transition_color(self.hover_color, self.default_background)

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
        if type(hex_color) is not str:
            return (255, 255, 255)
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


class GameOfLifeMainWindow:
    sound_volume_label = None
    PATTERNS_FILE = "data/patterns.json"
    patterns = {}
    changed_cells = []
    def __init__(self):
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
            "simulation_speed": 1
        }
        self.default_square_size = self.settings["square_size"]  # Store default zoom level
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.grid_offset_x = 0  # X-offset for panning the grid
        self.grid_offset_y = 0  # Y-offset for panning the grid
        
        # load patterns
        self.patterns = Patterns.get_patterns()
        self.load_patterns()

        self.panel_size = self.width // 6

        self.grid_width = self.width - self.panel_size
        self.grid_height = self.height

        self.grid_rows = self.grid_height // self.settings['square_size']
        self.grid_cols = self.grid_width // self.settings['square_size']
        
        # # Initialize volume settings
        self.volume = 0.2  # Initial volume (0.0 to 1.0)
        self.is_muted = False
        self.show_intro_window()

    def show_intro_window(self):
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
        # Show the main window again if the intro window is closed
        if self.intro_window:
            self.intro_window.destroy()
        self.root.deiconify()  # Show the main window
        self.init_game()
        pygame.mixer.music.unpause()  # Resume music if paused

    def init_game(self):
        # Initialize game and components
        self.grid_canvas = GridCanvas(self)
        self.grid_canvas.canvas.bind("<ButtonPress-1>", self.start_drag)  # Bind left mouse button press
        self.grid_canvas.canvas.bind("<B1-Motion>", self.do_drag)        # Bind mouse movement (while button 1 is held)
        self.grid_canvas.canvas.bind("<ButtonRelease-1>", self.end_drag)  # Bind left mouse button release
        self.grid_width = self.grid_canvas.canvas.winfo_width() - self.panel_size
        self.grid_height = self.grid_canvas.canvas.winfo_height()
        self.grid_rows = self.grid_height // self.settings['square_size']
        self.grid_cols = self.grid_width // self.settings['square_size']
        self.game = GameOfLife(self.grid_rows, self.grid_cols)

        self.game_controls = GameControls(self)

        self.grid_canvas.draw_grid()  # Draw the initial grid

        # Load and play background music
        pygame.mixer.init()  # Initialize the mixer
        pygame.mixer.music.load('relaxing_piano.mp3')  # Adjust according to your file structure
        pygame.mixer.music.play(-1)  # -1 to loop the music

        # Create volume control button
        self.sound_volume_label = ctk.StringVar(value=f"Volume {int(self.volume * 100)}%")

        # Set up UI elements
        self.create_widgets()

    def set_speed(self, value):
        """Set the volume based on the slider value and update the label."""
        volume = int(value)  # Convert the string value to float
        # Update the sound volume label
        self.settings["simulation_speed"] = volume


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
        self.control_frame = ctk.CTkFrame(self.root, fg_color=self.colors["background"],width=self.panel_size, corner_radius=10)
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
            ("Reset to Initial", self.reset_to_initial),
            ("Settings", self.open_settings),
            ("Save Pattern", self.save_pattern),
            ("Zoom In", self.zoom_in),
            ("Zoom Out", self.zoom_out),
            ("Reset Zoom", self.reset_zoom),
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
        self.volume_slider.pack(side=ctk.TOP, padx=10, pady=5)

        # Volume label
        self.volume_label = ctk.CTkLabel(self.control_frame, font=("System", 18), textvariable=self.sound_volume_label)
        self.volume_label.pack(side=ctk.TOP, padx=10, pady=5)


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
        self.pattern_dropdown.pack(side="bottom", pady=30)  # Adjust padding as necessary

        self.speeed_slider = ctk.CTkSlider(self.control_frame, from_=1, to=500, command=self.set_speed)
        self.speeed_slider.set(self.settings["simulation_speed"])  # Set initial volume
        self.speeed_slider.pack(side=ctk.TOP, padx=10, pady=5)

        # Optional: If you want to add a resolution entry below the dropdown
        # self.resolution_entry = ctk.CTkEntry(self.dropdown_frame, width=100)
        # self.resolution_entry.insert(0, "0.1")
        # self.resolution_entry.pack(pady=5)  # Adjust padding as necessary

    def open_settings(self):
        self.settings_window.open()

    def save_pattern(self):
        """ Save the current pattern to the patterns dictionary."""
        pattern_name = simpledialog.askstring("Save Pattern", "Enter a name for your pattern:")
        if pattern_name:
            # Check if the pattern name already exists
            if pattern_name in self.patterns:
                # Show an error message
                messagebox.showerror("Error", f"Pattern '{pattern_name}' already exists. Please choose a different name.")
            else:
                matrix_range = self.game.get_matrix_range(self.grid_rows, self.grid_cols)

                if matrix_range is None:
                    messagebox.showerror("Error", f"Please give a valid pattern\nThe grid is empty")
                    return

                self.patterns[pattern_name] = [
                    row[matrix_range["left"]:matrix_range["right"] + 1]
                    for row in
                    self.game.grid[matrix_range["top"]:matrix_range["bottom"] + 1]
                    ]
                self.save_patterns()
                self.pattern_dropdown['menu'].add_command(label=pattern_name, command=lambda value=pattern_name: self.load_pattern(value))
    
    def get_current_grid_state(self):
        """Retrieve the current state of the grid (alive/dead cells)."""
        return [[self.game.grid[row][col] for col in range(self.grid_cols)] for row in range(self.grid_rows)]

    def apply_grid_state(self, saved_state):
        """Apply the previously saved grid state back to the game grid."""
        for row in range(min(len(saved_state), self.grid_rows)):
            for col in range(min(len(saved_state[row]), self.grid_cols)):
                self.game.grid[row][col] = saved_state[row][col]  # Restore the cell state
        self.grid_canvas.draw_grid()  # Redraw the grid with the updated states
    
    def zoom_in(self):
        """Zoom in by increasing the square size and redrawing the grid."""
        if self.settings["square_size"] < 50:  # Set a maximum square size
            saved_state = self.get_current_grid_state()  # Save the current grid state
            self.settings["square_size"] += 5  # Increment square size
            self.update_grid()  # Update the grid size and redraw
            self.apply_grid_state(saved_state)  # Restore the saved state

    def zoom_out(self):
        """Zoom out by decreasing the square size and redrawing the grid."""
        if self.settings["square_size"] > 5:  # Set a minimum square size
            saved_state = self.get_current_grid_state()  # Save the current grid state
            self.settings["square_size"] -= 5  # Decrease square size
            self.update_grid()  # Update the grid size and redraw
            self.apply_grid_state(saved_state)  # Restore the saved state

    
    def reset_zoom(self):
        """Reset the zoom level to the default square size."""
        saved_state = self.get_current_grid_state()  # Save the current grid state
        self.settings["square_size"] = self.default_square_size  # Reset square size to default
        self.update_grid()  # Update the grid size and redraw
        self.apply_grid_state(saved_state)  # Restore the saved state
    
    def update_grid(self):
        self.grid_width = self.width - self.panel_size
        self.grid_height = self.height

        # Update the number of rows and columns based on the new square size
        self.grid_rows = self.grid_height // self.settings['square_size']
        self.grid_cols = self.grid_width // self.settings['square_size']

        # Update the canvas size to reflect the new grid dimensions
        self.grid_canvas.update_canvas_size(self.grid_width, self.grid_height)

        # Reinitialize the game grid with the new dimensions
        self.game = GameOfLife(self.grid_rows, self.grid_cols)
        
        self.grid_canvas.draw_grid()  # Redraw the grid


    def start_drag(self, event):
        """Called when the user presses the mouse button to start dragging."""
        self.is_dragging = True
        self.drag_start_x = event.x  # Store the starting x-coordinate
        self.drag_start_y = event.y  # Store the starting y-coordinate

    def do_drag(self, event):
        """Called when the user is dragging the grid."""
        if self.is_dragging:
            # Calculate how much the cursor moved
            move_x = event.x - self.drag_start_x
            move_y = event.y - self.drag_start_y

            # Update grid offsets based on the movement
            self.grid_offset_x += move_x
            self.grid_offset_y += move_y

            # Store the new cursor position as the starting point for the next move
            self.drag_start_x = event.x
            self.drag_start_y = event.y

            # Redraw the grid with the new offset
            self.grid_canvas.draw_grid(self.grid_offset_x, self.grid_offset_y)

    def end_drag(self, event):
        """Called when the user releases the mouse button to stop dragging."""
        self.is_dragging = False

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
            current_cell = self.game.grid[row][col]
            color = "#ff00e2" if current_cell == 0 else "#191541"
            self.game.grid[row][col] = 1 if current_cell == 0 else 0
            self.grid_canvas.canvas.itemconfig(self.grid_canvas.cells[row][col], fill=color)

    def run(self):
        self.root.mainloop()  # Ensure this method exists to run the main loop

    def run_game(self):
        if hasattr(self, 'is_running') and self.is_running:  # Check if is_running is defined
            changed_cells = self.game.update_game_grid(self.grid_canvas)
            self.grid_canvas.update_grid(changed_cells, self.game.grid)
            self.root.after(self.settings["simulation_speed"], self.run_game)
    
    def validate_data_direcory(self):
        if not os.path.exists("data"):
            os.makedirs("data")

    def load_patterns(self):
        if not os.path.exists(self.PATTERNS_FILE):
            return
        with open(self.PATTERNS_FILE, "r") as file:
            self.patterns.update(json.load(file))
    
    def save_patterns(self):
        new_patterns = self.patterns.copy()
        for pattern in Patterns.patterns_names():
            new_patterns.pop(pattern, None)
        
        if len(new_patterns) == 0:
            return

        self.validate_data_direcory()
        with open(self.PATTERNS_FILE, "w") as file:
            json.dump(new_patterns, file)
        
    def load_pattern(self, patt):
        self.game.reset()
        self.game.load_pattern(self.patterns[patt], self.grid_rows, self.grid_cols)
        self.grid_canvas.draw_grid()
