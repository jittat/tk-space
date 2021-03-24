import math
from random import randint, random

import tkinter as tk

from gamelib import Sprite, GameApp, Text

from consts import *
from elements import Ship, Bullet, Enemy
from utils import random_edge_position, normalize_vector

class SpaceGame(GameApp):
    def init_game(self):
        self.ship = Ship(self, CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)

        self.elements.append(self.ship)

    def add_enemy(self):
        x, y = random_edge_position()
        vx, vy = normalize_vector(self.ship.x - x, self.ship.y - y)

        vx *= ENEMY_BASE_SPEED
        vy *= ENEMY_BASE_SPEED

        enemy = Enemy(self, x, y, vx, vy)
        self.elements.append(enemy)

    def pre_update(self):
        if random() < 0.1:
            self.add_enemy()

    def post_update(self):
        pass

    def on_key_pressed(self, event):
        if event.keysym == 'Left':
            self.ship.start_turn('LEFT')
        elif event.keysym == 'Right':
            self.ship.start_turn('RIGHT')
        elif event.char == ' ':
            self.ship.fire()

    def on_key_released(self, event):
        if event.keysym == 'Left':
            self.ship.stop_turn('LEFT')
        elif event.keysym == 'Right':
            self.ship.stop_turn('RIGHT')


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Space Shotting")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = SpaceGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
