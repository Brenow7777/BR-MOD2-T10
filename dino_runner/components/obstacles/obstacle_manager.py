import pygame
import random

from dino_runner.utils.constants import SCREEN
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird

Y_POS = 310
JUMP_VEL = 8.5

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        obstacle_type = [
            Cactus(),
            Bird(),
        ]

        if len(self.obstacles) == 0:
            self.obstacles.append(obstacle_type[random.randint(0,1)])

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up or game.player.speed_down:                   
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    break
                elif game.player.has_power_up and game.player.hammer:
                    self.obstacles.remove(obstacle)
                elif game.player.has_power_up and game.player.shield:
                    break

    def reset_obstacles(self):
        self.obstacles = []

    def draw(self, SCREEN):
        for obstacle in self.obstacles:
            obstacle.draw(SCREEN)