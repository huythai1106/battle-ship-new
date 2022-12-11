import json
import asyncio
import websockets

update_addr = "ws://104.194.240.16/ws/channels/"

async def async_match_start_report(matchID) : 
    async with websockets.connect(update_addr) as websocket:
        data = { "result": 1, "match": matchID}
        pk = json.dumps(data)
        await websocket.send(pk)
async def async_match_close_report(matchID) : 
    async with websockets.connect(update_addr) as websocket:
        data = { "result": 3, "match": matchID}
        pk = json.dumps(data)
        await websocket.send(pk)
async def async_match_update_report(matchID, status, score1, score2) : 
    async with websockets.connect(update_addr) as websocket:
        #status o chua bat dau, 1 dien ra 
        data = { "result": 2, "match": matchID, "status" : status, "id1" : score1, "id2" : score2}
        pk = json.dumps(data)
        await websocket.send(pk)
async def async_match_error_report(matchID) : 
    async with websockets.connect(update_addr) as websocket:
        data = { "result": 0, "match": matchID}
        pk = json.dumps(data)
        await websocket.send(pk)

def match_start_report(matchID) : 
    asyncio.run(async_match_start_report(matchID))

def match_close_report(matchID) : 
    asyncio.run(async_match_close_report(matchID))

def match_update_report(matchID, status, score1, score2) : 
    asyncio.run(async_match_update_report(matchID, status, score1, score2))

def match_error_report(matchID) : 
    asyncio.run(async_match_error_report(matchID))


# match_start_report(100)
# match_update_report(100, 1, 6, 0)
# match_close_report(100)
# match_start_report(matchId)

# c = 0
# while c < 10 :
#     time.sleep(2)
#     match_update_report(matchId, 1, c, 0)
#     c += 1

# match_close_report(matchId)

