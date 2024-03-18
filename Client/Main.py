import json
import sys
from sys import exit

import pygame
from reactivex import Subject

from Agent.Agent import Agent
from Agent.AgentClient import AgentClient
from Agent.AgentType import AgentType
from Heuristic.HeuristicFactory import HeuristicFactory
from Store.Store import Store

HOST = "localhost"
PORT = 8000
FPS = 60

if __name__ == "__main__":
    arguments = sys.argv[1:]

    if len(arguments) == 0:
        print("No configuration file path provided")
        exit()

    configFilePath = arguments[0]

    clock = pygame.time.Clock()
    tickSubject = Subject()

    # Read the agent configuration file
    file = open(configFilePath, "r")
    config = json.load(file)
    file.close()

    # Create an agent
    client = AgentClient(HOST, PORT, tickSubject)
    store = Store(client.StoreObservable, client.StateObservable)

    agentType = AgentType[config["agentType"]]
    heuristicSet = HeuristicFactory.createHeuristics(config["heuristics"], store)

    # Configuration file path passed in as an argument
    agent = Agent(agentType, heuristicSet, store, client)

    client.ConnectionObservable.subscribe(
        on_completed=lambda: exit()
    )

    while True:
        tickSubject.on_next(None)
        clock.tick(FPS)
