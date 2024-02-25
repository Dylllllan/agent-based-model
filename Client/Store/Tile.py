from Client.Store.TileType import TileType


class Tile:
    def __init__(self, position: tuple, tileType: TileType = TileType.TILE):
        self.type = tileType
        self.position = position


class Shelf(Tile):
    def __init__(self, name: str, price: int, position: tuple, icon: str):
        super().__init__(position, TileType.SHELF)

        self.name = name
        self.price = price
        self.icon = icon
