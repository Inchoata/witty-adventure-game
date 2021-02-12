from game import Game
import pygame

g = Game()

if __name__ == "__main__":
     while g.running:
          g.curr_menu.display_menu()
          g.game_loop()
