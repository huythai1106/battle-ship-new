from until import *
import pygame
from .rect import Rect
# from .battle import Battle


class Ship:
    def __init__(self, length, direct, game, x, y, battle) -> None:
        self.active = False
        self.isSet = False
        self.isDead = False
        self.length = length
        self.game = game
        self.battle = battle
        self.x = x
        self.y = y
        self.direct = direct  # default: vertical , other value : horizon
        self.rects: list[Rect] = []
        self.setup()

    def setup(self):
        if self.direct == "vertical":
            for i in range(self.length):
                rect = Rect(self.x + i * 55, self.y, orange, i)
                self.rects.append(rect)
        else:
            for i in range(self.length):
                rect = Rect(self.x, self.y + i * 55, orange, i)
                self.rects.append(rect)

    def changeDirection(self):
        if self.direct == "vertical":
            self.direct = "horizon"
        else:
            self.direct = "vertical"

        if self.direct == "vertical":
            for i in range(self.length):
                self.rects[i].y = self.y
                self.rects[i].x = self.x + i*55
                self.rects[i].update()
        else:
            for i in range(self.length):
                self.rects[i].y = self.y + i * 55
                self.rects[i].x = self.x
                self.rects[i].update()

    def draw(self, win):
        for rect in self.rects:
            rect.draw(win)

    def changeColorActive(self):
        for rect in self.rects:
            if self.active == True:
                self.battle.isClickShip = True
                rect.color = red
            else:
                rect.color = orange
                self.battle.isClickShip = False

    def changeActive(self, pos):
        print("changeActive")
        if self.isSet:
            return False
        if self.battle.isClickShip and self.active == False:
            return False

        for rect in self.rects:
            if rect.click(pos):
                self.active = not self.active
                self.changeColorActive()
                if self.active == True:
                    self.isSet = False
                else:
                    self.battle.isClickShip = False
                return True

        return False

    def changePos(self, pos):
        x1 = pos[0] - self.x
        y1 = pos[1] - self.y
        self.x = pos[0]
        self.y = pos[1]

        for rect in self.rects:
            rect.x = rect.x + x1
            rect.y = rect.y + y1
            rect.update()

    def checkDead(self):
        for rect in self.rects:
            if not rect.isActive:
                return False
        return True

    def isEnableSet(self, pos):
        if not self.active or self.isSet:
            return False
