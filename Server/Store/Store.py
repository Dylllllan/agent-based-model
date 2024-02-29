import json

from Core.ISerializable import ISerializable
from Store.Checkout import Checkout
from Store.Door import Door
from Store.Shelf import Shelf
from Store.Tile import Tile
from Store.Wall import Wall


class Store(ISerializable):
    def __init__(self, configFilePath: str):
        # Read the JSON configuration
        file = open(configFilePath, "r")
        config = json.load(file)
        file.close()

        self.width = config["size"]["width"]
        self.height = config["size"]["height"]

        # Create a map of Tiles
        self.map = [Tile((x, y)) for y in range(self.height) for x in range(self.width)]

        # For each shelf, replace the shelf tiles
        self.replaceShelves(config["shelves"])

        # For each checkout, replace the checkout tiles
        self.replaceTiles(config["checkouts"], Checkout)
        # For each door, replace the door tiles
        self.replaceTiles(config["doors"], Door)
        # For each wall, replace the wall tiles
        self.replaceTiles(config["walls"], Wall)

    def getTile(self, position: tuple) -> Tile:
        return self.map[(position[1] * self.width) + position[0]]

    def replaceShelves(self, shelves):
        for shelf in shelves:
            x = int(shelf["position"]["x"])
            y = int(shelf["position"]["y"])
            self.map[(y * self.width) + x] = Shelf(shelf["item"]["name"], int(shelf["item"]["price"]),
                                                   (x, y), shelf["item"]["icon"])

    def replaceTiles(self, tiles, tile_type):
        for tile in tiles:
            x = int(tile["position"]["x"])
            y = int(tile["position"]["y"])
            self.map[(y * self.width) + x] = tile_type((x, y))

    def toDict(self) -> dict:
        return {"size": {"width": self.width, "height": self.height}, "map": [tile.toDict() for tile in self.map]}
