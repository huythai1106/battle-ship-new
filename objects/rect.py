import pygame
from until import click


class Rect:
    def __init__(self, x, y, color, index) -> None:
        self.x = x
        self.y = y
        self.index = index
        self.color = color
        self.isActive = False
        self.rect = (x, y, 50, 50)

    def setup(self):
        pass

    def draw(self, win):
        # self.update()
        pygame.draw.rect(win, self.color, self.rect)

    def update(self):
        self.rect = (self.x, self.y, 50, 50)

    def changeColor(self, color):
        self.color = color

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if (self.x <= x1 < + self.x + 50) and (self.y <= y1 < + self.y + 50):
            return True
        else:
            return False
