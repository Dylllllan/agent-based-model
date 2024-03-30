from Agent.AgentState import AgentState
from Agent.AgentTimeStep import AgentTimeStep
from Agent.AgentType import AgentType
from Agent.IAgent import IAgent
from Agent.IAgentClient import IAgentClient
from Heuristic.SpontaneityHeuristic import SpontaneityHeuristic
from Store.Store import Store


class Agent(IAgent):
    def __init__(self, agentType: AgentType, heuristicSet: list, store: Store, agentClient: IAgentClient):
        self.client = agentClient

        self.store = store
        self.heuristicSetIterator = iter(heuristicSet)
        self.currentHeuristicSet = next(self.heuristicSetIterator)

        # When the client is connected, send the agent type to the server
        self.client.ConnectionObservable.subscribe(lambda _: self.client.sendInit(agentType))

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
        if self.evaluateHeuristics(currentState) <= 0:
            self.nextHeuristicSet()

        # Create a new time step
        # TO-DO: Can we move the heuristic set into its own class, rather than passing agent?
        self.currentTimeStep = AgentTimeStep(self.agentId, self.store, self.client, self)

    def evaluateHeuristics(self, state: AgentState) -> float:
        spontaneousHeuristics = [heuristic for heuristic in self.currentHeuristicSet if
                                 isinstance(heuristic, SpontaneityHeuristic) and heuristic.activated]

        # If there is an activated spontaneity heuristic, return the sum of only those heuristics
        if len(spontaneousHeuristics) > 0:
            return sum([heuristic.evaluate(state) for heuristic in spontaneousHeuristics])
        else:
            # Otherwise, return the sum of all heuristics
            return sum([heuristic.evaluate(state) for heuristic in self.currentHeuristicSet])

    def nextHeuristicSet(self):
        try:
            print("Next heuristic set")
            self.currentHeuristicSet = next(self.heuristicSetIterator)
        except StopIteration:
            # print("No more heuristic sets")
            self.client.Close()
