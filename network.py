import socket
import pickle
from utils import *


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "0.tcp.ap.ngrok.io"
        self.port = 17305
        self.addr = (self.server, self.port)
        # self.p = self.connect()

    def getP(self):
        # lay thong tin nguoi choi (0 or 1)
        return self.connect()

    def startConnect(self, data: str, type: int, uid : int):
        try:
            # print(data)
            self.client.connect(self.addr)

            # type == 0 : thong bao choi game
            # data : password

            type = int.to_bytes(type, 4, "little")
            len1 = int.to_bytes(len(data), 4, "little")
            pk_send = type + len1 + str.encode(data)
            self.client.send(pk_send)
            self.client.send(int.to_bytes(uid, 4, "little"))

            return self.pkt_recv()
        except socket.error as e:
            print(e)

    def connect(self):
        try:
            type, p = self.pkt_recv()
            print(type, p)
            return p
        except:
            print("loi")
            pass

    def send(self, data: str):
        try:
            # print(data)
            self.client.send(str.encode(data))
            data1 = pickle.loads(self.client.recv(4096 * 4))
            return data1
        except socket.error as e:
            print(e)

    def pkt_send(self, type, data):
        type = int.to_bytes(type, 4, "little")
        len1 = int.to_bytes(len(str(data)), 4, "little")
        pk_send = type + len1 + str.encode(data)
        self.client.send(pk_send)

    def pkt_recv(self):
        type = decodeByte(self.client.recv(4))
        len = decodeByte(self.client.recv(4))
        data = self.client.recv(len).decode()
        return (type, data)
