import pygame as pg
from sys import exit as ex
from reactivex import Observable

from Store.Store import Store
from Store.TileType import TileType

TILESIZE = 50
SURF_POS = 10
assets_path = "Graphics/assets/"


class Renderer:
    def __init__(self, tickObservable: Observable, store: Store, connectionObservable: Observable):
        pg.init()
        self.readyToStart = False

        self.mapSurface = None
        self.agentsSurface = None

        self.store = store
        self.store.MapObservable.subscribe(on_next=lambda mapList: self.initialiseStore(mapList))

        tickObservable.subscribe(on_next=lambda _: self.render())
        connectionObservable.subscribe(on_completed=lambda: self.stop_rendering())

    def initialiseStore(self, mapList: list):
        print("Initialising store")

        self.screen = pg.display.set_mode((self.store.width * TILESIZE + 20,
                                           self.store.height * TILESIZE + 20))

        print("Creating map surface")
        self.mapSurface = pg.Surface((self.store.width * TILESIZE, self.store.height * TILESIZE))
        c1, c2 = pg.Color('#F3F9EF'), pg.Color('#E7EEE2')
        colourSwitch = False
        # Make a small checkerboard to better see the squares
        for x in range(self.store.width):
            for y in range(self.store.height):
                square = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
                pg.draw.rect(self.mapSurface, c1 if colourSwitch is True else c2, square)
                colourSwitch = not colourSwitch
            colourSwitch = not colourSwitch

        print("Adding items to map surface")
        for tile in self.store.map:
            image = None
            if tile.type == TileType.SHELF:
                image = pg.image.load(f"{assets_path}bread.png")  # Registered picture for now
            elif tile.type == TileType.CHECKOUT:
                image = pg.image.load(f"{assets_path}checkout.png")
            elif tile.type == TileType.DOOR:
                image = pg.image.load(f"{assets_path}door.png")
            if image is not None:
                x, y = tile.position
                square = pg.Rect(x * TILESIZE, y * TILESIZE,
                                 TILESIZE, TILESIZE)
                self.mapSurface.blit(image, image.get_rect(center=square.center))

        self.readyToStart = True

    def getColourFromID(self, agent_id):
        colour_value = int(agent_id.replace("-", ""), 16) % (256 ** 3)
        return "#{:06x}".format(colour_value)

    def render(self):
        if self.readyToStart is False:
            return

        # Need to handle events every frame for Pygame to run
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.stop_rendering()

        self.screen.fill((255, 255, 255))  # Fill the window with white color

        self.screen.blit(self.mapSurface, (SURF_POS, SURF_POS))

        # Draw each agent as a circle
        for agent in self.store.agents:
            (x, y), colour = agent.position, self.getColourFromID(agent.id)
            pg.draw.circle(self.screen, colour,
                           (x * TILESIZE + 25 + SURF_POS, y * TILESIZE + 25 + SURF_POS), 25)

        # Update the display
        pg.display.flip()

    def stop_rendering(self):
        pg.quit()
        ex()
