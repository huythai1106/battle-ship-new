from .rect import Rect
from game import Game


class Battle:
    def __init__(self, x, y, status, game) -> None:
        self.x = x
        self.y = y
        self.status = status
        self.game: Game = game
        self.rects = []
        self.ships = []
        self.setup()

    def setup(self):
        for x in range(5):
            for y in range(5):
                rect = Rect(self.x + 55*x,
                            self.y + 55*y, (255, 255, 255))
                self.rects.append(rect)

        # pygame.display.update()

    def setupShip(self):
        pass

    def draw(self, win):
        if self.game.getStatus() == 1:
            for rect in self.rects:
                rect.draw(win)
            for ship in self.ships:
                ship.draw(ship)
        elif self.game.getStatus() == 2:
            for rect in self.rects:
                rect.draw(win)

    def changeStatus(self):
        self.status = not self.status

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
        print(pos)
        for rect in self.rects:
            if rect.click(pos):
                rect.changeColor((255, 0, 0))
                return True

        return False

    def reset(self):
        pass

    def update(self):
        pass
