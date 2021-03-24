import math
from random import randint

import tkinter as tk

from gamelib import Sprite, GameApp, Text

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

UPDATE_DELAY = 33

SHIP_SPEED = 5
SHIP_TURN_ANGLE = 5
BULLET_BASE_SPEED = 10

def direction_to_dxdy(direction):
    return (math.cos(direction * math.pi / 180), 
        math.sin(direction * math.pi / 180))


class Bullet(Sprite):
    def __init__(self, app, x, y, vx, vy):
        super().__init__(app, 'images/bullet1.png', x, y)
        self.vx = vx
        self.vy = vy

    def update(self):
        self.x += self.vx
        self.y += self.vy


class Ship(Sprite):
    def __init__(self, app, x, y):
        super().__init__(app, 'images/ship.png', x, y)

        self.app = app

        self.direction = 0
        self.is_turning_left = False
        self.is_turning_right = False

    def update(self):
        dx,dy = direction_to_dxdy(self.direction)

        self.x += dx * SHIP_SPEED
        self.y += dy * SHIP_SPEED

        if self.is_turning_left:
            self.turn_left()
        elif self.is_turning_right:
            self.turn_right()

    def start_turn(self, dir):
        if dir.upper() == 'LEFT':
            self.is_turning_left = True
            self.is_turning_right = False
        else:
            self.is_turning_right = True
            self.is_turning_left = False

    def stop_turn(self, dir=None):
        if (dir == None) or (dir.upper() == 'LEFT'):
            self.is_turning_left = False
        if (dir == None) or (dir.upper() == 'RIGHT'):
            self.is_turning_right = False

    def turn_left(self):
        self.direction -= SHIP_TURN_ANGLE

    def turn_right(self):
        self.direction += SHIP_TURN_ANGLE

    def fire(self):
        dx,dy = direction_to_dxdy(self.direction)
        bullet = Bullet(self.app, self.x, self.y, dx * BULLET_BASE_SPEED, dy * BULLET_BASE_SPEED)
        self.app.elements.append(bullet)


class SpaceGame(GameApp):
    def init_game(self):
        self.ship = Ship(self, CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)

        self.elements.append(self.ship)

    def pre_update(self):
        pass

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
