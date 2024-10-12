from os import system as run
from time import sleep

class Engine:
    old_board = None
    board = None
    board_size = None
    row_size = 0
    col_size = 0

    def get_surrending(board, i, j, rs, cs):
        r_start = i - 1 if i > 0 else 0
        c_start = j - 1 if j > 0 else 0
        r_end = i + 1 if i < rs - 1 else rs
        c_end = j + 1 if j < cs - 1 else cs

        count = -1 if board[i][j] == 1 else 0

        for row in board[r_start : r_end + 1]:
            for col in row[c_start : c_end + 1]:
                if col:
                    count += 1

        return count

    def starting_point(self, arr):
        self.old_board = arr
        self.board = arr
        self.row_size = len(arr)
        self.col_size = len(arr[0])

    def update_board(self):
        self.old_board = [[col for col in row] for row in self.board]
        br = self.old_board
        i = 0
        while i < self.row_size:
            j = 0
            while j < self.col_size:
                nb = self.get_surrending(br, i, j, self.row_size, self.col_size)
                if br[i][j] == 1 and (nb > 3 or nb < 2):
                    self.board[i][j] = 0
                elif br[i][j] == 0 and nb == 3:
                    self.board[i][j] = 1
                j += 1
            i += 1

    def start(self):
        try:
            while True:
                self.update_board()
        except KeyboardInterrupt:
            pass
