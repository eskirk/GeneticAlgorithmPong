import pygame
import random


class Ball:
    def __init__(self, pos_x, pos_y, four_player=False):
        rect = pygame.Rect(pos_x, pos_y, 15, 15)
        self.bounds = rect
        if not four_player:
            self.vel_x = random.choice([-150, 150])
            self.vel_y = random.choice([-150, 150])
        else:
            self.vel_x = random.choice([-150, -100, 100, 150])
            self.vel_y = random.choice([-150, -100, 100, 150])
        self.last_hit = None

    def draw(self, display):
        pygame.draw.rect(display, (255, 0, 0), self.bounds)

    def move(self, delta):
        self.bounds = self.bounds.move(self.vel_x * delta, self.vel_y * delta)

    def get_position(self):
        return self.bounds.x, self.bounds.y

    def intersects_paddle(self, paddle1, paddle2):
        if self.bounds.x <= paddle1.bounds.x + paddle1.bounds.width \
                and paddle1.bounds.y <= self.bounds.y <= paddle1.bounds.y + paddle1.bounds.height \
                and self.last_hit != paddle1 \
                and self.behind_paddle():
            paddle1.contacts_ball += 1
            self.last_hit = paddle1
            return True
        elif self.bounds.x + self.bounds.width >= paddle2.bounds.x \
                and paddle2.bounds.y <= self.bounds.y <= paddle2.bounds.y + paddle2.bounds.height \
                and self.last_hit != paddle2 \
                and self.behind_paddle():
            paddle2.contacts_ball += 1
            self.last_hit = paddle2
            return True
        return False

    def intersects_top_paddle(self, paddle3, paddle4):
        if self.bounds.y <= paddle3.bounds.y + paddle3.bounds.height \
                and paddle3.bounds.x <= self.bounds.x <= paddle3.bounds.x + paddle3.bounds.width \
                and self.last_hit != paddle3:
            paddle3.contacts_ball += 1
            self.last_hit = paddle3
            return True
        elif self.bounds.y + self.bounds.width >= paddle4.bounds.y \
                and paddle4.bounds.x <= self.bounds.x <= paddle4.bounds.x + paddle4.bounds.width \
                and self.last_hit != paddle4:
            paddle4.contacts_ball += 1
            self.last_hit = paddle4
            return True
        return False

    def behind_paddle(self):
        if self.get_position()[0] < 40 or self.get_position()[0] > 610:
            return False
        return True

    def reset(self):
        from pong import PongGame
        self.bounds = pygame.Rect(PongGame.window_width / 2, PongGame.window_height / 2, 15, 15)
