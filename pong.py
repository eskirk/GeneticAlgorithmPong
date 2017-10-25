import sys

import pygame

from ball import Ball
from paddle import Paddle
from neuralnet import AIPaddle


class PongGame:
    window_width = 500
    window_height = 500

    def __init__(self):
        # self.cpu_paddle = Paddle(50, PongGame.window_height / 2)
        self.human_paddle = Paddle(PongGame.window_width - 50, PongGame.window_height / 2)
        self.ball = Ball(PongGame.window_width / 2, PongGame.window_height / 2)
        self.cpu_paddle = AIPaddle(50, PongGame.window_height / 2, self.ball, self)
        self.temp_cpu_move_down = True

        self.start_game()

    def start_game(self):
        pygame.init()

        clock = pygame.time.Clock()
        display = pygame.display.set_mode((PongGame.window_width, PongGame.window_height))
        pygame.display.set_caption('Neural Net Pong')

        while True:
            delta = clock.tick(60) / 1000
            display.fill((255, 255, 255))

            # listen for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # listen for key presses
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.human_paddle.bounds.y > 0:
                self.human_paddle.move_up(delta)
            if keys[
                pygame.K_DOWN] and self.human_paddle.bounds.y + self.human_paddle.bounds.height < PongGame.window_height:
                self.human_paddle.move_down(delta)

            # super super advanced AI
            self.cpu_paddle.follow_ball(delta)

            # collision with human paddle
            if self.ball.bounds.x + self.ball.bounds.width >= self.human_paddle.bounds.x and self.human_paddle.bounds.y <= self.ball.bounds.y <= self.ball.bounds.y <= self.human_paddle.bounds.y + self.human_paddle.bounds.height:
                self.ball.vel_x = -self.ball.vel_x
                self.ball.vel_x *= 1.1
                self.ball.vel_y *= 1.1
            # collision with cpu paddle
            elif self.ball.bounds.x <= self.cpu_paddle.bounds.x + self.cpu_paddle.bounds.width and self.cpu_paddle.bounds.y <= self.ball.bounds.y <= self.ball.bounds.y <= self.cpu_paddle.bounds.y + self.human_paddle.bounds.height:
                self.ball.vel_x = -self.ball.vel_x
                self.ball.vel_x *= 1.1
                self.ball.vel_y *= 1.1
            # collision with ceiling
            elif self.ball.bounds.y <= 0:
                self.ball.vel_y = -self.ball.vel_y
            # collision with floor
            elif self.ball.bounds.y + self.ball.bounds.height >= PongGame.window_height:
                self.ball.vel_y = -self.ball.vel_y

            # off screen
            if self.ball.bounds.x + self.ball.bounds.width > PongGame.window_width or self.ball.bounds.x <= 0:
                self.ball = Ball(PongGame.window_width / 2, PongGame.window_height / 2)
                self.cpu_paddle = AIPaddle(50, PongGame.window_height / 2, self.ball, self)
            self.ball.move(delta)

            self.draw(display)
            pygame.display.flip()

    def key_down(self, event):
        self.human_paddle.move_down()

    def key_up(self, event):
        self.human_paddle.move_up()

    def draw(self, display):
        self.human_paddle.draw(display)
        self.cpu_paddle.draw(display)
        self.ball.draw(display)


def main():
    PongGame()


if __name__ == '__main__':
    main()
