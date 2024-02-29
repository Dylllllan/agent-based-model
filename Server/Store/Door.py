from Action.LeaveAction import LeaveAction
from Store.Tile import Tile
from Store.TileType import TileType


class Door(Tile):
    def __init__(self, position: tuple):
        super().__init__(position, TileType.DOOR)

        self.action = LeaveAction(position)
