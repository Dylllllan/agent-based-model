from Core.ISerializable import ISerializable
from Store.Item import Item


class PredictionItemState(ISerializable):
    def __init__(self, item: Item, timeStep: int):
        self.item = item
        self.timeStep = timeStep

    def toDict(self) -> dict:
        return {
            "time": self.timeStep,
            "x": self.item.position[0],
            "y": self.item.position[1],
            "category": self.item.category,
            "status": "complete",
            "id": self.item.id
        }
