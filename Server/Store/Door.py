from Server.Action.LeaveAction import LeaveAction
from Server.Store.Tile import Tile
from Server.Store.TileType import TileType


class Door(Tile):
    def __init__(self, position: tuple):
        super().__init__(position, TileType.DOOR)

        self.action = LeaveAction(position)
