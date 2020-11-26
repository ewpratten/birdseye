from pydantic import BaseModel
from typing import List

from .player import DynmapPlayerModel

class DynmapUpdateModel(BaseModel):
    currentcount: int
    servertime: int
    timestamp: int
    players: List[DynmapPlayerModel]