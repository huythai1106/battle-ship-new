from .rect import Rect
# from .game import Game
from .ship import Ship
from utils import *
from .image import Image


class Battle:
    def __init__(self, x, y, idMap, game) -> None:
        self.x = x
        self.y = y
        self.idMap = idMap
        self.game = game
        self.rects: list[Rect] = []
        self.actives: list[Image] = []
        self.isClickShip = False
        self.ships: list[Ship] = []
        self.boardGame = Image(self.x - 24, self.y - 28,
                               "./assets/image/boardGame.png")
        # self.isSetting = True
        self.setup()
        self.setupShip()

    def setup(self):
        i = 0
        for x in range(SIZE):
            for y in range(SIZE):
                rect = Rect(self.x + (WEIGHT + LINE_WEIGHT)*x,
                            self.y + (WEIGHT + LINE_WEIGHT)*y, BLUE, i)
                i += 1
                self.rects.append(rect)

        # pygame.display.update()

    def setupShip(self):
        x = self.x
        if self.idMap == 0:
            x += 300
        else:
            x -= 300
        ship1_1 = Ship(1, "vertical", self.game, x, self.y + 50, self, 0)
        ship1_2 = Ship(1, "vertical", self.game, x +60, self.y + 50, self, 1)
        ship1_3 = Ship(1, "vertical", self.game, x+120, self.y + 50, self, 2)
        ship2_1 = Ship(2, "vertical", self.game, x, self.y + 100, self, 3)
        ship2_2 = Ship(2, "vertical", self.game, x+120, self.y + 100, self, 4)
        ship3 = Ship(3, "vertical", self.game, x, self.y + 150, self, 5)
        ship4 = Ship(4, "vertical", self.game, x, self.y + 200, self, 6)

        self.ships.append(ship1_1)
        self.ships.append(ship1_2)
        self.ships.append(ship1_3)
        self.ships.append(ship2_1)
        self.ships.append(ship2_2)
        self.ships.append(ship3)
        self.ships.append(ship4)

    def draw(self, win):
        self.boardGame.draw(win)

        if self.game.getStatusGame() == 1:
            for rect in self.rects:
                rect.draw(win)
            for ship in self.ships:
                ship.draw(win)
        elif self.game.getStatusGame() == 2:
            for rect in self.rects:
                rect.draw(win)

        for act in self.actives:
            act.draw(win)

    # return : [0, 1, 2]

    def gainAttack(self, pos):
        for rect in self.rects:
            if rect.click(pos) and not rect.isAttacked:
                rect.changeColor(GRAY_LIGHT)
                act = Image(rect.x, rect.y, "./assets/image/active.png")
                self.actives.append(act)
                rect.isAttacked = True
                i = 0
                for ship in self.ships:
                    if ship.checkDead():
                        continue

                    if ship.checkAttack(pos):
                        # trung thuyen
                        rect.changeColor(GRAY)
                        act = Image(rect.x, rect.y,
                                    "./assets/image/attack.png")
                        self.actives.append(act)
                        if ship.checkDead():
                            ship.actDead()
                            i += 1
                            if self.checkResultBattle():
                                self.game.finish = True
                        return 2

                return 1

        return 0

    def gainAttackIndex(self, index):
        rect = self.rects[index]

        if not rect.isAttacked:
            rect.changeColor(GRAY_LIGHT)
            act = Image(rect.x, rect.y, "./assets/image/active.png")
            self.actives.append(act)
            rect.isAttacked = True
            i = 0
            for ship in self.ships:
                if ship.checkDead():
                    continue

                if ship.checkAttackIndex(index):
                    # trung thuyen
                    rect.changeColor(GRAY)
                    act = Image(rect.x, rect.y,
                                "./assets/image/attack.png")
                    self.actives.append(act)
                    if ship.checkDead():
                        ship.actDead()
                        i += 1
                        if self.checkResultBattle():
                            self.game.finish = True
                    return 2
            return 1

        return 0

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
