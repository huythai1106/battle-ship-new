from .battle import Battle
from utils import *

# trung gian cua game

# """
#     status game :
#     0 : waiting player
#     1 : waiting player setup
#     2 : play game
#     3 : finish game
# """


class Game:
    def __init__(self, id) -> None:
        self.status: int = 0
        self.p1Went: bool = False
        self.p2Went = False
        self.p1Ready = False
        self.p2Ready = False
        self.click = False
        self.ready = False
        self.id = id
        self.maps: list[Battle] = [Battle(50, 250, 0, self),  Battle(
            400, 250, 1, self)]  # map trong 1 game
        # self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def getStatusGame(self):
        if self.p1Ready and self.p2Ready:
            self.status = 2
        elif self.p1Went and self.p2Went:
            self.status = 1
        else:
            self.status = 0

        return self.status

    def play(self, player, data):
        # self.moves[player] = move
        # self.maps[player] = Map()
        if self.getStatusGame() == 1:
            if data == "ready":
                if (player == 0):
                    self.p1Ready = True
                else:
                    self.p2Ready = True
                self.maps[player].isSetting = False
            elif data == "changeDirection":
                for ship in self.maps[player].ships:
                    if ship.active:
                        ship.changeDirection()
            else:
                pos = read_pos(data)
                for ship in self.maps[player].ships:
                    if ship.changeActive(pos):
                        print("123123 active")

                # set Ship in map
                for rect in self.maps[player].rects:
                    if rect.isActive == False and rect.click(pos):
                        x = rect.x
                        y = rect.y
                        index = rect.index
                        for ship in self.maps[player].ships:
                            if ship.isEnableSet() and self.checkIsSet(index, ship.length, ship.direct, player):
                                print("changPos")
                                ship.changePos((x, y))
                                ship.isSet = True
                                ship.active = False
                                ship.changeColorActive()

                                # set rect active in map

        elif self.getStatusGame() == 2:
            pos = read_pos(data)
            if player == 0 and self.click == False:
                if self.maps[1].gainAttack(pos):
                    self.click = True
            if player == 1 and self.click == True:
                if self.maps[0].gainAttack(pos):
                    self.click = False

    def checkIsSet(self, index, length, direct, player):
        x = convertNumToPos(index, SIZE)[0]
        y = convertNumToPos(index, SIZE)[1]
        print(x, y)
        if direct == "vertical":
            if x + length > SIZE:
                return False
            for i in range(length):
                x1 = x + i
                print(x1)
                index1 = convertPosToNum((x1, y), SIZE)
                print(index1)
                self.maps[player].rects[index1].isActive = True
            return True
        else:
            if y + length > SIZE:
                return False
            for i in range(length):
                y1 = y + i
                print(y1)
                index1 = convertPosToNum((x, y1), SIZE)
                self.maps[player].rects[index1].isActive = True
            return True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):
        winner = -1
        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False

    def resetGame(self):
        pass
