from tkinter import Button

class Position:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
    
    def __sub__ (self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Position(x, y)

    def __eq__(self, other_position: object) -> bool:
        if isinstance(other_position, Position):
            return self.x == other_position.x and self.y == other_position.y
        return False

    def __str__(self) -> str:
        return f"({self.x},{self.y})"


class HexapawnButton(Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.group = 0
        self.position:Position = Position()
