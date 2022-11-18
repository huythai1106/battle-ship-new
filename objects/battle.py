from .rect import Rect
# from .game import Game
from .ship import Ship
from utils import *


class Battle:
    def __init__(self, x, y, idMap, game) -> None:
        self.x = x
        self.y = y
        self.idMap = idMap
        self.game = game
        self.rects: list[Rect] = []
        self.isClickShip = False
        self.ships: list[Ship] = []
        # self.isSetting = True
        self.setup()
        self.setupShip()

    def setup(self):
        i = 0
        for x in range(SIZE):
            for y in range(SIZE):
                rect = Rect(self.x + (WEIGHT + LINE_WEIGHT)*x,
                            self.y + (WEIGHT + LINE_WEIGHT)*y, WHITE, i)
                i += 1
                self.rects.append(rect)

        # pygame.display.update()

    def setupShip(self):
        x = self.x
        if self.idMap == 0:
            x += 300
        else:
            x -= 300

        ship = Ship(3, "vertical", self.game, x, self.y + 200, self)
        ship1 = Ship(2, "vertical", self.game, x, self.y + 100, self)

        self.ships.append(ship)
        self.ships.append(ship1)

    def draw(self, win):
        if self.game.getStatusGame() == 1:
            for rect in self.rects:
                rect.draw(win)
            for ship in self.ships:
                ship.draw(win)
        elif self.game.getStatusGame() == 2:
            for rect in self.rects:
                rect.draw(win)

    # def setMap(self, x, y):
    #     x1 = self.x
    #     y1 = self.y
    #     self.x = x
    #     self.y = y

    #     for rect in self.rects:
    #         rect.x += x1 - self.x
    #         rect.y += y1 - self.y
    #         rect.update()

    def gainAttack(self, pos):
        for rect in self.rects:
            if rect.click(pos) and not rect.isAttacked:
                rect.changeColor(RED)
                rect.isAttacked = True
                i = 0
                for ship in self.ships:
                    if ship.checkDead():
                        continue

                    if ship.checkAttack(pos):
                        rect.changeColor(BLACK)

                    if ship.checkDead():
                        print("dead 1", i)
                        i += 1
                        if self.checkResultBattle():
                            print("lost")
                            self.game.finish = True

                return True

        return False

    def isClickMaps(self, pos):
        for rect in self.rects:
            if rect.click(pos):
                return True
        return False

    def isSetAllShip(self):
        for ship in self.ships:
            if not ship.isSet:
                return False
        return True

    # check KQ
    def checkResultBattle(self):
        for ship in self.ships:
            if not ship.checkDead():
                return False
        return True

    def reset(self):
        pass

    def update(self):
        pass
