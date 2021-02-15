import pygame
from menu import *

class Level(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game
        self.text_complete = False
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)  # Just makes a rect to represent the cursor
        self.offset = -5

        # Text and option block templates
        # Main text box
        self.twelth_x = self.game.DISPLAY_W/12
        self.twelth_y = self.game.DISPLAY_H/12
        self.text_block_x = self.twelth_x
        self.text_block_y = self.twelth_y

        # Option block
        # Box dimensions
        self.action_box_x = self.twelth_x
        self.action_box_y = self.twelth_y * 7
        self.action_box_width = self.twelth_x * 10
        self.action_box_height = self.twelth_y * 4
        self.action_box_text_top = self.action_box_y + 30
        self.action_box_text_bottom = self.action_box_height - 30


        # Text positions



    def draw_cursor(self):
        self.game.draw_text('*', 15, (self.cursor_rect.x, self.cursor_rect.y))


    def display_text_animation(self, text):
        w_pos = self.text_block_x
        h_pos = self.text_block_y
        for line in text:
            for letter in self.split(line):
                #self.game.check_input()
                self.game.draw_text(letter, 18, (w_pos, h_pos))
                self.game.window.blit(self.game.display, (0, 0))
                pygame.display.update()
                pygame.time.wait(10)
                w_pos += 10
            w_pos = 50
            h_pos += 30
        self.text_complete = True
        return self.text_complete


    def display_text_block(self, text):
        x_pos = self.text_block_x
        y_pos = self.text_block_y
        for line in text:
            for letter in self.split(line):
                self.game.draw_text(letter, 18, (x_pos, y_pos))
                x_pos += 10
            x_pos = 50
            y_pos += 30
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()


    def split(self, word):
        return[char for char in word]


class LevelOne(Level):
    def __init__(self, game):
        Level.__init__(self, game)
        self.current_level = 1



        self.opening_text = ["You awaken, head pounding. There is a bright light",
                             "shining onto your face. You open your eyes. You're",
                             "alone in a bright, clinical room. You are tied to a",
                             "surgical operating table. There are surgical ",
                             "instruments on a table beside you. It looks like you",
                             "could lean over and reach the tools with your mouth.",
                             "What will you do?"]

        self.options =      ["A) Cry for help.",
                             "B) Attempt to lean over to reach a scalpel ",
                             "   with your mouth.",
                             "C) Look around."]

        self.controls =      "I - Inventory         M - Map       ENTER - Main Menu"

        # Positions for text in player action box
        self.state = "A"
        self.A_x, self.A_y = (self.action_box_x + self.twelth_x), self.action_box_text_top
        self.B_x, self.B_y = self.A_x, (self.A_y + (self.action_box_text_bottom / len(self.options)))
        self.C_x, self.C_y = self.A_x, (self.B_y + (self.action_box_text_bottom / len(self.options)))
        self.cursor_rect.midtop = (self.A_x + self.offset, self.A_y)  # Sets initial cursor pos to option A

    def display_action_block(self, options):  # This is a horrendous method, refactor later!
        pygame.draw.rect(self.game.display, self.game.GREEN,
                        (self.action_box_x, self.action_box_y,
                        self.action_box_width, self.action_box_height), 1)
        text_x_pos = self.action_box_x + self.twelth_x
        text_y_pos = self.action_box_text_top
        for option in options:
            text_font = self.game.action_font
            text_surface = text_font.render(option, True, self.game.GREEN)
            text_rect = text_surface.get_rect()
            text_rect.midleft = (text_x_pos, text_y_pos)
            self.game.display.blit(text_surface, text_rect)
            text_y_pos += (self.action_box_text_bottom / len(options))

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "A":
                print("Selected A")
            elif self.state == "B":
                print("Selected B")
            elif self.state == "C":
                print("Selected C")
        elif self.game.I_KEY:
            print("I should show the inventory.")
            self.current_level = 0
            self.game.curr_menu = self.game.main_menu
            self.game.playing = False
        elif self.game.M_KEY:
            print("I should be showing the map")
            self.current_level = 0
            self.game.curr_menu = self.game.level_one_map
            self.game.playing = False


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "A":
                self.cursor_rect.midtop = (self.B_x + self.offset, self.B_y)
                self.state = "B"
            elif self.state == "B":
                self.cursor_rect.midtop = (self.C_x + self.offset, self.C_y)
                self.state = "C"
            elif self.state == "C":
                self.cursor_rect.midtop = (self.A_x + self.offset, self.A_y)
                self.state = "A"
        if self.game.UP_KEY:
            if self.state == "A":
                self.cursor_rect.midtop = (self.C_x + self.offset, self.C_y)
                self.state = "C"
            elif self.state == "B":
                self.cursor_rect.midtop = (self.A_x + self.offset, self.A_y)
                self.state = "A"
            elif self.state == "C":
                self.cursor_rect.midtop = (self.B_x + self.offset, self.B_y)
                self.state = "B"

    def show_level(self):
        self.game.playing = True
        self.game.reset_screen()
        self.current_level = 1
        while self.current_level == 1:
            self.game.events()
            self.check_input()
            if self.text_complete:
                self.game.display.fill(self.game.BLACK)
                self.display_text_block(self.opening_text)
                self.display_action_block(self.options)
                self.game.draw_text(self.controls, 14, (self.game.mid_width, self.game.DISPLAY_H-20))
                self.draw_cursor()
                self.game.blit_screen()
            else:
                self.game.display.fill(self.game.BLACK)
                self.text_complete = self.display_text_animation(self.opening_text)

