import json

from Agent.AgentState import AgentState
from Agent.AgentTimeStep import AgentTimeStep
from Agent.AgentType import AgentType
from Agent.IAgent import IAgent
from Agent.IAgentClient import IAgentClient
from Heuristic.HeuristicFactory import HeuristicFactory
from Store.Store import Store


class Agent(IAgent):
    def __init__(self, configFilePath: str, store: Store, agentClient: IAgentClient):
        # Read the JSON configuration
        file = open(configFilePath, "r")
        config = json.load(file)
        file.close()

        self.client = agentClient

        self.store = store
        self.heuristicIterator = iter(HeuristicFactory.createHeuristics(config["heuristics"], store))
        self.currentHeuristicSet = next(self.heuristicIterator)

        # When the client is connected, send the agent type to the server
        self.client.ConnectionObservable.subscribe(lambda _: self.client.sendInit(AgentType[config["agentType"]]))

        self.agentId = None
        self.client.AgentIdObservable.subscribe(lambda agentId: self.setAgentId(agentId))

        self.currentTimeStep = None
        # Create a new time step when a new state is received
        self.client.StateObservable.subscribe(lambda _: self.nextTimeStep())

    def setAgentId(self, agentId: str):
        print("Received agent id: ", agentId)
        self.agentId = agentId

    def nextTimeStep(self):
        currentState = self.store.getAgent(self.agentId)
        if self.evaluateHeuristics(currentState) == 0:
            self.nextHeuristicSet()

        # Create a new time step
        # TO-DO: Can we move the heuristic set into its own class, rather than passing agent?
        self.currentTimeStep = AgentTimeStep(self.agentId, self.store, self.client, self)

    def evaluateHeuristics(self, state: AgentState) -> float:
        # print("Evaluating heuristics", self.currentHeuristicSetIndex)
        # print("There are", len(self.heuristics), "heuristic sets")
        return sum([heuristic.evaluate(state) for heuristic in self.currentHeuristicSet])

    def nextHeuristicSet(self):
        try:
            self.currentHeuristicSet = next(self.heuristicIterator)
        except StopIteration:
            print("No more heuristic sets")
            self.client.Close()
