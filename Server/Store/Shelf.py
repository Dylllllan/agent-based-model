from Action.PickupAction import PickupAction
from Store.ItemState import ItemState
from Store.Tile import Tile
from Store.TileType import TileType


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
