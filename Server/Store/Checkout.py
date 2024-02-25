from Server.Action.PayAction import PayAction
from Server.Store.Tile import Tile
from Server.Store.TileType import TileType


class Checkout(Tile):
    def __init__(self, position: tuple):
        super().__init__(position, TileType.CHECKOUT)

        self.action = PayAction()
