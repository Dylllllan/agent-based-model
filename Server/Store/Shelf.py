from Action.PickupAction import PickupAction
from Store.ItemState import ItemState
from Store.Tile import Tile
from Store.TileType import TileType


class Shelf(Tile):
    def __init__(self, position: tuple, metadata: dict):
        super().__init__(position, TileType.SHELF)

        self.name = metadata["name"]
        self.price = int(metadata["price"])
        self.category = metadata["category"]
        self.icon = metadata["icon"]

        self.action = PickupAction(self.getItemState())

    def getItemState(self) -> ItemState:
        return ItemState(self.name, self.category, self.price, 0.5)

    def toDict(self) -> dict:
        tile = super().toDict()
        tile["name"] = self.name
        tile["category"] = self.category
        tile["price"] = self.price
        tile["icon"] = self.icon

        return tile
