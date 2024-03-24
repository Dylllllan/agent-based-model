import os
import sys
from sys import exit

import pygame
from reactivex import Subject

from Agent.AgentClient import AgentClient
from Agent.AgentType import AgentType
from Graphics.Controller import Controller
from Graphics.Renderer import Renderer
from Store.Store import Store

HOST = "localhost"
PORT = 8000
FPS = 60

if __name__ == "__main__":
    arguments = sys.argv[1:]

    if len(arguments) == 0:
        print("No agent type specified. Please specify the agent type as an argument. (SHOPPER/SHOPLIFTER)")
        exit()

    clock = pygame.time.Clock()
    tickSubject = Subject()

    # Create a new client and store
    client = AgentClient(HOST, PORT, tickSubject)
    store = Store(client.StoreObservable, client.StateObservable)

    # Parse agent type from string
    agentType = AgentType[arguments[0].upper()]

    controller = Controller(agentType, client, store)

    # If the GRAPHICS_MODE environment variable is set, run the graphics renderer
    # The environment variable is required as this is global configuration for the program
    if os.environ.get("GRAPHICS_MODE"):
        renderer = Renderer(tickSubject, store, client.ConnectionObservable, controller)

    while True:
        tickSubject.on_next(None)
        clock.tick(FPS)
