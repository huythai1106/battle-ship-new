from .battle import Battle
from utils import *
import string
import random

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
        self.finish = False
        self.id = id
        self.maps: list[Battle] = [Battle(30, 250, 0, self),  Battle(
            400, 250, 1, self)]  # map trong 1 game
        # self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def getStatusGame(self):
        if self.finish:
            self.status = 3
        elif self.p1Ready and self.p2Ready:
            self.status = 2
        elif self.p1Went and self.p2Went:
            self.status = 1
        else:
            self.status = 0

        return self.status

    def play(self, player, data, type, conn, conn2):
        # self.moves[player] = move
        # self.maps[player] = Map()
        print(type, data)
        if type == 5:  # active ship
            data = int(data)
            if self.getStatusGame() != 1:
                pkt_send(conn, 0, "loi")
                return

            if self.maps[player].ships[data].changeActiveIndex():
                pkt_send(conn, 100, "ok")
            else:
                pkt_send(conn, 0, "da co thuyen dc chon")
        elif type == 6:  # changeDirection
            if self.getStatusGame() != 1:
                pkt_send(conn, 0, "loi")
                return

            for ship in self.maps[player].ships:
                if ship.active:
                    ship.changeDirection()
                    pkt_send(conn, 100, "ok")
                    return

            pkt_send(conn, 0, "chua co thuyen duoc chon")

        elif type == 7:
            index = int(data)
            isSet = False
            if self.getStatusGame() != 1:
                pkt_send(conn, 0, "loi")
                return

            rect = self.maps[player].rects[index]
            if not (rect.isActive == False):
                pkt_send(conn, 0, "loi")
                return

            x = self.maps[player].rects[index].x
            y = self.maps[player].rects[index].y

            for ship in self.maps[player].ships:
                if ship.isEnableSet() and self.checkIsSet(index, ship.length, ship.direct, player):
                    ship.changePos((x, y))
                    ship.isSet = True
                    ship.active = False
                    ship.setIndex = index
                    ship.changeColorActive()
                    # self.maps[player].isClickShip = False
                    ship.setColorInMap()
                    pkt_send(conn, 100, "ok")
                    isSet = True

            if isSet == False:
                pkt_send(conn, 0, "loi")

        elif type == 10:
            data = int(data)
            if player == 0:
                if self.click == True:
                    pkt_send(conn, 0, "ko den luot 1")
                elif self.maps[1].gainAttackIndex(data) == 1:
                    self.click = True
                    pkt_send(conn, 11, "MISS")
                    pkt_send(conn2, 11, str(data))
                # ban thanh cong va ban trung
                elif self.maps[1].gainAttackIndex(data) == 2:
                    pkt_send(conn, 12, "HIT")
                    pkt_send(conn2, 12, str(data))
                else:
                    pkt_send(conn, 0, "LOI BAN")

            if player == 1:
                if self.click == False:
                    pkt_send(conn, 0, "ko den luot 2")
                elif self.maps[0].gainAttackIndex(data) == 1:
                    self.click = False
                    pkt_send(conn, 11, "MISS")
                    pkt_send(conn2, 11, str(data))
                elif self.maps[0].gainAttackIndex(data) == 2:
                    pkt_send(conn, 12, "HIT")
                    pkt_send(conn2, 12, str(data))
                else:
                    pkt_send(conn, 0, "LOI BAN")
        else:
            pkt_send(conn, 0, "loi ko xac dinh")

        # if self.getStatusGame() == 1:
        #     if data == "submit":
        #         if self.maps[player].isSetAllShip():
        #             if (player == 0):
        #                 self.p1Ready = True
        #             else:
        #                 self.p2Ready = True
        #         # self.maps[player].isSetting = False
        #     elif data == "changeDirection":
        #         for ship in self.maps[player].ships:
        #             if ship.active:
        #                 ship.changeDirection()
        #     else:
        #         pos = read_pos(data)
        #         for ship in self.maps[player].ships:
        #             if ship.changeActive(pos):
        #                 print("active")

        #         # set Ship in map
        #         for rect in self.maps[player].rects:
        #             if rect.isActive == False and rect.click(pos):
        #                 x = rect.x
        #                 y = rect.y
        #                 index = rect.index
        #                 for ship in self.maps[player].ships:
        #                     if ship.isEnableSet() and self.checkIsSet(index, ship.length, ship.direct, player):
        #                         ship.changePos((x, y))
        #                         ship.isSet = True
        #                         ship.active = False
        #                         ship.setIndex = index
        #                         ship.changeColorActive()
        #                         # self.maps[player].isClickShip = False
        #                         ship.setColorInMap()

        #                         # set rect active in map

        # elif self.getStatusGame() == 2:
            # pos = read_pos(data)
            # if player == 0 and self.click == False:
            #     if self.maps[1].gainAttack(pos) == 1:
            #         self.click = True
            # if player == 1 and self.click == True:
            #     if self.maps[0].gainAttack(pos) == 1:
            #         self.click = False

    def checkIsSet(self, index, length, direct, player):
        x = convertNumToPos(index, SIZE)[0]
        y = convertNumToPos(index, SIZE)[1]
        if direct == "vertical":
            if x + length > SIZE:
                return False
            for i in range(length):
                x1 = x + i
                for numX in (-1, 0, 1):
                    for numY in (-1, 0, 1):
                        xNum = x1 + numX
                        yNum = y + numY
                        if (xNum >= 0 and xNum < SIZE) and (yNum >= 0 and yNum < SIZE):
                            index1 = convertPosToNum((xNum, yNum), SIZE)
                            self.maps[player].rects[index1].isActive = True
            return True
        else:
            if y + length > SIZE:
                return False
            for i in range(length):
                y1 = y + i
                for numX in (-1, 0, 1):
                    for numY in (-1, 0, 1):
                        xNum = x + numX
                        yNum = y1 + numY
                        if (xNum >= 0 and xNum < SIZE) and (yNum >= 0 and yNum < SIZE):
                            index1 = convertPosToNum((xNum, yNum), SIZE)
                            self.maps[player].rects[index1].isActive = True
            return True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):
        winner = -1

        if self.maps[0].checkResultBattle():
            winner = 1
        elif self.maps[1].checkResultBattle():
            winner = 0

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False

    def resetGame(self):
        pass

    def draw(self, win):
        pass
