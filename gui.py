from tkinter import *
from tkinter import messagebox
from helpers import *
import random

BOARDSIZE = 3
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

        self.playerWin = 0
        self.AIWin = 0

        self.ai_move_directions = (
            Position(-1, 0), Position(-1, 1), Position(-1, -1))
        self.player_move_directions = (
            Position(1, 0), Position(1, -1), Position(1, 1))

        self.direction_mapping = {
            AI: self.ai_move_directions,
            PLAYER: self.player_move_directions
        }

        self.valid_directions = self.player_move_directions + self.ai_move_directions

        self.current_player = PLAYER
        self.matchEnd = False

        self.create_score_board()
        self.create_game_board()
        self.center_window()

    def create_score_board(self):
        entries = [
            ("Player", "Ai"),
            (self.playerWin, self.AIWin)
        ]

        table = Frame(self)
        table.config(bg='black')
        table.pack(pady=10)

        self.playertext = None
        self.aitext = None

        for row, values in enumerate(entries):
            for col, text in enumerate(values):
                columnname = Entry(table, fg='white', font=(
                    'Arial', 16, 'bold'), justify='center')
                columnname.configure({"background": "Black"})
                columnname.grid(row=row, column=col)
                columnname.insert(index=END, string=text)

                if row == 1:
                    if col == 0:
                        self.playertext = columnname
                    else:
                        self.aitext = columnname

        Button(self, text="Start a New Match", command=self.print_help).pack(
            fill=BOTH, pady=10)

    def create_game_board(self):
        self.Gameboard = [[EMPTY] * BOARDSIZE for _ in range(BOARDSIZE)]
        self.boardtiles = [[None]*BOARDSIZE for _ in range(BOARDSIZE)]

        self.Player_units = []
        self.AI_units = []

        self.Gameboard_tile_frame = Frame(self)
        self.Gameboard_tile_frame.pack(padx=60, pady=(0, 60), expand=True)

        colors = ('black', 'white')

        for row in range(BOARDSIZE):
            for col in range(BOARDSIZE):
                tile = HexapawnButton(
                    self.Gameboard_tile_frame, text='{},{}'.format(row, col))
                tile_color = colors[(row + col) % 2]
                text_color = 'white' if tile_color == 'black' else 'black'

                tile.config(
                    relief=FLAT,
                    bg=tile_color,
                    fg=text_color,
                    activebackground=tile_color,
                    command=lambda row=row, col=col, tile=tile: self.player_selected(
                        row, col, tile),
                )
                tile.grid(column=col, row=row)

                tile.position = Position(row, col)

                if row == 0:
                    self.initialize_unit(
                        tile, AI, self.bpawn, self.AI_units, id=row+col)
                elif row == BOARDSIZE - 1:
                    self.initialize_unit(
                        tile, PLAYER, self.wpawn, self.Player_units, id=row+col)
                else:
                    self.initialize_unit(tile, EMPTY, self.empty, id=row+col)

    def initialize_unit(self, tile: HexapawnButton, group, image, unit_list=None, id=EMPTY):
        tile.group = group
        tile.config(image=image)
        tile.image = image
        tile.id = id
        self.Gameboard[tile.position.x][tile.position.y] = group

        self.boardtiles[tile.position.x][tile.position.y] = tile

        if unit_list is not None:
            unit_list.append(tile)

    def player_selected(self, row: int, col: int, tile: HexapawnButton):
        if self.matchEnd:
            return
        if self.selectedPiece is None:
            self.handle_selection(row, col, tile)
        else:
            if tile.group != self.selectedPiece.group:
                self.handle_move(row, col, tile)
                self.selectedPiece = None
                self.ai_move_pieces()
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

        if direction in self.valid_directions:
            target_group = self.Gameboard[row][col]

            if direction == self.player_move_directions[0] or direction == self.ai_move_directions[0]:
                if target_group == EMPTY:
                    self.move_piece(row, col, tile)
                else:
                    print(
                        f'Invalid move for selected piece at {self.selectedPiece.position}, Deselected')
            else:
                if target_group == -self.selectedPiece.group:
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
            print(f'Captured piece at ({row}, {col}), Deselected')
            self.capture_unit(tile)

        self.update_tile_image(tile, self.selectedPiece.image)
        self.update_tile_image(self.selectedPiece, self.empty)

        self.update_tile_group(
            tile, self.selectedPiece.group, self.selectedPiece.id)

        self.update_gameboard(row, col, tile)

        self.update_player_units_after_move(self.selectedPiece, tile)
        self.current_player = -self.current_player
        self.checkWin(row)
        self.update_tile_group(self.selectedPiece, EMPTY, EMPTY)

    def capture_unit(self, tile):
        if tile.group == PLAYER:
            self.Player_units.remove(tile)
        else:
            self.AI_units.remove(tile)

    def update_tile_image(self, tile, image):
        tile.config(image=image)
        tile.image = image

    def update_tile_group(self, tile, group, id):
        tile.group = group
        tile.id = id

    def update_gameboard(self, row, col, tile):
        self.Gameboard[row][col] = tile.group
        self.Gameboard[self.selectedPiece.position.x][self.selectedPiece.position.y] = EMPTY

    def update_player_units_after_move(self, source_tile, target_tile):
        if source_tile in self.Player_units:
            self.Player_units.remove(source_tile)
            self.Player_units.insert(0, target_tile)
        elif source_tile in self.AI_units:
            self.AI_units.remove(source_tile)
            self.AI_units.insert(0, target_tile)

    def checkWin(self, row):
        print('gameboard after move is')
        for boardrow in self.Gameboard:
            print(boardrow)

        if row == 0 or row == BOARDSIZE-1:
            winner = None
            if self.selectedPiece.group == PLAYER:
                winner = 'Player'
                self.playerWin += 1
                self.playertext.delete(0, END)
                self.playertext.insert(0, self.playerWin)
            else:
                winner = 'AI'
                self.AIWin += 1
                self.aitext.delete(0, END)
                self.aitext.insert(0, self.AIWin)
            print(f'{winner} won by conquer')
            self.matchEnd = True
            messagebox.showinfo('Match End', f'{winner} won by conquer')
            return True
        elif self.current_player == PLAYER:
            if not self.has_moveable_unit(self.Player_units):
                print('AI Wins')
                self.matchEnd = True
                self.AIWin += 1
                self.aitext.delete(0, END)
                self.aitext.insert(0, self.AIWin)
                messagebox.showinfo('Match End', 'AI Wins')
                return True
        else:
            if not self.has_moveable_unit(self.AI_units):
                print('Player Wins')
                self.matchEnd = True
                self.playerWin += 1
                self.playertext.delete(0, END)
                self.playertext.insert(0, self.playerWin)
                messagebox.showinfo('Match End', 'Player Wins')
                return True
        return False

    def has_moveable_unit(self, units: list[HexapawnButton]) -> bool:
        result = False

        for unit in units:
            print(unit.position)
            direction = self.direction_mapping[unit.group]

            possible_position = unit.position - direction[0]

            if not (0 <= possible_position.x < BOARDSIZE and 0 <= possible_position.y < BOARDSIZE):
                pass

            elif self.Gameboard[possible_position.x][possible_position.y] == EMPTY:
                result = True
                break

            possible_position = unit.position - direction[1]

            if not (0 <= possible_position.x < BOARDSIZE and 0 <= possible_position.y < BOARDSIZE):
                pass

            elif self.Gameboard[possible_position.x][possible_position.y] == -unit.group:
                result = True
                break

            possible_position = unit.position - direction[2]

            if not (0 <= possible_position.x < BOARDSIZE and 0 <= possible_position.y < BOARDSIZE):
                pass

            elif self.Gameboard[possible_position.x][possible_position.y] == -unit.group:
                result = True
                break

        return result

    def ai_move_pieces(self):

        if self.current_player != AI:
            return

        print("AI thinking")
        possibleunits = self.AI_units.copy()

        for unit in possibleunits:
            if not self.has_moveable_unit([unit]):
                possibleunits.remove(unit)
        print("Possible units")
        for unit in possibleunits:
            print(unit.position)

        if not possibleunits:
            return

        aiunitselection = random.choice(possibleunits)

        aiunitselection.invoke()

        direction = self.direction_mapping[aiunitselection.group]

        possible_positions = []
        possible_position = aiunitselection.position - direction[0]
        print(possible_position)

        if not (0 <= possible_position.x < BOARDSIZE and 0 <= possible_position.y < BOARDSIZE):
            pass

        elif self.Gameboard[possible_position.x][possible_position.y] == EMPTY:
            possible_positions.append(possible_position)

        possible_position = aiunitselection.position - direction[1]
        print(possible_position)

        if not (0 <= possible_position.x < BOARDSIZE and 0 <= possible_position.y < BOARDSIZE):
            pass

        elif self.Gameboard[possible_position.x][possible_position.y] == -unit.group:
            possible_positions.append(possible_position)

        possible_position = aiunitselection.position - direction[2]
        print(possible_position)

        if not (0 <= possible_position.x < BOARDSIZE and 0 <= possible_position.y < BOARDSIZE):
            pass

        elif self.Gameboard[possible_position.x][possible_position.y] == -unit.group:
            possible_positions.append(possible_position)

        if not possible_positions:
            return
        possible_position = random.choice(possible_positions)

        self.aimovedPiece = aiunitselection.id
        self.aimovedPosition = possible_position

        self.boardtiles[possible_position.x][possible_position.y].invoke()

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

    def print_help(self):
        self.Gameboard_tile_frame.destroy()
        self.matchEnd = False
        self.create_game_board()
        self.current_player = PLAYER
        self.center_window()


if __name__ == "__main__":
    hexapawn_obj = HexapawnGUI(title="Hexapawn")
    hexapawn_obj.mainloop()
