from Server.Core.ISerializable import ISerializable


class ItemState(ISerializable):
    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price

    def toDict(self) -> dict:
        return {
            "name": self.name,
            "price": self.price
        }
