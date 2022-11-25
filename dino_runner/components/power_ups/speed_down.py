from dino_runner.utils.constants import CLOCK, SPEED_TYPE
from dino_runner.components.power_ups.power_up import PowerUp


class SpeedDown(PowerUp):
    def __init__(self):
        self.image = CLOCK
        self.type = SPEED_TYPE
        super().__init__(self.image, self.type)