#!/usr/bin/env python3
""" John Conway’s Game of Life """
from src.main_window import MainWindow
import sys


app = MainWindow()


if __name__ == '__main__':
    sys.setrecursionlimit(1500)
    app.mainloop()
