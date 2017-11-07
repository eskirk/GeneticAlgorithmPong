import pygame
import random


class Ball:
    def __init__(self, pos_x, pos_y):
        rect = pygame.Rect(pos_x, pos_y, 15, 15)
        self.bounds = rect
        self.vel_x = random.choice([-150, 150])
        self.vel_y = random.choice([-150, 150])

    def draw(self, display):
        pygame.draw.rect(display, (255, 0, 0), self.bounds)

    def move(self, delta):
        self.bounds = self.bounds.move(self.vel_x * delta, self.vel_y * delta)

    def get_position(self):
        return self.bounds.x, self.bounds.y

    def intersects_paddle(self, cpu_paddle, human_paddle):
        if (self.bounds.x <= cpu_paddle.bounds.x + cpu_paddle.bounds.width and cpu_paddle.bounds.y <= self.bounds.y <= cpu_paddle.bounds.y + cpu_paddle.bounds.height):
            # cpu_paddle.score += 1
            return True
        elif (self.bounds.x + self.bounds.width >= human_paddle.bounds.x and human_paddle.bounds.y <= self.bounds.y <= human_paddle.bounds.y + human_paddle.bounds.height):
            # human_paddle.score += 1
            return True
        return False

    def reset(self):
        from pong import PongGame
        self.bounds = pygame.Rect(PongGame.window_width / 2, PongGame.window_height / 2, 15, 15)
