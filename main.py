import math
from random import randint

import tkinter as tk

from gamelib import Sprite, GameApp, Text

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

UPDATE_DELAY = 33

class Ship(Sprite):
    def __init__(self, app, x, y):
        super().__init__(app, 'images/pacman.png', x, y)

    def update(self):
        pass


class SpaceGame(GameApp):
    def init_game(self):
        pass

    def pre_update(self):
        pass

    def post_update(self):
        pass

    def on_key_pressed(self, event):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Space Shotting")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = SpaceGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
