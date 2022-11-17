import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5556
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            a = self.client.recv(2048).decode()
            return a
        except:
            pass

    def send(self, data: str):
        try:
            # print(data)
            self.client.send(str.encode(data))
            data1 = pickle.loads(self.client.recv(4096 * 4))
            return data1
        except socket.error as e:
            print(e)
