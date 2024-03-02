import os

import pygame as pg
import requests

from Store.TileType import TileType

TILE_COLORS = {
    TileType.DOOR: pg.Color("#4EC362"),
    TileType.CHECKOUT: pg.Color("#FF0047"),
    TileType.WALL: pg.Color("#1F2933"),
    TileType.WAYPOINT: pg.Color("#FFD500"),
}

# If a Cache folder does not exist, create it
if not os.path.exists("Cache"):
    os.makedirs("Cache")


class Tile:
    def __init__(self, position: tuple, tileType: TileType = TileType.TILE):
        self.type = tileType
        self.position = position

    def drawTile(self, surface: pg.Surface, position: tuple, size: int):
        # If the tile type has a color, draw it as a rectangle
        if self.type in TILE_COLORS:
            pg.draw.rect(surface, TILE_COLORS[self.type], pg.Rect(position, (size, size)))


class Shelf(Tile):
    def __init__(self, position: tuple, name: str, category: str, price: int, icon: str):
        super().__init__(position, TileType.SHELF)

        self.name = name
        self.category = category
        self.price = price
        self.icon = icon
        self.iconImage = None

        # If the GRAPHICS_MODE environment variable is set, load the icon image
        if os.environ.get("GRAPHICS_MODE"):
            self.loadIconImage()

    def downloadIconImage(self, cacheFilePath: str):
        # Download the icon image (note: this is blocking)
        iconDownload = requests.get(self.icon)
        # Save the icon to a file in the Cache folder
        with open(cacheFilePath, "wb") as file:
            file.write(iconDownload.content)

    def loadIconImage(self):
        # Create the path to the icon image in the Cache folder
        iconPath = f"Cache/{self.icon.split('/')[-1]}"

        # If the icon image does not exist in the Cache folder, download it
        if not os.path.exists(iconPath):
            self.downloadIconImage(iconPath)

        # Save the path to the icon image - Pygame will use this path to load the image
        self.iconImage = iconPath

    def drawTile(self, surface: pg.Surface, position: tuple, size: int):
        icon = pg.transform.scale(pg.image.load(self.iconImage).convert_alpha(), (size, size))
        surface.blit(icon, icon.get_rect(center=(position[0] + size // 2, position[1] + size // 2)))
