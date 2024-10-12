#!/usr/bin/env python3
import customtkinter as ctk
from src.components.main_window import GameOfLifeMainWindow

if __name__ == "__main__":
    app = GameOfLifeMainWindow()
    app.root.mainloop()
