#!/usr/bin/env python3
""" John Conways Game of Life """
import tkinter as tk
from src.components.main_window import GameOfLifeMainWindow

if __name__ == "__main__":
    game_gui = GameOfLifeMainWindow()
    game_gui.run()
