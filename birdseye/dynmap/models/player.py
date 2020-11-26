from pydantic import BaseModel

class DynmapPlayerModel(BaseModel):
    world: str
    name: str
    account: str
    x: int
    y: int
    z: int

    def isInHiddenWorld(self) -> bool:
        return self.world == "-some-other-bogus-world-"
