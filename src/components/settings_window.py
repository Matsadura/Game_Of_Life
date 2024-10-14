import tkinter as tk
from tkinter import Toplevel, Scale, Label

class SettingsWindow:
    def __init__(self, main_window):
        self.main_window = main_window

    def open(self):
        settings_window = Toplevel(self.main_window.root)
        settings_window.title("Settings")

        # Grid size settings
        Label(settings_window, text="Number of Rows").pack()
        # self.rows_slider = Scale(settings_window, from_=self.main_window.min_grid_size, to=self.main_window.max_grid_size,
        #                          label="Rows", orient=tk.HORIZONTAL, command=self.update_grid)
        # self.rows_slider.set(self.main_window.settings["rows"])
        # self.rows_slider.pack()

        # Label(settings_window, text="Number of Columns").pack()
        # self.cols_slider = Scale(settings_window, from_=self.main_window.min_grid_size, to=self.main_window.max_grid_size,
        #                          label="Columns", orient=tk.HORIZONTAL, command=self.update_grid)
        # self.cols_slider.set(self.main_window.settings["cols"])
        # self.cols_slider.pack()

        # Square size settings
        Label(settings_window, text="Square Size").pack()
        self.square_size_slider = Scale(settings_window, from_=self.main_window.min_square_size, to=self.main_window.max_square_size,
                                         label="Square Size", orient=tk.HORIZONTAL, command=self.update_grid)
        self.square_size_slider.set(self.main_window.settings["square_size"])
        self.square_size_slider.pack()

        # Simulation speed settings
        Label(settings_window, text="Simulation Speed (ms)").pack()
        self.speed_slider = Scale(settings_window, from_=self.main_window.min_speed, to=self.main_window.max_speed,
                                  label="Speed", orient=tk.HORIZONTAL, command=self.update_speed)
        self.speed_slider.set(self.main_window.settings["simulation_speed"])
        self.speed_slider.pack()

    def update_grid(self, value):
        self.main_window.update_grid()

    def update_speed(self, value):
        self.main_window.update_speed()
