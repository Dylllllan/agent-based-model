from Core.ISerializable import ISerializable
from Prediction.PredictionItemState import PredictionItemState


class PredictionRequest(ISerializable):
    def __init__(self, items: list, timeStep: int):
        self.items = items
        self.timeStep = timeStep

    def toDict(self) -> dict:
        return {
            "data_points": [PredictionItemState(item, self.timeStep).toDict() for item in self.items]
        }
