import random
import pygame

from dino_runner.utils.constants import HAMMER_TYPE, SHIELD_TYPE, SPEED_TYPE
from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.power_ups.speed_down import SpeedDown


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0

    def update(self, game):
        p_up_type = [
            Shield(),
            Hammer(),
            SpeedDown()
        ]

        if len(self.power_ups) == 0 and self.when_appears == game.score:
            self.when_appears += random.randint(200, 300) 
            self.power_ups.append(p_up_type[random.randint(0,2)])


        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)
            if game.player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                if power_up.type == SHIELD_TYPE:
                    game.player.shield = True
                    game.player.hammer = False
                    game.player.speed_down = False
                elif power_up.type == HAMMER_TYPE:
                    game.player.shield = False
                    game.player.hammer = True
                    game.player.speed_down = False
                if power_up.type == SPEED_TYPE:
                    game.player.speed_down = True
                    game.game_speed = 20
                game.player.has_power_up = True
                game.player.type = power_up.type
                game.player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)

    def draw(self, SCREEN):
        for power_up in self.power_ups:
            power_up.draw(SCREEN)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)