from Core.ISerializable import ISerializable


class ItemState(ISerializable):
    def __init__(self, name: str, category: str, price: int, prediction: float):
        self.name = name
        self.category = category
        self.price = price
        self.prediction = prediction

    def toDict(self) -> dict:
        return {
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "prediction": self.prediction
        }
