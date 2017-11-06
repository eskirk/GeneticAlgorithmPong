import pygame
from pong import PongGame


class Paddle:
    def __init__(self, x_pos, y_pos):
        self.bounds = pygame.Rect(x_pos, y_pos, 15, 100)

    def draw(self, display):
        pygame.draw.rect(display, (0, 0, 255), self.bounds)

    def move_up(self, delta):
        self.bounds = self.bounds.move(0, -250 * delta)

    def move_down(self, delta):
        self.bounds = self.bounds.move(0, 250 * delta)

    def reset(self):
        self.bounds = pygame.Rect(PongGame.window_width - 50, PongGame.window_height / 2, 15, 100)





