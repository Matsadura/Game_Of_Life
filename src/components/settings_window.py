import customtkinter as ctk

class SettingsWindow:
    def __init__(self, main_window):
        self.main_window = main_window
        self.settings_window = ctk.CTkToplevel(self.main_window.root)
        self.settings_window.title("Settings")
        
        self.create_widgets()

    def create_widgets(self):
        # Add widgets for setting rows, columns, square size, and speed
        self.rows_label = ctk.CTkLabel(self.settings_window, text="Rows:")
        self.rows_label.grid(row=0, column=0, padx=5, pady=5)

        self.rows_entry = ctk.CTkEntry(self.settings_window)
        self.rows_entry.grid(row=0, column=1, padx=5, pady=5)
        self.rows_entry.insert(0, str(self.main_window.settings["rows"]))

        self.cols_label = ctk.CTkLabel(self.settings_window, text="Cols:")
        self.cols_label.grid(row=1, column=0, padx=5, pady=5)

        self.cols_entry = ctk.CTkEntry(self.settings_window)
        self.cols_entry.grid(row=1, column=1, padx=5, pady=5)
        self.cols_entry.insert(0, str(self.main_window.settings["cols"]))

        self.square_size_label = ctk.CTkLabel(self.settings_window, text="Square Size:")
        self.square_size_label.grid(row=2, column=0, padx=5, pady=5)

        self.square_size_entry = ctk.CTkEntry(self.settings_window)
        self.square_size_entry.grid(row=2, column=1, padx=5, pady=5)
        self.square_size_entry.insert(0, str(self.main_window.settings["square_size"]))

        self.simulation_speed_label = ctk.CTkLabel(self.settings_window, text="Simulation Speed:")
        self.simulation_speed_label.grid(row=3, column=0, padx=5, pady=5)

        self.simulation_speed_entry = ctk.CTkEntry(self.settings_window)
        self.simulation_speed_entry.grid(row=3, column=1, padx=5, pady=5)
        self.simulation_speed_entry.insert(0, str(self.main_window.settings["simulation_speed"]))

        self.save_button = ctk.CTkButton(self.settings_window, text="Save", command=self.save_settings)
        self.save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def show(self):
        self.settings_window.deiconify()

    def hide(self):
        self.settings_window.withdraw()

    def save_settings(self):
        # Update main window settings
        self.main_window.settings["rows"] = int(self.rows_entry.get())
        self.main_window.settings["cols"] = int(self.cols_entry.get())
        self.main_window.settings["square_size"] = int(self.square_size_entry.get())
        self.main_window.settings["simulation_speed"] = int(self.simulation_speed_entry.get())
        
        # Call the update function in main window
        self.main_window.update_grid()
        self.hide()
