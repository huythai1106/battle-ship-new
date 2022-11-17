import pygame
from utils import *


class Rect:
    def __init__(self, x, y, color, index) -> None:
        self.x = x
        self.y = y
        self.index = index
        self.color = color
        self.isActive = False  # use when status game = 1 (setup game)
        self.isAttacked = False  # use when status game = 2 (play game)
        self.rect = (x, y, WEIGHT, WEIGHT)

    def setup(self):
        pass

    def draw(self, win):
        # self.update()
        pygame.draw.rect(win, self.color, self.rect)

    def update(self):
        self.rect = (self.x, self.y, WEIGHT, WEIGHT)

    def changeColor(self, color):
        self.color = color

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if (self.x <= x1 < + self.x + WEIGHT) and (self.y <= y1 < + self.y + WEIGHT):
            return True
        else:
            return False
