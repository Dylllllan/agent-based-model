import pygame
from reactivex import Subject

from Agent.AgentClient import AgentClient
from Agent.Agent import Agent
from Graphics.Renderer import Renderer
from Store.Store import Store

HOST = "localhost"
PORT = 8000
FPS = 60

if __name__ == "__main__":
    clock = pygame.time.Clock()
    tickSubject = Subject()

    client = AgentClient(HOST, PORT, tickSubject)

    store = Store(client.StoreObservable, client.StateObservable)
    agent = Agent("", store, client)
    renderer = Renderer(tickSubject, store, client.ConnectionObservable)

    while True:
        tickSubject.on_next(None)
        clock.tick(FPS)
