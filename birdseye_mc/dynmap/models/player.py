from pydantic import BaseModel
from typing import Optional

class DynmapPlayerModel(BaseModel):
    world: str
    name: str
    account: str
    x: int
    y: int
    z: int
    test: Optional[bool] = False

    def isInHiddenWorld(self) -> bool:
        return self.world == "-some-other-bogus-world-"
