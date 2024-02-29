from Store.Tile import Tile
from Store.TileType import TileType


class Wall(Tile):
    def __init__(self, position: tuple):
        super().__init__(position, TileType.WALL)

        self.action = None
