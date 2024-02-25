from Server.Store.Tile import Tile
from Server.Store.TileType import TileType


class Wall(Tile):
    def __init__(self, position: tuple):
        super().__init__(position, TileType.WALL)

        self.action = None
