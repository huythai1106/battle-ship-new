import socket
from _thread import *
import pickle
from objects.game import Game
import string
import random
from utils import *
import pygame

pygame.font.init()
pygame.mixer.init()


width = 700
height = 700
win = None


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


# def redrawWindow(win: pygame.Surface, game: Game):
#     if game.getStatusGame() == 1:
#         font = pygame.font.SysFont("comicsans", 40)

#         text = font.render("Player 1", 1, TEXT_COLOR)
#         win.blit(text, (50, 80))

#         text = font.render("Player 2", 1, TEXT_COLOR)
#         win.blit(text, (400, 80))

#         text1 = "set up"
#         text2 = "set up"

#         if game.p1Ready:
#             text1 = "Lock In"
#         if game.p2Ready:
#             text2 = "Lock In"

#         text1Render = font.render(text1, 1, (255, 0, 0, True))
#         text2Render = font.render(text2, 1, (255, 0, 0, True))

#         win.blit(text1Render, (50, 530))
#         win.blit(text2Render, (400, 530))

#     elif game.getStatusGame() == 2:
#         font = pygame.font.SysFont("comicsans", 40)

#         text = font.render("Player 1", 1, TEXT_COLOR)
#         win.blit(text, (50, 80))

#         text = font.render("Player 2", 1, TEXT_COLOR)

#         win.blit(text, (400, 80))
#         for map in game.maps:
#             for rect in map.rects:
#                 rect.draw(win)
#             for ship in map.ships:
#                 ship.draw(win)
#             for rectActive in map.actives:
#                 rectActive.draw(win)

#     elif game.getStatusGame() == 3:
#         font = pygame.font.SysFont("comicsans", 90)
#         if (game.winner() == 0):
#             text = font.render("Player 1 won", 1, (255, 0, 0))
#         elif (game.winner() == 1):
#             text = font.render("Player 1 won", 1, (255, 0, 0))
#         else:
#             text = font.render("Tie game!", 1, (255, 0, 0))

#         win.blit(text, (width / 2 - text.get_width() /
#                         2, height / 2 - text.get_height() / 2))
#     else:
#         text = "waiting for 2 player"
#         font = pygame.font.Font(None, 32)

#         text_render = font.render(text, 1, (0, 0, 0))
#         win.blit(text_render, (width / 2 - text_render.get_width() /
#                  2, height / 2 - text_render.get_height() / 2))


def redrawWindow(win: pygame.Surface, game: Game):
    if game.getStatusGame == 0:
        text = "waiting for 2 player"
        font = pygame.font.Font(None, 32)

        text_render = font.render(text, 1, (0, 0, 0))
        win.blit(text_render, (width / 2 - text_render.get_width() /
                 2, height / 2 - text_render.get_height() / 2))
    else:
        font = pygame.font.SysFont("comicsans", 40)

        text = font.render("Player 1", 1, TEXT_COLOR)
        win.blit(text, (50, 80))

        text = font.render("Player 2", 1, TEXT_COLOR)
        win.blit(text, (400, 80))

        text1 = "set up"
        text2 = "set up"

        if game.p1Ready:
            text1 = "Lock In"
        if game.p2Ready:
            text2 = "Lock In"

        text1Render = font.render(text1, 1, (255, 0, 0, True))
        text2Render = font.render(text2, 1, (255, 0, 0, True))

        win.blit(text1Render, (50, 530))
        win.blit(text2Render, (400, 530))

        win.blit(text, (400, 80))

        for map in game.maps:
            for rect in map.rects:
                rect.draw(win)
            for ship in map.ships:
                ship.draw(win)
            for rectActive in map.actives:
                rectActive.draw(win)


def threaded_webServer(conn: socket.socket, game: Game, gameID):
    global win
    pygame.font.init()

    win = pygame.display.set_mode((width, height))

    pygame.display.set_caption("Server")
    background = pygame.image.load(
        "./assets/image/background.png").convert()

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))  # to mau nen background
        win.blit(background, (0, 0))
        redrawWindow(win, game)
        if game.getStatusGame() == 3:
            # redrawWindow(win, game)
            # pygame.time.delay(3000)
            # run = False

            # gui goi tin ket thuc len web server
            print("finish game")
            break

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                win = None
                pygame.quit()
                run = False

    try:
        del games[gameID]
    except:
        pass
    win = None
    print("Closing game in server: ", gameId)
    conn.close()


