import random

from dino_runner.utils.constants import BIRD
from dino_runner.components.obstacles.obstacle import Obstacle


class Bird(Obstacle):
    def __init__(self):
        super().__init__(BIRD, 0)
        
        if random.randint(0, 1) == 0:
            self.rect.y = 250
        else:
            self.rect.y = 320
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1