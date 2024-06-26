import json

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from starlette.responses import FileResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

from model.PointHolder import PointHolder
from model.WSConnectionManager import WSConnectionManager

app = FastAPI()

red = PointHolder()
red_key = "red"

blue = PointHolder()
blue_key = "blue"

manager = WSConnectionManager()


#
# @app.get("/static/bg.png")
# async def bg():
#     return FileResponse("static/bg.png")
#
# @app.get("/static/bg_blue.png")
# async def bg():
#     return FileResponse("static/bg_blue.png")


@app.get("/")
async def home():
    return FileResponse("static/selector.html")


@app.get("/bo3")
async def viewer():
    return FileResponse("static/bo3-viewer.html")


@app.get("/bo3/commander")
async def viewer():
    return FileResponse("static/bo3-commander.html")


@app.get("/bo5")
async def viewer():
    return FileResponse("static/bo5-viewer.html")


@app.get("/bo5/commander")
async def viewer():
    return FileResponse("static/bo5-commander.html")


@app.get("/increase")
async def increase_counter(side: str, amount: int = 1):
    print(side, red_key, blue_key)
    if side == red_key:
        red.increase(amount)
    elif side == blue_key:
        blue.increase(amount)
    else:
        print(f"No known side, 'side':{side}")
    await broadcast_response_to_all_clients()


@app.get("/decrease")
async def decrease_counter(side: str, amount: int = 1):
    if side == red_key:
        red.decrease(amount)
    elif side == blue_key:
        blue.decrease(amount)
    await broadcast_response_to_all_clients()


@app.get("/wins")
async def set_wins(side: str, amount: int = 1):
    if side == red_key:
        red.set_wins(amount)
    elif side == blue_key:
        blue.set_wins(amount)
    await broadcast_response_to_all_clients()


@app.get("/restart")
async def restart():
    red.reset()
    blue.reset()
    await broadcast_response_to_all_clients()


@app.get("/reset")
async def reset_counter():
    red.reset_points()
    blue.reset_points()
    await broadcast_response_to_all_clients()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
            await manager.send_personal_message(build_response_object(), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


def build_response_object():
    return json.dumps(jsonable_encoder({red_key: red, blue_key: blue}))


async def broadcast_response_to_all_clients():
    await manager.broadcast(build_response_object())