def threaded_client_handleSend(game: Game, p, data, type, conn, conn2):
    game.play(p, data, type, conn, conn2)


def threaded_client(conn: socket.socket, p, gameId):
    global idCount
    # ket noi

    # conn.send(str.encode(str(p)))
    pkt_send(conn, 1, str(p))
    #

    startGame = False
    readyGame = False
    playGame = False

    while True:
        # data = conn.recv(2048).decode()
        if gameId in games:
            game: Game = games[gameId]["game"]
            if not game:
                break
            if p == 0:
                game.p1Went = True
            else:
                game.p2Went = True

            if game.bothWent() and not startGame:
                print(1)
                pkt_send(conn, 4, "starting game")
                startGame = True

            elif startGame:
                if game.getStatusGame() == 1:

                    if readyGame:
                        continue
                        # pkt_send(conn, 0, "loi goi tin")

                    type, data = pkt_recv(conn)
                    print(type, data)

                    if type == 8:  # submit game
                        if game.maps[p].isSetAllShip():
                            if p == 0:
                                game.p1Ready = True
                            else:
                                game.p2Ready = True
                            readyGame = True
                            pkt_send(conn, 100, "ready game")
                        else:
                            pkt_send(conn, 0, "chua dat xong game")
                    else:
                        conn2 = None
                        if p == 0:
                            conn2 = games[gameId]["conns"][1]
                        else:
                            conn2 = games[gameId]["conns"][0]

                        game.play(p, data, type, conn, conn2)
                elif game.getStatusGame() == 2:
                    if playGame == False:
                        print("1321213")
                        playGame = True
                        pkt_send(conn, 9, "play game")
                        continue

                    print("1111: ", p)
                    type, data = pkt_recv(conn)
                    print(type, data, p)

                    if p == 0:
                        conn2 = games[gameId]["conns"][1]
                    else:
                        conn2 = games[gameId]["conns"][0]
                    start_new_thread(threaded_client_handleSend,
                                     (game, p, data, type, conn, conn2))
                elif game.getStatusGame() == 3:
                    break
                    # type, data = pkt_recv(conn)
                    # print(type, data)

                    # reply = game
                    # conn.sendall(pickle.dumps(game))
        else:
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

    if type == 1:

        # khi webserver gui ket noi den game server
        # matchid = decodeByte(conn.recv(4))
        # uid1 = decodeByte(conn.recv(4))
        # uid2 = decodeByte(conn.recv(4))
        # lengthKey = decodeByte(conn.recv(4))
        if win == None:
            gameId = str(''.join(random.choices(
                string.ascii_uppercase + string.digits, k=1)))  # thay keypassword
            games[gameId] = {
                "game": Game(gameId),
                "countP": 0,
                # "u1Id" : uid1,
                # "u1Id" : uid2  // tam thoi chua co
                "conns": []
            }

            #  [Game(gameId), 0]
            conn.send(str.encode(
                "success creat new game with ID: " + str(gameId)))
            # conn.send(1)
            # conn.close()

            start_new_thread(threaded_webServer,
                             (conn, games[gameId]["game"], gameId))
        else:
            conn.send(str.encode("Game exsit!"))
            conn.close()
    elif type == 2:
        idCount += 1
        len = decodeByte(conn.recv(4))
        data = conn.recv(len).decode()  # password
        if data in games:
            # game, p = games[data]
            games[data]["countP"] += 1
            if games[data]["countP"] == 1:
                pkt_send(conn, 3, "waiting for player")
                games[data]["conns"].append(conn)
                start_new_thread(
                    threaded_client, (conn, games[data]["countP"] - 1, data))
            elif games[data]["countP"] == 2:
                pkt_send(conn, 3, "waiting for player")
                games[data]["conns"].append(conn)
                games[data]["game"].ready = True
                start_new_thread(
                    threaded_client, (conn, games[data]["countP"] - 1, data))
            else:
                pkt_send(conn, 0, "Room full")
                games[data]["countP"] -= 1
                conn.close()
                idCount -= 1
        else:
            conn.send(str.encode("Not found ID game"))
            conn.close()
            idCount -= 1
    else:
        pkt_send(conn, 0, "Coundn't get game")
        conn.close()

    # p = 0
    # gameId = (idCount - 1) // 2

    # if (idCount % 2 == 1):
    #     games[gameId] = Game(gameId)
    #     print("Creating a new game...")
    # else:
    #     games[gameId].ready = True
    #     p = 1

    # start_new_thread(threaded_client, (conn, p, gameId))
