# from ais.kane import kane
# from ais.abel import abel

# def main():
#     print("Welcome to the AI play NES project!")
#     print("Please select the AI you want to use:")
#     print("1. Kane's AI")
#     print("2. Abel's AI")
#     print("3. Quit")
#     while True:
#         try:
#             choice = int(input("Please enter your choice: "))
#             if choice == 1:
#                 kane.run()
#             elif choice == 2:
#                 abel.run()
#             elif choice == 3:
#                 break
#             else:
#                 print("Invalid choice!")
#         except ValueError:
#             print("Invalid choice!")

# if __name__ == '__main__':
#     main()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import config
import uvicorn
import os

app = FastAPI()

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
def read_ai():
    platforms = [
        {'key': platform, 'name': config.retro_config[platform]['name']}
        for platform in config.retro_config
    ]
    return {"data": platforms}

@app.get("/games/{platform}")
def read_platform(platform: str):
    games = config.retro_config[platform]['games']
    return {"data": list(games.keys())}


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