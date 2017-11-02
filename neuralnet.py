import pygame

class NeuralNet:
    def __init__(self):
        self.fitness = -1

    def __gt__(self, other):
        return self.fitness > other.fitness

    def randomize(self):
        pass

    def draw(self, display):
        pygame.draw.rect(display, (0, 0, 255), self.bounds)

    def move_up(self, delta):
        self.bounds = self.bounds.move(0, -250 * delta)

    def move_down(self, delta):
        self.bounds = self.bounds.move(0, 250 * delta)

    def follow_ball(self, delta):
        if (self.ball.bounds.y + self.ball.bounds.width) > (self.bounds.y + self.bounds.height):
            if self.bounds.y + self.bounds.height < self.game.window_height:
                self.move_down(delta)
        elif (self.ball.bounds.y + self.ball.bounds.width) < (self.bounds.y + self.bounds.height):
            if self.bounds.y > 0:
                self.move_up(delta)

    def mutate(self):
        pass