import sys
import pygame

from ball import Ball
from paddle import Paddle, AIPaddle, NNPaddle, SidewaysNNPaddle


class PongGame:
    window_width = 650
    window_height = 500

    def __init__(self, four_player=False):
        self.ball = Ball(PongGame.window_width / 2, PongGame.window_height / 2)
        self.paddle1 = NNPaddle(PongGame.window_width - 50, PongGame.window_height / 2, self.ball, self)
        self.paddle2 = AIPaddle(50, PongGame.window_height / 2, self.ball, self)
        self.paddle3 = None
        self.paddle4 = None

        self.temp_paddle = None
        self.four_player = four_player

        self.winner = None
        self.game_over = False
        self.speed = 1000
        self.scores = [0, 0]
        self.timeout = 0
        self.pause = False

        if self.four_player:
            PongGame.window_width = 650
            PongGame.window_height = 650

            self.ball = Ball(PongGame.window_width / 2, PongGame.window_height / 2)
            self.scores = [0, 0, 0, 0]
            self.paddle1 = NNPaddle(PongGame.window_width - 50, PongGame.window_height / 2, self.ball, self, True)
            self.paddle2 = NNPaddle(50, PongGame.window_height / 2, self.ball, self, True)
            self.paddle3 = SidewaysNNPaddle(PongGame.window_width / 2, PongGame.window_height - 50, self.ball, self)
            self.paddle4 = SidewaysNNPaddle(PongGame.window_width / 2, 50, self.ball, self)

    def start_game(self):
        pygame.init()

        clock = pygame.time.Clock()
        display = pygame.display.set_mode((PongGame.window_width, PongGame.window_height))

        pygame.display.set_caption('Neural Net Pong')

        while not self.game_over:
            delta = clock.tick(60) / self.speed
            display.fill((255, 255, 255))

            # listen for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.handle_input(delta)
            if not self.four_player:
                self.game_over = self.handle_off_screen()
            else:
                self.game_over = self.handle_off_screen_four_player()

            if not self.game_over:
                self.handle_collisions()

            self.paddle1.follow_ball(delta)
            self.paddle2.follow_ball(delta)
            if self.paddle3 is not None and self.paddle4 is not None:
                self.paddle3.follow_ball(delta)
                self.paddle4.follow_ball(delta)

            self.ball.move(delta)

            self.draw(display)
            if self.timeout < 100:
                self.timeout += 1
            if self.pause:
                self.reset()
            pygame.display.flip()

    def draw(self, display):
        self.paddle1.draw(display)
        self.paddle2.draw(display)
        if self.paddle3 is not None and self.paddle4 is not None:
            self.paddle3.draw(display)
            self.paddle4.draw(display)

        self.ball.draw(display)
        font = pygame.font.Font(None, 25)
        score = font.render(self.paddle2.name + ' | ' + str(self.scores[1]) + ' - ' + str(self.scores[0]) + ' | ' +
                            self.paddle1.name, True, (0, 0, 0))
        info = font.render('Generation ' + str(self.paddle1.generation), True, (0, 0, 0))
        rect = score.get_rect(center=(325, 60))
        info_rect = info.get_rect(center=(325, 90))
        display.blit(score, rect)
        display.blit(info, info_rect)

    def handle_input(self, delta):
        # listen for key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.paddle2.bounds.y > 0:
            self.paddle2.move_up(delta)
        if keys[pygame.K_DOWN] and self.paddle2.bounds.y + self.paddle2.bounds.height < PongGame.window_height:
            self.paddle2.move_down(delta)
        if keys[pygame.K_RIGHT] and self.speed > 10:
                self.speed -= 10
        if keys[pygame.K_LEFT] and self.speed < 1000000:
                self.speed += 10
        if keys[pygame.K_r]:
            self.reset()
        if keys[pygame.K_SPACE] and self.timeout == 100:
            self.timeout = 0
            if self.paddle2.name != 'Player':
                self.temp_paddle = self.paddle2
                self.paddle2 = Paddle(50, PongGame.window_height / 2)
                self.paddle2.score = self.scores[0]
            else:
                self.paddle2 = self.temp_paddle
        if keys[pygame.K_p] and self.timeout == 100:
            if not self.pause:
                self.pause = True
            else:
                self.pause = False

    def handle_collisions(self):
        # collision with paddle
        if self.ball.intersects_paddle(self.paddle2, self.paddle1):
            self.ball.vel_x = -self.ball.vel_x
            self.ball.vel_x *= 1.05
            self.ball.vel_y *= 1.05
        elif self.four_player and self.ball.intersects_top_paddle(self.paddle4, self.paddle3):
            self.ball.vel_y = -self.ball.vel_y
            self.ball.vel_x *= 1.05
            self.ball.vel_y *= 1.05
        # collision with ceiling
        if not self.four_player:
            if (self.ball.bounds.y <= 0 and self.ball.vel_y < 0) or (self.ball.bounds.y + self.ball.bounds.height >= PongGame.window_height and self.ball.vel_y > 0):
                self.ball.vel_y = -self.ball.vel_y

    def handle_off_screen_four_player(self):
        if self.paddle1.score >= 6:
            self.winner = self.paddle1
            return True
        elif self.paddle2.score >= 6:
            self.winner = self.paddle2
            return True
        elif self.paddle3.score >= 6:
            self.winner = self.paddle3
            return True
        elif self.paddle4.score >= 6:
            self.winner = self.paddle4
            return True

        if self.ball.bounds.x + self.ball.bounds.width > PongGame.window_width or self.ball.bounds.x <= 0:
            if self.ball.bounds.x <= 0:
                self.paddle1.score += 1
                self.paddle1.fitness += 10
                self.scores[0] += 1
            elif self.ball.bounds.x >= PongGame.window_width:
                self.paddle2.score += 1
                self.paddle2.fitness += 10
                self.scores[1] += 1

            self.ball = Ball(PongGame.window_width / 2, PongGame.window_height / 2)
            self.paddle1.reset(PongGame.window_width - 50, PongGame.window_height / 2, self.ball)
            self.paddle2.reset(50, PongGame.window_height / 2, self.ball)
            self.paddle3.reset(PongGame.window_width / 2, PongGame.window_height - 50, self.ball)
            self.paddle4.reset(PongGame.window_width / 2, 50, self.ball)

        elif self.ball.bounds.y + self.ball.bounds.height > PongGame.window_height or self.ball.bounds.y <= 0:
            if self.ball.bounds.y <= 0:
                self.paddle3.score += 1
                self.paddle3.fitness += 10
                self.scores[2] += 1
            elif self.ball.bounds.y >= PongGame.window_height:
                self.paddle4.score += 1
                self.paddle4.fitness += 10
                self.scores[3] += 1

            self.ball = Ball(PongGame.window_width / 2, PongGame.window_height / 2)
            self.paddle1.reset(PongGame.window_width - 50, PongGame.window_height / 2, self.ball)
            self.paddle2.reset(50, PongGame.window_height / 2, self.ball)
            self.paddle3.reset(PongGame.window_width / 2, PongGame.window_height - 50, self.ball)
            self.paddle4.reset(PongGame.window_width / 2, 50, self.ball)
        return False

    def handle_off_screen(self):
        if self.paddle1.score >= 3:
            self.winner = self.paddle1
            return True
        elif self.paddle2.score >= 3:
            self.winner = self.paddle2
            return True
        
        if self.ball.bounds.x + self.ball.bounds.width > PongGame.window_width or self.ball.bounds.x <= 0:
            if self.ball.bounds.x <= 0:
                self.paddle1.score += 1
                self.paddle1.fitness += 10
                self.scores[0] += 1
            else:
                self.paddle2.score += 1
                self.paddle2.fitness += 10
                self.scores[1] += 1
            self.ball = Ball(PongGame.window_width / 2, PongGame.window_height / 2)
            self.paddle1.reset(PongGame.window_width - 50, PongGame.window_height / 2, self.ball)
            self.paddle2.reset(50, PongGame.window_height / 2, self.ball)
        return False

    def reset(self):
        self.ball.reset()
        self.paddle1.reset(PongGame.window_width - 50, PongGame.window_height / 2, self.ball)
        self.paddle1.fitness = 0
        self.paddle1.contacts_ball = 0
        self.paddle1.score = 0
        self.paddle2.reset(50, PongGame.window_height / 2, self.ball)
        self.paddle2.score = 0
        self.scores = [0, 0]


def main():
    PongGame()


if __name__ == '__main__':
    main()
