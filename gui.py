from tkinter import *

class Gui(Tk):
    """
    Custom Tkinter selfdow class.
    """
    def __init__(self,title:str):
        """
        Constructor for custom Settings.
        """
        Tk.__init__(self)
        self.title(title)
        self.resizable(True, True)
        self.wpawn = PhotoImage(file='assets/white.gif')
        self.tk.call('wm', 'iconphoto', self._w, self.wpawn)
        self.centerselfdow()
    
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