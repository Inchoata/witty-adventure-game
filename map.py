import pygame
from menu import *
from level import *
from text import *

class Map(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game
        self.run_display = False
        self.level = Level(self.game)
        self.text = Text()
        self.level_one_text = LevelOneText()
        self.controls = self.text.controls
        self.legend = self.level_one_text.legend

        # Load maps
        self.first_map = ["                      wwwwwwwwwwwwwwww  ",
                          "                      W              W  ",
                          "                      W              W  ",
                          "                      W              W  ",
                          "                      ----------------  ",
                          "                      |              |__",
                          "                      |              |__",
                          "                      |              |  ",
                          "  ---------------     ------|   |-----  ",
                          "  |             |           |   |       ",
                          "  |             |       ----     ----   ",
                          "  |             |------|      |      |  ",
                          "   --  ----------       --------------  ",
                          "    |  |                                ",
                          "  --|  |-------                         ",
                          "  |           |                         ",
                          "  -------------                         ",
                          "                                        "]

        # Map sizes
        self.map_size = self.get_map_size(self.first_map)

        # Display setup
        self.screen_border = 20
        self.map_width, self.map_height = self.get_map_dimensions(self.first_map)

        # Legend dimensions
        self.legend_x = 2 * (self.game.DISPLAY_W/3)
        self.legend_y = self.screen_border
        self.legend_width = (self.game.DISPLAY_W/3) - self.screen_border
        self.legend_height = self.game.mid_height
        self.legend_text_top = self.legend_y + 20
        self.legend_text_bottom = self.legend_height - 20

        self.controls_rect = self.display_controls()
        self.legend_rect = self.display_legend(self.legend)

        # Map positions
        self.map_x = (self.game.DISPLAY_W - self.legend_rect.width) / self.map_size
        self.map_y = (self.game.DISPLAY_H - self.screen_border) / self.map_size

    def display_controls(self):
        controls_rect = self.game.draw_text(self.controls, 14, (self.game.mid_width, self.game.DISPLAY_H - 20))
        return controls_rect

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keys()

    def get_map_dimensions(self, map):
        map_width = 0
        map_height = 0
        for line in map:
            map_height += 1
            for i in self.split(line):
                map_width += 9
        return map_width, map_height

    def draw_map(self, map):
        w_pos = self.map_x
        h_pos = self.map_y
        for line in map:
            for i in self.split(line):
                self.game.draw_text(i, 18, (w_pos, h_pos))
                w_pos += 9
            w_pos = self.map_x
            h_pos += self.map_y
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()

    def display_legend(self, legend):
        self.legend_x = 2 * (self.game.DISPLAY_W / 3)
        self.legend_y = self.screen_border
        self.legend_width = (self.game.DISPLAY_W / 3) - self.screen_border
        self.legend_height = self.game.DISPLAY_H/2
        legend_rect = pygame.draw.rect(self.game.display, self.game.GREEN,
                         (self.legend_x, self.legend_y,
                          self.legend_width, self.legend_height), 1)
        text_x_pos = self.legend_x + 10
        text_y_pos = self.legend_text_top
        for line in legend:
            text_font = self.game.legend_font
            text_surface = text_font.render(line, True, self.game.GREEN)
            text_rect = text_surface.get_rect()
            text_rect.midleft = (text_x_pos, text_y_pos)
            self.game.display.blit(text_surface, text_rect)
            text_y_pos += 20
        return legend_rect

    def get_map_size(self, map):
        size = 0
        for line in map:
            size += 1
        return size

    def split(self, word):
        return [char for char in word]

class LevelOneMap(Map):
    def __init__(self, game):
        Map.__init__(self, game)

    def check_input(self):
        #self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
                # self.game.current_level = 1
            elif self.state == "Options":
                self.game.curr_menu = self.game.options_menu
            elif self.state == "Credits":
                self.game.curr_menu = self.game.credits_menu
            self.run_display = False
        elif self.game.BACK_KEY:
            self.run_display = False
            self.game.current_level = 1
            self.game.playing = True

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.draw_map(self.first_map)
            self.display_controls()
            self.display_legend(self.legend)
            self.blit_screen()