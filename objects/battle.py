from .rect import Rect
# from .game import Game
from .ship import Ship


class Battle:
    def __init__(self, x, y, idMap, game) -> None:
        self.x = x
        self.y = y
        self.idMap = idMap
        self.game = game
        self.rects = []
        self.isClickShip = False
        self.ships: list[Ship] = []
        self.isSetting = True
        self.setup()
        self.setupShip()

    def setup(self):
        i = 0
        for x in range(5):
            for y in range(5):
                rect = Rect(self.x + 55*x,
                            self.y + 55*y, (255, 255, 255), i)
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
            if rect.click(pos):
                rect.changeColor((255, 0, 0))
                return True

        return False

    def isClickMaps(self, pos):
        for rect in self.rects:
            if rect.click(pos):
                return True
        return False

    def checkAllShipSet(self):
        pass

    def reset(self):
        pass

    def update(self):
        pass
