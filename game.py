import pygame
from menu import MainMenu, OptionsMenu, CreditsMenu
import time
from level import LevelOne
from map import LevelOneMap

class Game():
    def __init__(self):
        pygame.init()
        self.running = True # When the application is running
        self.playing = False # When the game is actually being played
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False # START_KEY = ENTER
        self.I_KEY, self.M_KEY = False, False
        self.DISPLAY_H = 600
        self.DISPLAY_W = 600
        self.mid_width = self.DISPLAY_W/2
        self.mid_height = self.DISPLAY_H/2
        self.twelth_x = self.DISPLAY_W / 12
        self.twelth_y = self.DISPLAY_H / 12

        #Initialise window
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        pygame.display.set_caption("SOME COOL GAME NAME")
        self.display = pygame.Surface((self.window.get_size()))
        self.font = pygame.font.SysFont("Courier", 20)
        self.action_font = pygame.font.SysFont("Courier", 16)
        self.legend_font = pygame.font.SysFont("Courier", 12)
        self.BLACK = (0,0,0)
        self.GREEN = (0,255,0)

        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.level_one_map = LevelOneMap(self)
        self.curr_menu = self.main_menu
        self.current_screen = ''
        self.all_options_selected = []

        # Current menu. Self (current Game instance) given as parameter as MainMenu requires a game to be passed in.

        self.level_one = LevelOne(self)
        self.current_level = 0

    def game_loop(self):
        while self.playing:
            self.events()
            if self.START_KEY:
                self.playing = False
            self.reset_keys()
            self.level_one.show_level()

    def draw_text(self, text, size, position):
        text_font = pygame.font.SysFont("Courier", size)
        text_surface = text_font.render(text, True, self.GREEN)
        text_rect = text_surface.get_rect()
        text_rect.center = position
        self.display.blit(text_surface, text_rect)
        return text_rect

    def blit_screen(self):
        self.window.blit(self.display, (0,0))
        pygame.display.update()
        self.reset_keys()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
                self.level_one.current_level = 0 # This needs changing
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_i:
                    self.I_KEY = True
                if event.key == pygame.K_m:
                    self.M_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.I_KEY, self.M_KEY = False, False, False, False, False, False

    def reset_screen(self):
        self.display.fill(self.BLACK)
        self.window.blit(self.display, (0, 0))
        pygame.display.update()
