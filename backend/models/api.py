from pydantic import BaseModel

class GameRequest(BaseModel):
    platform: str
    game: str
    ai: str
