from utils import *
from network import Network
from objects.game import Game


class Client:
    def __init__(self) -> None:
        self.net = Network()
        self.width = 700
        self.height = 700
        self.game = None
        self.p = None

    def connect(self, data):
        recv = self.net.startConnect(data, 0)
        print(recv)
        if recv:
            self.game = Game(123)
        else:
            pass

    def getP(self):
        try:
            self.p = self.net.getP()
            print("You are player", self.p)
        except:
            print("loi game")
            quit()

    def getStatusGame(self):
        return self.game.getStatusGame()

    def startGame(self):
        self.net.send("submit")

    def attack(self, pos):
        if self.getStatusGame() == 2:
            posData = make_pos(pos)
            self.net.send(posData)

    def setPosShip(self, pos):
        if self.getStatusGame() == 1:
            self.net.send(make_pos(pos))
