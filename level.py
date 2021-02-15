import pygame
from menu import *
from text import *

class Level(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game
        self.text_complete = False
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)  # Just makes a rect to represent the cursor
        self.offset = -5

        # Text and option box setup
        self.text = Text()
        self.controls = self.text.controls
        self.current_option_selected = ""

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
        self.text = LevelOneText()
        self.opening_text = self.text.opening_text
        self.options = self.text.options

        # Positions for text in player action box
        self.state = "A"
        self.A_x, self.A_y = (self.action_box_x + self.twelth_x), self.action_box_text_top
        self.B_x, self.B_y = self.A_x, (self.A_y + (self.action_box_text_bottom / len(self.options)))
        self.C_x, self.C_y = self.A_x, (self.B_y + 2 * (self.action_box_text_bottom / len(self.options))) # TO DO
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

    def display_controls(self):
        self.game.draw_text(self.controls, 14, (self.game.mid_width, self.game.DISPLAY_H - 20))

    def display_all_text(self, game_text, player_options):
        if self.text_complete:
            self.game.display.fill(self.game.BLACK)
            self.display_text_block(game_text)
            self.display_action_block(player_options)
            self.display_controls()
            self.draw_cursor()
            self.game.blit_screen()
        else:
            self.game.display.fill(self.game.BLACK)
            self.text_complete = self.display_text_animation(game_text)

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "A":
                print("Selected A")
                self.current_option_selected = "A"
                self.game.all_options_selected.append("A")
            elif self.state == "B":
                print("Selected B")
                self.current_option_selected = "B"
                self.game.all_options_selected.append("A")
            elif self.state == "C":
                print("Selected C")
                self.current_option_selected = "C"
                self.game.all_options_selected.append("A")
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
            self.display_all_text(self.opening_text, self.options)
            if self.current_option_selected == "A":
                # TO DO display next screen
                pass
            if self.current_option_selected == "B":
                # TO DO display next screen
                pass
            if self.current_option_selected == "C":
                # TO DO display next screen
                pass
