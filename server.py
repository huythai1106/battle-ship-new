import socket
from _thread import *
import pickle
from objects.game import Game
import string
import random
from utils import *

server = "127.0.0.1"
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started: ", server)

connected = set()

# @define property
# games : {
#   "MatchID" : {
#     "game" : game
#     countP : number, // so luong nguoi tham gia
#     u1Id : number,
#     u2Id : number,
#     keyPass : string
#     }
# }


games = {}
idCount = 0


def threaded_client(conn: socket.socket, p, gameId):
    global idCount
    # ket noi

    conn.send(str.encode(str(p)))
    #

    while True:
        try:
            data = conn.recv(2048).decode()
            if gameId in games:
                game = games[gameId]["game"]
                if p == 0:
                    game.p1Went = True
                else:
                    game.p2Went = True

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    # reply = game
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    print("Closing game: ", gameId)
    try:
        del games[gameId]
    except:
        pass

    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    type = decodeByte(conn.recv(4))
    print(type)

    if type == 1:

        # khi webserver gui ket noi den game server
        # matchid = decodeByte(conn.recv(4))
        # uid1 = decodeByte(conn.recv(4))
        # uid2 = decodeByte(conn.recv(4))
        # lengthKey = decodeByte(conn.recv(4))

        gameId = str(''.join(random.choices(
            string.ascii_uppercase + string.digits, k=3)))  # thay keypassword
        games[gameId] = {
            "game": Game(gameId),
            "countP": 0,
            # "u1Id" : uid1,
            # "u1Id" : uid2  // tam thoi chua co
        }

        #  [Game(gameId), 0]
        conn.send(str.encode("success creat new game with ID: " + str(gameId)))
        conn.close()

    else:
        idCount += 1
        data = conn.recv(2048).decode()
        print(data)
        if data in games:
            # game, p = games[data]
            games[data]["countP"] += 1
            if games[data]["countP"] == 1:
                conn.send(str.encode("ok"))
                start_new_thread(
                    threaded_client, (conn, games[data]["countP"] - 1, data))
            elif games[data]["countP"] == 2:
                conn.send(str.encode("ok"))
                games[data]["game"].ready = True
                start_new_thread(
                    threaded_client, (conn, games[data]["countP"] - 1, data))
            else:
                conn.send(str.encode("Room full"))
                games[data]["countP"] -= 1
                conn.close()
                idCount -= 1
        else:
            conn.send(str.encode("Not found ID game"))
            conn.close()
            idCount -= 1

    print(games)

    # p = 0
    # gameId = (idCount - 1) // 2

    # if (idCount % 2 == 1):
    #     games[gameId] = Game(gameId)
    #     print("Creating a new game...")
    # else:
    #     games[gameId].ready = True
    #     p = 1

    # start_new_thread(threaded_client, (conn, p, gameId))
