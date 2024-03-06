import os

import pygame
from reactivex import Subject

from Agent.AgentClient import AgentClient
from Agent.AgentType import AgentType
from Graphics.Renderer import Renderer
from Store.Store import Store

HOST = "localhost"
PORT = 8000
FPS = 60

if __name__ == "__main__":
    clock = pygame.time.Clock()
    tickSubject = Subject()

    # Create a new client and store
    client = AgentClient(HOST, PORT, tickSubject)
    store = Store(client.StoreObservable, client.StateObservable)

    # Initialise this client as a spectator
    # Spectators only listen for state updates and do not send any other commands
    client.sendInit(AgentType.SPECTATOR)

    # If the GRAPHICS_MODE environment variable is set, run the graphics renderer
    # The environment variable is required as this is global configuration for the program
    if os.environ.get("GRAPHICS_MODE"):
        renderer = Renderer(tickSubject, store, client.ConnectionObservable)

    while True:
        tickSubject.on_next(None)
        clock.tick(FPS)
