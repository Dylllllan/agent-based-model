from Action.Action import Action
from Action.MoveAction import MoveAction
from Core.ISerializable import ISerializable
from Store.TileType import TileType


class Tile(ISerializable):
    def __init__(self, position: tuple, tileType: TileType = TileType.TILE):
        self.type = tileType
        self.position = position
        self.action = MoveAction(self.position)

    def getAction(self) -> Action:
        return self.action

    def toDict(self) -> dict:
        return {"type": self.type, "position": self.position}
