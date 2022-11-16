
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


orange = (225, 93, 14)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
