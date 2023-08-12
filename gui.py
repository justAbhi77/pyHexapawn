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

        Gameboard = [[]*3]*3
        self.tile_frame = Frame(self)
        self.tile_frame.pack(padx=60, pady=(0, 60), expand=True)

        # Create game board tiles
        color = 'black'
        i = 0

        for row in range(3):
            for col in range(3):
                tile = myButton(self.tile_frame, text='{},{}'.format(row, col))
                tile.config(
                    relief=FLAT,
                    bg=color,
                    fg='white' if color == 'black' else 'black',
                    activebackground=color,
                    command=lambda row=row, col=col, tile=tile: self.player_selected(
                        row, col, tile)
                )
                tile.grid(column=col, row=row)
                Gameboard.append(tile)
                color = 'black' if color == 'white' else 'white'
                i += 1

                if row == 0:
                    tile.config(image=self.bpawn)
                    tile.image = self.wpawn
                    tile.isAIpiece = True
                if row == 1:
                    tile.config(image=self.empty)
                    tile.image = self.empty
                if row == 2:
                    tile.config(image=self.wpawn)
                    tile.image = self.bpawn
                    tile.isplayerpiece = True

        self.centerselfdow()

    def player_selected(self, row: int, col: int, tile: myButton):
        if tile.isplayerpiece and self.selectedPiece == None:
            self.selectedPiece = tile
        if not tile.isplayerpiece and not tile.isAIpiece and self.selectedPiece != None:
            self.selectedPiece.grid(column=col, row=row)

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
