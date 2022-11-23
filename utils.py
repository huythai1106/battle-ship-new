
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


ORANGE = (225, 93, 14)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SIZE = 10
WEIGHT = 25
LINE_WEIGHT = 2
