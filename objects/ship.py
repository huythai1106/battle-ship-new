import pygame
from .rect import Rect
from until import *


class Ship:
    def __init__(self, length, direct, game, x, y) -> None:
        self.active = False
        self.isSet = False
        self.length = length
        self.game = game
        self.x = x
        self.y = y
        self.direct = direct  # default: vertical , other value : horizon
        self.rects: list[Rect] = []
        self.setup()

    def setup(self):
        if self.direct == "vertical":
            for i in range(self.length):
                rect = Rect(self.x + i * 55, self.y, orange)
                self.rects.append(rect)
        else:
            for i in range(self.length):
                rect = Rect(self.x, self.y + i * 55, orange)
                self.rects.append(rect)

    def changeDirect(self):
        if self.direct == "vertical":
            self.direct = "horizon"
        else:
            self.direct = "vertical"

    def draw(self, win):
        for rect in self.rects:
            rect.draw(win)

    def changeColorActive(self):
        for rect in self.rects:
            if self.active == True:
                rect.color = red
            else:
                rect.color = orange

    def active(self, pos):
        for rect in self.rects:
            if rect.click(pos):
                self.active = not self.active
                self.changeColorActive()
                return True
        return False
