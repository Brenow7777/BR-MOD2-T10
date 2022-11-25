import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE, SCREEN, DEFAULT_TYPE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

GM_SP = 20


class Game:

    half_screen_height = SCREEN_HEIGHT // 2
    half_screen_width = SCREEN_WIDTH // 2

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.score = 0
        self.death_count = 0
        self.game_speed = GM_SP
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()


    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.score = 0
        self.game_speed = GM_SP
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running= False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self)

    def update_score(self):
        self.score += 1
        if self.score % 20 == 0:
            self.game_speed *= 1.02 

    def draw(self):
        self.clock.tick(FPS)
        SCREEN.fill((255, 255, 255)) #ffffff
        self.draw_background()
        self.player.draw(SCREEN)
        self.obstacle_manager.draw(SCREEN)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(SCREEN)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        SCREEN.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        SCREEN.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def txt_generate(self, text, screen_height, screen_width):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(f"{text}", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (screen_width, screen_height)
        SCREEN.blit(text, text_rect)

    def draw_score(self):
        self.txt_generate(f"Score: {self.score}", 50, 1000)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000)
            if time_to_show >= 0:
                self.txt_generate(f"{self.player.type.capitalize()} enabled for {time_to_show} seconds", 40, 500)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def handle_events_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN: # não confuda: K_DOWN
                self.run()

    def show_menu(self):
        SCREEN.fill((255, 255, 255))

        if self.death_count == 0:
            self.txt_generate("Press any key to start", self.half_screen_height, self.half_screen_width)
        else:
            SCREEN.blit(ICON, (self.half_screen_width - 45, self.half_screen_height - 140))
            self.txt_generate("Press any key to restart", self.half_screen_height, self.half_screen_width)
            self.txt_generate(f"Score: {self.score}", self.half_screen_height + 30, self.half_screen_width)
            self.txt_generate(f"Death count: {self.death_count}", self.half_screen_height + 60, self.half_screen_width)

        pygame.display.update()
        self.handle_events_menu()