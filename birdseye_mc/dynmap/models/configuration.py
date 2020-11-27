from pydantic import BaseModel
from typing import List

from .world import DynmapWorldModel

class DynmapConfigurationModel(BaseModel):
    updaterate: int
    title: str
    defaultworld: str
    worlds: List[DynmapWorldModel]
