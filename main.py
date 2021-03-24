import math
from random import randint, random

import tkinter as tk

from gamelib import Sprite, GameApp, Text

from consts import *
from elements import Ship, Bullet, Enemy
from utils import random_edge_position, normalize_vector, direction_to_dxdy, vector_len, distance


class SpaceGame(GameApp):
    def init_game(self):
        self.ship = Ship(self, CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)

        self.score = 0
        self.score_wait = 0

        self.score_text = Text(self, 'Score: XX', 100, 20)

        self.elements.append(self.ship)
        self.elements.append(self.score_text)

        self.enemies = []
        self.bullets = []


    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def bullet_count(self):
        return len(self.bullets)

    def update_score(self):
        self.score_wait += 1
        if self.score_wait >= SCORE_WAIT:
            self.score += 1
            self.score_text.set_text(f'Score: {self.score}')
            self.score_wait = 0


    def update_score_text(self):
        self.score_text.set_text(f'Score: {self.score}')


    def create_enemy_star(self):
        enemies = []

        x = randint(100, CANVAS_WIDTH - 100)
        y = randint(100, CANVAS_HEIGHT - 100)

        while vector_len(x - self.ship.x, y - self.ship.y) < 200:
            x = randint(100, CANVAS_WIDTH - 100)
            y = randint(100, CANVAS_HEIGHT - 100)

        for d in range(18):
            dx, dy = direction_to_dxdy(d * 20)
            enemy = Enemy(self, x, y, dx * ENEMY_BASE_SPEED, dy * ENEMY_BASE_SPEED)
            enemies.append(enemy)

        return enemies


    def create_enemy_from_edges(self):
        x, y = random_edge_position()
        vx, vy = normalize_vector(self.ship.x - x, self.ship.y - y)

        vx *= ENEMY_BASE_SPEED
        vy *= ENEMY_BASE_SPEED

        enemy = Enemy(self, x, y, vx, vy)
        return [enemy]


    def create_enemies(self):
        if random() < 0.2:
            enemies = self.create_enemy_star()
        else:
            enemies = self.create_enemy_from_edges()

        for e in enemies:
            self.add_enemy(e)

    def pre_update(self):
        if random() < 0.1:
            self.create_enemies()

    def process_bullet_enemy_collisions(self):
        for b in self.bullets:
            for e in self.enemies:
                if b.is_hit_enemy(e):
                    b.to_be_deleted = True
                    e.to_be_deleted = True

    def process_ship_enemy_collision(self):
        for e in self.enemies:
            if self.ship.is_hit_enemy(e):
                self.stop_animation()

    def process_collisions(self):
        self.process_bullet_enemy_collisions()
        self.process_ship_enemy_collision()

    def update_and_filter_deleted(self, elements):
        new_list = []
        for e in elements:
            e.update()
            e.render()
            if e.to_be_deleted:
                e.delete()
            else:
                new_list.append(e)
        return new_list

    def post_update(self):
        self.process_collisions()

        self.bullets = self.update_and_filter_deleted(self.bullets)
        self.enemies = self.update_and_filter_deleted(self.enemies)

        self.update_score()

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
    root.title("Space Fighter")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = SpaceGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
