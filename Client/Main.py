import os
import sys

import pygame
from reactivex import Subject

from Agent.Agent import Agent
from Agent.AgentClient import AgentClient
from Graphics.Renderer import Renderer
from Store.Store import Store

HOST = "localhost"
PORT = 8000
FPS = 60

if __name__ == "__main__":
    arguments = sys.argv[1:]

    clock = pygame.time.Clock()
    tickSubject = Subject()

    client = AgentClient(HOST, PORT, tickSubject)

    store = Store(client.StoreObservable, client.StateObservable)
    # Configuration file path passed in as an argument
    agent = Agent(arguments[0], store, client)

    # If GRAPHICS_MODE environment variable is set, run the graphics renderer
    if os.environ.get("GRAPHICS_MODE"):
        renderer = Renderer(tickSubject, store, client.ConnectionObservable)

    while True:
        tickSubject.on_next(None)
        clock.tick(FPS)
