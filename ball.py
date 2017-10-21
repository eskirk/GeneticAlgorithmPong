import pygame
import random


class Ball:
    def __init__(self, pos_x, pos_y):
        self.bounds = pygame.Rect(pos_x, pos_y, 15, 15)
        self.vel_x = random.choice([-150, 150])
        self.vel_y = random.choice([-150, 150])

    def draw(self, display):
        pygame.draw.rect(display, (255, 0, 0), self.bounds)

    def move(self, delta):
        self.bounds = self.bounds.move(self.vel_x * delta, self.vel_y * delta)
