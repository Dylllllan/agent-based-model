import json
import random
import sys
from sys import exit
from time import sleep

from reactivex import Subject

from Agent.Agent import Agent
from Agent.AgentClient import AgentClient
from Agent.AgentType import AgentType
from Heuristic.HeuristicFactory import HeuristicFactory
from Heuristic.ShoplifterHeuristicFactory import ShoplifterHeuristicFactory
from Heuristic.ShopperHeuristicFactory import ShopperHeuristicFactory
from Store.Store import Store

HOST = "localhost"
PORT = 8000

if __name__ == "__main__":
    arguments = sys.argv[1:]

    tickSubject = Subject()

    # Create an agent
    client = AgentClient(HOST, PORT, tickSubject)
    store = Store(client.StoreObservable, client.StateObservable)

    if len(arguments) > 0:
        # Configuration file path provided as an argument
        configFilePath = arguments[0]

        # Read the agent configuration file
        file = open(configFilePath, "r")
        config = json.load(file)
        file.close()

        agentType = AgentType[config["agentType"]]
        heuristicSet = HeuristicFactory.createHeuristics(config["heuristics"], store)

        agent = Agent(agentType, heuristicSet, store, client)
    else:
        # Random agent configuration
        agentType = random.choice([AgentType.SHOPPER, AgentType.SHOPLIFTER])

        if agentType == AgentType.SHOPPER:
            heuristicSet = ShopperHeuristicFactory.createRandomHeuristics(store)
        else:
            heuristicSet = ShoplifterHeuristicFactory.createRandomHeuristics(store)

        agent = Agent(agentType, heuristicSet, store, client)

    # When the client has disconnected from the server, exit the program
    client.ConnectionObservable.subscribe(
        on_completed=lambda: exit()
    )

    while True:
        tickSubject.on_next(None)
        sleep(0.001)
