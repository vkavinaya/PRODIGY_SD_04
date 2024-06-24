import tkinter as tk
from tkinter import messagebox

class SudokuSolver:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sudoku Solver")
        self.window.geometry("500x550")
        self.window.configure(bg="#f0f0f0")
        self.cells = [[tk.Entry(self.window, width=2, font=("Arial", 24, "bold"), justify="center", 
                               highlightthickness=1, bd=0, bg='#d3d3d3') for _ in range(9)] for _ in range(9)]
        self.create_grid()
        self.solve_button = tk.Button(self.window, text="Solve", command=self.solve, bg="#4CAF50", fg="white",
                                      font=("Arial", 18, "bold"), width=10)
        self.solve_button.grid(row=9, column=0, columnspan=9, pady=20)
        self.window.mainloop()

    def create_grid(self):
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                top = 2 if i % 3 == 0 and i != 0 else 1
                left = 2 if j % 3 == 0 and j != 0 else 1
                bottom = 2 if i == 8 else 1
                right = 2 if j == 8 else 1
                cell.grid(row=i, column=j, padx=(left, right), pady=(top, bottom), ipadx=10, ipady=10)
        self.load_initial_puzzle()

    def load_initial_puzzle(self):
        # A sample 9x9 Sudoku puzzle (0 represents empty cells)
        initial_puzzle = [
            [5, 3, 4, 6, 7, 0, 0, 1, 2],
            [6, 0, 0, 1, 9, 5, 0, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 0, 0, 0, 6, 1, 4, 2, 3],
            [4, 0, 0, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 0, 0, 6],
            [0, 6, 0, 0, 3, 7, 2, 8, 4],
            [0, 0, 0, 4, 1, 9, 6, 3, 5],
            [0, 4, 5, 2, 8, 0, 0, 7, 9]
        ]

        for i in range(9):
            for j in range(9):
                if initial_puzzle[i][j] != 0:
                    self.cells[i][j].insert(0, str(initial_puzzle[i][j]))
                    self.cells[i][j].configure(state='disabled')  # Prevent editing of initial numbers

    def is_valid(self, board, row, col, num):
        for x in range(9):
            if board[row][x] == num or board[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve_sudoku(self, board):
        empty = self.find_empty_location(board)
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0
        return False

    def find_empty_location(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def get_board(self):
        board = []
        try:
            for row in range(9):
                board_row = []
                for col in range(9):
                    val = self.cells[row][col].get()
                    if val == "":
                        board_row.append(0)
                    else:
                        board_row.append(int(val))
                board.append(board_row)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers between 1 and 9.")
            return None
        return board

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, str(board[i][j]))

    def solve(self):
        board = self.get_board()
        if board is None:
            return  # Error already shown
        if self.solve_sudoku(board):
            self.set_board(board)
        else:
            messagebox.showerror("Error", "No solution exists for the given Sudoku")

if __name__ == "__main__":
    SudokuSolver()