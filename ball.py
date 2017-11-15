import pygame
import random


class Ball:
    def __init__(self, pos_x, pos_y):
        rect = pygame.Rect(pos_x, pos_y, 15, 15)
        self.bounds = rect
        self.vel_x = random.choice([-150, 150])
        self.vel_y = random.choice([-150, 150])
        self.last_hit = None

    def draw(self, display):
        pygame.draw.rect(display, (255, 0, 0), self.bounds)

    def move(self, delta):
        self.bounds = self.bounds.move(self.vel_x * delta, self.vel_y * delta)

    def get_position(self):
        return self.bounds.x, self.bounds.y

    def intersects_paddle(self, paddle2, paddle1):
        if self.bounds.x <= paddle2.bounds.x + paddle2.bounds.width \
                and paddle2.bounds.y <= self.bounds.y <= paddle2.bounds.y + paddle2.bounds.height\
                and self.last_hit != paddle2:
            paddle2.fitness += 1
            self.last_hit = paddle2
            return True
        elif self.bounds.x + self.bounds.width >= paddle1.bounds.x \
                and paddle1.bounds.y <= self.bounds.y <= paddle1.bounds.y + paddle1.bounds.height\
                and self.last_hit != paddle1:
            paddle1.fitness += 1
            self.last_hit = paddle1
            return True
        return False

    def reset(self):
        from pong import PongGame
        self.bounds = pygame.Rect(PongGame.window_width / 2, PongGame.window_height / 2, 15, 15)
