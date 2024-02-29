from Action.PayAction import PayAction
from Store.Tile import Tile
from Store.TileType import TileType


class Checkout(Tile):
    def __init__(self, position: tuple):
        super().__init__(position, TileType.CHECKOUT)

        self.action = PayAction()
