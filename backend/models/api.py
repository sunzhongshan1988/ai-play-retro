from pydantic import BaseModel

class PlayRetroRequest(BaseModel):
    platform: str
    game: str
    ai: str

class StopRetroRequest(BaseModel):
    ai: str
