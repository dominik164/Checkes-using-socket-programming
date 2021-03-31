import pygame
import pygame.freetype
from colors import *
pygame.init()
font_1 = pygame.freetype.SysFont('Sans', 35)
txt_K = "K"


class Pion:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.queen = False

    def draw_pion(self, win):
        pygame.draw.circle(
            win, self.color, (self.x*80+40, self.y*80+100), 32)
        if self.queen == True:
            font_1.render_to(win, (self.x*80+32, self.y*80+88),
                             txt_K, (255, 255, 0))
            pygame.display.flip()

    def move(self, x, y):
        self.x = x
        self.y = y

    def make_queen(self):
        if self.y == 0 and self.color == WHITE:
            self.queen = True
        elif self.y == 7 and self.color == GREY:
            self.queen = True
