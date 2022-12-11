
def click(pos, x, y, width, height):
    x1 = pos[1]
    y1 = pos[1]
    if (x <= x1 < + x + width) and (y <= y1 < + y + height):
        return True
    else:
        return False


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def convertNumToPos(number, length):
    x = number // length
    y = number % length
    return (x, y)


def convertPosToNum(tup, len):
    return tup[0] * len + tup[1]


def decodeByte(msg):
    return int.from_bytes(msg, 'little')


def pkt_send(conn, type, data):
    type = int.to_bytes(type, 4, "little")
    len1 = int.to_bytes(str(data).__len__(), 4, "little")
    pk_send = type + len1 + str.encode(data)
    conn.send(pk_send)


def pkt_recv(conn):
    type = decodeByte(conn.recv(4))
    len = decodeByte(conn.recv(4))
    data = conn.recv(len).decode()
    return (type, data)

file = None

ORANGE = (225, 93, 14)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (227, 132, 113)
BLUE = (84, 155, 196)
ORANGE_ACTIVE = (179, 154, 91)
GRAY_LIGHT = (161, 160, 159)
GRAY = (84, 83, 82)
TEXT_COLOR = (47, 77, 135)

SIZE = 10
WEIGHT = 27
LINE_WEIGHT = 1

