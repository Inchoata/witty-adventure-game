import pygame
from menu import *
from level import *

class Map(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keys()

    def display_text_block(self, text, w_pos, h_pos):
        for line in text:
            for letter in self.split(line):
                self.game.draw_text(letter, 18, (w_pos, h_pos))
                w_pos += 10
            w_pos = 50
            h_pos += 30
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()

    def split(self, word):
        return [char for char in word]


class LevelOneMap(Map):
    def __init__(self, game):
        Map.__init__(self, game)

    def display_menu(self):

        self.first_map = ["                      wwwwwwwwwwwwwwww  ",
                          "                      W              W  ",
                          "                      W              W  ",
                          "                      W              W  ",
                          "                      ----------------  ",
                          "                      |              |__",
                          "                      |              |__",
                          "                   == |              |  ",
                          "  --------------- ==  ------|   |-----  ",
                          "  |             |==         |   |       ",
                          "  |             |       ----     ----   ",
                          "  |             |------|      |      |  ",
                          "   --  -----------      --------------   ",
                          "    |  |                                 ",
                          "  --|  |-------                          ",
                          "  |           |                          ",
                          "  -------------                          "]

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
                # self.game.current_level = 1
            elif self.state == "Options":
                self.game.curr_menu = self.game.options_menu
            elif self.state == "Credits":
                self.game.curr_menu = self.game.credits_menu
            self.run_display = False

        #self.run_display = True
        while self.game.curr_menu == self.game.level_one_map:
            self.game.events()
            #self.check_input()

            self.game.display.fill(self.game.BLACK)

            self.display_text_block(self.first_map, 100, 100)
            self.blit_screen()