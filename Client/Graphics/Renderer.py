from sys import exit

import pygame as pg
from reactivex import Observable

from Graphics.Controller import Controller
from Store.Store import Store

TILE_SIZE = 40

NUMBER_OF_ITEMS_FONT_SIZE = 24
PREDICTION_FONT_SIZE = 16


class Renderer:
    def __init__(self, tickObservable: Observable, store: Store, connectionObservable: Observable,
                 controller: Controller = None):
        pg.init()
        self.screen = None
        self.readyToStart = False

        self.mapSurface = None
        self.agentsSurface = None

        self.store = store
        self.store.MapObservable.subscribe(on_next=lambda _: self.initialiseStore())

        self.controller = controller

        tickObservable.subscribe(on_next=lambda _: self.render())
        connectionObservable.subscribe(on_completed=lambda: self.stopRendering())

    def initialiseStore(self):
        print("Initialising store")

        self.screen = pg.display.set_mode((self.store.width * TILE_SIZE,
                                           self.store.height * TILE_SIZE))

        print("Creating map surface")
        self.mapSurface = pg.Surface((self.store.width * TILE_SIZE, self.store.height * TILE_SIZE))
        colors = [pg.Color("#F5F7FA"), pg.Color("#E4E7EB")]

        # Create a checkerboard pattern to improve visibility of the map
        for y in range(self.store.height):
            for x in range(self.store.width):
                square = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pg.draw.rect(self.mapSurface, colors[(y + x) % 2], square)

        print("Adding items to map surface")
        for tile in self.store.map:
            # Get the position of the tile to be rendered
            position = self.getRenderPosition(tile.position)
            tile.drawTile(self.mapSurface, position, TILE_SIZE)

        self.readyToStart = True

    @staticmethod
    def getAgentColor(agentId: str) -> str:
        idColor = int(agentId.replace("-", ""), 16) % (256 ** 3)
        return "#{:06x}".format(idColor)

    def getRenderPosition(self, position: tuple) -> tuple:
        return position[0] * TILE_SIZE, (self.store.height - position[1] - 1) * TILE_SIZE

    def getAgentPosition(self, position: tuple) -> tuple:
        # Get the render position, then add half the tile size to get the center
        renderPosition = self.getRenderPosition(position)
        return renderPosition[0] + TILE_SIZE // 2, renderPosition[1] + TILE_SIZE // 2

    def render(self):
        if self.readyToStart is False:
            return

        # Need to handle events every frame for Pygame to run
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.stopRendering()
            # Otherwise, arrow keys can be used to move the agent
            elif event.type == pg.KEYDOWN and self.controller is not None:
                if event.key == pg.K_UP:
                    self.controller.moveInDirection((0, 1))
                elif event.key == pg.K_DOWN:
                    self.controller.moveInDirection((0, -1))
                elif event.key == pg.K_LEFT:
                    self.controller.moveInDirection((-1, 0))
                elif event.key == pg.K_RIGHT:
                    self.controller.moveInDirection((1, 0))

        # Draw the store map
        self.screen.blit(self.mapSurface, (0, 0))

        # Draw each agent as a circle
        for agent in self.store.agents:
            pg.draw.circle(self.screen, self.getAgentColor(agent.id),
                           self.getAgentPosition(agent.position), TILE_SIZE // 2)

            # If the agent has paid, draw a smaller circle inside the agent
            if agent.paid:
                pg.draw.circle(self.screen, pg.Color("green"),
                               self.getAgentPosition(agent.position), TILE_SIZE // 4)

            # If the agent has any items, draw a small number inside the agent
            if len(agent.items) > 0:
                font = pg.font.Font(None, NUMBER_OF_ITEMS_FONT_SIZE)
                text = font.render(str(len(agent.items)), True, pg.Color("black"))
                textRect = text.get_rect(center=self.getAgentPosition(agent.position))
                self.screen.blit(text, textRect)

                # For each item, draw the prediction above the agent
                drawPositionY = self.getAgentPosition(agent.position)[1] - TILE_SIZE // 2 - PREDICTION_FONT_SIZE // 2
                for item in agent.items:
                    predictionFont = pg.font.Font(None, PREDICTION_FONT_SIZE)
                    predictionText = predictionFont.render(str(round(item.prediction, 2)), True, pg.Color("black"))
                    predictionRect = predictionText.get_rect(center=(self.getAgentPosition(agent.position)[0],
                                                                     drawPositionY))
                    self.screen.blit(predictionText, predictionRect)
                    drawPositionY -= PREDICTION_FONT_SIZE

        # Update the display
        pg.display.flip()

    @staticmethod
    def stopRendering():
        pg.quit()
        exit()
