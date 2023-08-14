from tkinter import *
from helpers import *

PLAYER = 1
EMPTY = 0
AI = -1


class HexapawnGUI(Tk):
    def __init__(self, title: str):
        super().__init__()
        self.title(title)
        self.resizable(True, True)
        self.wpawn = PhotoImage(file='assets/white.gif')
        self.bpawn = PhotoImage(file='assets/black.gif')
        self.empty = PhotoImage(file='assets/empty.gif')
        self.tk.call('wm', 'iconphoto', self._w, self.bpawn)
        self.selectedPiece = None

        self.ai_move_directions = (
            Position(-1, 0), Position(-1, 1), Position(-1, -1))
        self.player_move_directions = (
            Position(1, 0), Position(1, -1), Position(1, 1))

        self.current_player = PLAYER

        self.create_score_board()
        self.create_game_board()
        self.center_window()

    def create_score_board(self):
        entries = [
            ("Player", "Ai"),
            ("0", "0")
        ]

        table = Frame(self)
        table.config(bg='black')
        table.pack(pady=10)

        for row, values in enumerate(entries):
            for col, text in enumerate(values):
                columnname = Entry(table, fg='white', font=(
                    'Arial', 16, 'bold'), justify='center')
                columnname.configure({"background": "Black"})
                columnname.grid(row=row, column=col)
                columnname.insert(index=END, string=text)

        Button(self, text="Hello World", command=self.print_help).pack(
            fill=BOTH, pady=10)

    def create_game_board(self):
        self.Gameboard = [[AI, AI, AI], [
            EMPTY, EMPTY, EMPTY], [PLAYER, PLAYER, PLAYER]]

        tile_frame = Frame(self)
        tile_frame.pack(padx=60, pady=(0, 60), expand=True)

        colors = ('black', 'white')

        for row in range(3):
            for col in range(3):
                tile = HexapawnButton(
                    tile_frame, text='{},{}'.format(row, col))
                tile.config(
                    relief=FLAT,
                    bg=colors[(row + col) % 2],
                    fg='white' if colors[(row + col) %
                                         2] == 'black' else 'black',
                    activebackground=colors[(row + col) % 2],
                    command=lambda row=row, col=col, tile=tile: self.player_selected(
                        row, col, tile),
                )
                tile.grid(column=col, row=row)

                tile.group = self.Gameboard[row][col]
                tile.position.x = row
                tile.position.y = col

                if row == 0:
                    tile.config(image=self.bpawn)
                    tile.image = self.bpawn
                elif row == 2:
                    tile.config(image=self.wpawn)
                    tile.image = self.wpawn
                else:
                    tile.config(image=self.empty)
                    tile.image = self.empty

    def player_selected(self, row: int, col: int, tile: HexapawnButton):
        if self.selectedPiece is None:
            self.handle_selection(row, col, tile)
        else:
            if tile.group != self.selectedPiece.group:
                self.handle_move(row, col, tile)
            else:
                print('Deselected piece')
            self.selectedPiece = None

    def handle_selection(self, row: int, col: int, tile: HexapawnButton):
        if tile.group == EMPTY:
            return
        if tile.group == self.current_player:
            print(f'Selected piece at ({row}, {col})')
            self.selectedPiece = tile
        else:
            print(
                f'Selected piece is not of this Player, Current player is {self.current_player}')

    def handle_move(self, row: int, col: int, tile: HexapawnButton):
        direction = self.selectedPiece.position - tile.position

        if direction in self.player_move_directions or direction in self.ai_move_directions:
            if direction == self.player_move_directions[0] or direction == self.ai_move_directions[0]:
                if self.Gameboard[row][col] == EMPTY:
                    self.move_piece(row, col, tile)
                else:
                    print(
                        f'Invalid move for selected piece at {self.selectedPiece.position}, Deselected')
            else:
                if self.Gameboard[row][col] == -self.selectedPiece.group:
                    self.move_piece(row, col, tile)
                else:
                    print(
                        f'Invalid move for selected piece at {self.selectedPiece.position}, Deselected')
        else:
            print(
                f'Invalid move for selected piece at {self.selectedPiece.position}, Deselected')

    def move_piece(self, row: int, col: int, tile: HexapawnButton):
        print(
            f'Valid move for selected piece, move from {self.selectedPiece.position} to ({row}, {col})')
        if self.Gameboard[row][col] == -self.selectedPiece.group:
            print(f'Captured piece at {row}, {col}, Deselected')

        tile.config(image=self.selectedPiece.image)
        tile.image = self.selectedPiece.image
        self.selectedPiece.config(image=self.empty)
        self.selectedPiece.image = self.empty

        tile.group = self.selectedPiece.group
        self.Gameboard[row][col] = tile.group
        self.Gameboard[self.selectedPiece.position.x][self.selectedPiece.position.y] = EMPTY

        self.selectedPiece.group = EMPTY
        self.current_player = -self.current_player

    def print_help(self):
        print('Hello World')

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        frm_width = self.winfo_rootx() - self.winfo_x()
        self_width = width + 2 * frm_width
        height = self.winfo_height()
        titlebar_height = self.winfo_rooty() - self.winfo_y()
        self_height = height + titlebar_height + frm_width
        x = self.winfo_screenwidth() // 2 - self_width // 2
        y = self.winfo_screenheight() // 2 - self_height // 2
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))


if __name__ == "__main__":
    hexapawn_obj = HexapawnGUI(title="Hexapawn")
    hexapawn_obj.mainloop()
