import asyncio
from models.api import GameRequest
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import config
import uvicorn
import os
from starlette.websockets import WebSocketDisconnect

from ais.kane import kane
from ais.abel import abel
from services.retro_manager import retro_manager

app = FastAPI()

# Define global variables for the WebSocket
global_ws = []

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/platforms")
async def read_ai():
    platforms = [
        {'key': platform, 'name': config.retro_config[platform]['name']}
        for platform in config.retro_config
    ]
    return {"platforms": platforms}

@app.get("/games")
async def read_platform(platform: str):
    game = config.retro_config[platform]['games']
    games =  [
        {'key': key, 'name': game[key]['display_name'], 'description': game[key]['description']}
        for key in config.retro_config[platform]['games']
    ]
    return {"games": games}

@app.post("/play")
async def play_game(request: GameRequest):
    game = config.retro_config[request.platform]['games'][request.game]['name']
    if not game:
        return {"status": "error" ,"msg": "Invalid game"}
    
    if request.ai not in ["kane", "abel"]:
        return {"status": "error" ,"msg": "Invalid AI"}
    
    retro_manager.start_retro(request.ai, game, global_ws)

    return {"status": "success"}

@app.post("/stop")
async def stop_game(request: GameRequest):
    if request.ai not in ["kane", "abel"]:
        return {"status": "error" ,"msg": "Invalid AI"}
    
    retro_manager.stop_retro(request.ai)

    return {"status": "success"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Set the global WebSocket
    global global_ws
    global_ws = websocket
    try:
        while True:
            data = await websocket.receive_text()
            print(f"ws received: {data}")
    except WebSocketDisconnect:
        global_ws = None

def dev():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        reload=True,
        loop="uvloop",
        http="httptools",
        log_level="debug"
    )


def start():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        loop="uvloop",
        http="httptools",
        workers=4,
    )
