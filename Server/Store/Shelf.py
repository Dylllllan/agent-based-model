from Server.Action.PickupAction import PickupAction
from Server.Store.ItemState import ItemState
from Server.Store.Tile import Tile
from Server.Store.TileType import TileType


class Shelf(Tile):
    def __init__(self, name: str, price: int, position: tuple, icon: str):
        super().__init__(position, TileType.SHELF)

        self.name = name
        self.price = price
        self.icon = icon

        self.action = PickupAction(self.getItemState())

    def getItemState(self) -> ItemState:
        return ItemState(self.name, self.price)

    def toDict(self) -> dict:
        tile = super().toDict()
        tile["name"] = self.name
        tile["price"] = self.price
        tile["icon"] = self.icon

        return tile
