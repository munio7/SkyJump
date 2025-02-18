import sys
import pygame
import random
import math
from game import Game
from game import UI

game = Game()
ui = UI(game)

ui.main_menu("SKY JUMP")
# end game
pygame.mixer.music.stop()
nature_background_music.stop()
pygame.quit()