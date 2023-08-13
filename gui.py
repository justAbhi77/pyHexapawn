from tkinter import *
from helpers import *


class Gui(Tk):
    """
    Custom Tkinter selfdow class.
    """

    def __init__(self, title: str):
        """
        Constructor for custom Settings.
        """
        Tk.__init__(self)
        self.title(title)
        self.resizable(True, True)
        self.wpawn = PhotoImage(file='assets/white.gif')
        self.bpawn = PhotoImage(file='assets/black.gif')
        self.empty = PhotoImage(file='assets/empty.gif')
        self.tk.call('wm', 'iconphoto', self._w, self.bpawn)
        self.selectedPiece = None
        table = Frame(self)
        table.config(bg='black')
        table.pack(pady=10)

        columnname = Entry(table, fg='white', font=(
            'Arial', 16, 'bold'), justify='center')
        columnname.configure({"background": "Black", })
        columnname.grid(row=0, column=0)
        columnname.insert(index=END, string='Player')

        columnname = Entry(table, fg='white', font=(
            'Arial', 16, 'bold'), justify='center')
        columnname.configure({"background": "Black", })
        columnname.grid(row=0, column=1)
        columnname.insert(index=END, string='Ai')

        columnname = Entry(table, fg='white', font=(
            'Arial', 16, 'bold'), justify='center')
        columnname.configure({"background": "Black", })
        columnname.grid(row=1, column=0)
        columnname.insert(index=END, string='0')

        columnname = Entry(table, fg='white', font=(
            'Arial', 16, 'bold'), justify='center')
        columnname.configure({"background": "Black", })
        columnname.grid(row=1, column=1)
        columnname.insert(index=END, string='0')

        Button(self, text="Hello World", command=self.printHelp).pack(
            fill=BOTH, pady=10)

        Gameboard = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
        print(Gameboard)
        tile_frame = Frame(self)
        tile_frame.pack(padx=60, pady=(0, 60), expand=True)

        # Create game board tiles
        color = 'black'
        i = 0

        for row in range(3):
            for col in range(3):
                tile = myButton(tile_frame, text='{},{}'.format(row, col))
                tile.config(
                    relief=FLAT,
                    bg=color,
                    fg='white' if color == 'black' else 'black',
                    activebackground=color,
                    command=lambda row=row, col=col, tile=tile: self.player_selected(
                        row, col, tile),
                )
                tile.grid(column=col, row=row)
                Gameboard.append(tile)
                color = 'black' if color == 'white' else 'white'
                i += 1

                tile.group = Gameboard[row][col]

                if row == 0:
                    tile.config(image=self.bpawn)
                    tile.image = self.bpawn
                if row == 1:
                    tile.config(image=self.empty)
                    tile.image = self.empty
                if row == 2:
                    tile.config(image=self.wpawn)
                    tile.image = self.wpawn

        self.centerselfdow()

    def player_selected(self, row: int, col: int, tile: myButton):

        if tile.group != 0 and self.selectedPiece == None:
            print("selected piece at",row,col)
            self.selectedPiece = tile

        elif self.selectedPiece != None and tile.group != self.selectedPiece.group:
            print('move selected piece to', row, col)

            tile.config(image=self.selectedPiece.image)
            tile.image = self.selectedPiece.image
            self.selectedPiece.config(image=self.empty)
            self.selectedPiece.image = self.empty

            tile.group = self.selectedPiece.group

            self.selectedPiece.group = 0

            self.selectedPiece = None

    def printHelp(self):
        print('Hello World')

    def centerselfdow(self):
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
    selfdowobj = Gui(title="Hexapawn")
    selfdowobj.mainloop()
