from utils import *
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
        self.setIndex: int = None
        self.x = x
        self.y = y
        self.direct: str = direct  # default: vertical , other value : horizon
        self.rects: list[Rect] = []
        self.setup()

    def setup(self):
        if self.direct == "vertical":
            for i in range(self.length):
                rect = Rect(self.x + i * (WEIGHT +
                            LINE_WEIGHT), self.y, ORANGE, i)
                self.rects.append(rect)
        else:
            for i in range(self.length):
                rect = Rect(self.x, self.y + i *
                            (WEIGHT + LINE_WEIGHT), ORANGE, i)
                self.rects.append(rect)

    def changeDirection(self):
        if self.direct == "vertical":
            self.direct = "horizon"
        else:
            self.direct = "vertical"

        if self.direct == "vertical":
            for i in range(self.length):
                self.rects[i].y = self.y
                self.rects[i].x = self.x + i * (WEIGHT + LINE_WEIGHT)
                self.rects[i].update()
        else:
            for i in range(self.length):
                self.rects[i].y = self.y + i * (WEIGHT + LINE_WEIGHT)
                self.rects[i].x = self.x
                self.rects[i].update()

    def draw(self, win):
        for rect in self.rects:
            rect.draw(win)

    def changeColorActive(self):
        for rect in self.rects:
            if self.active == True:
                self.battle.isClickShip = True
                rect.color = RED
            else:
                rect.color = ORANGE
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

    def checkAttack(self, pos):
        for rect in self.rects:
            if rect.click(pos):
                rect.isAttacked = True
                rect.changeColor(BLACK)
                return True

        return False

    def checkDead(self):
        for rect in self.rects:
            if not rect.isAttacked:
                return False

        # do something
        return True

    def actDead(self):
        index = self.setIndex
        x = convertNumToPos(index, SIZE)[0]
        y = convertNumToPos(index, SIZE)[1]
        if self.direct == "vertical":
            if x + self.length > SIZE:
                return False
            for i in range(self.length):
                x1 = x + i
                for numX in (-1, 0, 1):
                    for numY in (-1, 0, 1):
                        if numX == 0 and numY == 0:
                            continue
                        xNum = x1 + numX
                        yNum = y + numY
                        if (xNum >= 0 and xNum < SIZE) and (yNum >= 0 and yNum < SIZE):
                            index1 = convertPosToNum((xNum, yNum), SIZE)
                            self.battle.rects[index1].isAttacked = True
                            self.battle.rects[index1].changeColor(RED)

        else:
            if y + self.length > SIZE:
                return False
            for i in range(self.length):
                y1 = y + i
                for numX in (-1, 0, 1):
                    for numY in (-1, 0, 1):
                        if numX == 0 and numY == 0:
                            continue
                        xNum = x + numX
                        yNum = y1 + numY
                        if (xNum >= 0 and xNum < SIZE) and (yNum >= 0 and yNum < SIZE):
                            index1 = convertPosToNum((xNum, yNum), SIZE)
                            # self.maps[player].rects[index1].isActive = True
                            self.battle.rects[index1].isAttacked = True
                            self.battle.rects[index1].changeColor(RED)

    def isEnableSet(self):
        return self.active and not self.isSet
