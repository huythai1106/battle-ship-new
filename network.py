import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5556
        self.addr = (self.server, self.port)
        # self.p = self.connect()

    def getP(self):
        # lay thong tin nguoi choi (0 or 1)
        return self.connect()

    def startConnect(self, data: str, type: int):
        try:
            # print(data)
            self.client.connect(self.addr)

            # type == 0 : thong bao choi game
            # data : password

            type = int.to_bytes(type, 4, "little")
            pk_send = type + str.encode(data)
            self.client.send(pk_send)
            data1 = self.client.recv(2048).decode()
            return data1
        except socket.error as e:
            print(e)

    # def startConnect(self, data: str):
    #     try:
    #         # print(data)
    #         self.client.connect(self.addr)
    #         self.client.send(str.encode(data))
    #         data1 = self.client.recv(2048).decode()
    #         return data1
    #     except socket.error as e:
    #         print(e)

    def connect(self):
        try:
            a = self.client.recv(2048).decode()
            print(a)
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
