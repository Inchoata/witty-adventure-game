import pygame

class Menu():
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.mid_w = self.game.DISPLAY_W/2
        self.mid_h = self.game.DISPLAY_H/2
        self.run_display = True # Whether the menu is currently displayed

        self.cursor_rect = pygame.Rect(0,0,20,20) # Just makes a rect to represent the cursor
        self.offset = -100

        self.game.current_level = 0

    def draw_cursor(self):
        self.game.draw_text('*', 15, (self.cursor_rect.x, self.cursor_rect.y))

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start" # Sets the current state of the game
        self.start_x, self.start_y = self.mid_w, self.mid_h + 30 # Position of the start text
        self.options_x, self.options_y = self.mid_w, self.mid_h + 50 # Position of options text
        self.credits_x, self.credits_y = self.mid_w, self.mid_h + 70 # Position of credits text
        self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y) # Sets initial cursor pos to start text

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Main Menu", 20, (self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -20))
            self.game.draw_text("Start Game", 20, (self.start_x, self.start_y))
            self.game.draw_text("Options", 20, (self.options_x, self.options_y))
            self.game.draw_text("Credits", 20, (self.credits_x, self.credits_y))
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = "Start"
        if self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = "Credits"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = "Start"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
                self.state = "Options"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
                #self.game.current_level = 1
            elif self.state == "Options":
                self.game.curr_menu = self.game.options_menu
            elif self.state == "Credits":
                self.game.curr_menu = self.game.credits_menu
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Volume"
        self.vol_x, self.vol_y = self.mid_w, self.mid_h + 20
        self.controls_x, self.controls_y = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.vol_x + self.offset, self.vol_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Options", 20, (self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30))
            self.game.draw_text("Volume", 20, (self.vol_x, self.vol_y))
            self.game.draw_text("Controls", 20, (self.controls_x, self.controls_y))
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            if self.state == "Volume":
                self.cursor_rect.midtop = (self.controls_x + self.offset, self.controls_y)
                self.state = "Controls"
            elif self.state == "Controls":
                self.cursor_rect.midtop = (self.vol_x + self.offset, self.vol_y)
                self.state = "Volume"

    def check_input(self):
        self.move_cursor()
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        if self.game.START_KEY:
            if self.state == "Volume":
                self.game.draw_text("This is the volume menu!", 20, (self.mid_h, self.mid_w))
            elif self.state == "Controls":
                self.game.draw_text("This is the controls menu!", 20, (self.mid_h, self.mid_w))
            self.run_display = False

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Credits", 20, (self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 20))
            self.game.draw_text("By Taz", 20, (self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 20))
            self.blit_screen()

#class InGameMenu(Menu):
# Showing Inventory, Health, Stats, Map
