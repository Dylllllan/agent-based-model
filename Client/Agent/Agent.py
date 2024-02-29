from Agent.AgentState import AgentState
from Agent.AgentTimeStep import AgentTimeStep
from Agent.AgentType import AgentType
from Agent.IAgent import IAgent
from Agent.IAgentClient import IAgentClient
from Heuristic.GoToCheckoutHeuristic import GoToCheckoutHeuristic
from Heuristic.GoToDoorHeuristic import GoToDoorHeuristic
from Heuristic.GoToItemHeuristic import GoToItemHeuristic
from Heuristic.PayForItemsHeuristic import PayForItemsHeuristic
from Heuristic.PickUpItemHeuristic import PickUpItemHeuristic
from Store.Store import Store


class Agent(IAgent):
    def __init__(self, configFilePath: str, store: Store, agentClient: IAgentClient):
        self.configFilePath = configFilePath
        # TO-DO: Read from config file

        self.client = agentClient

        self.store = store
        self.heuristics = self.createHeuristics("", self.store)
        self.currentHeuristicSetIndex = 0

        self.client.ConnectionObservable.subscribe(lambda _: self.client.sendInit(AgentType.SHOPPER))

        self.agentId = None
        self.client.AgentIdObservable.subscribe(lambda agentId: self.setAgentId(agentId))

        self.currentTimeStep = None
        # Create a new time step when a new state is received
        self.client.StateObservable.subscribe(lambda _: self.nextTimeStep())

    def setAgentId(self, agentId: str):
        print("Received agent id: ", agentId)
        self.agentId = agentId

    def nextTimeStep(self):
        # Create a new time step
        # TO-DO: Can we move the heuristic set into its own class, rather than passing agent?
        self.currentTimeStep = AgentTimeStep(self.agentId, self.store, self.client, self)

    @staticmethod
    def createHeuristics(configFilePath: str, store: Store) -> list:
        # TO-DO: Read the config file to create the heuristics
        return [
            [
                GoToItemHeuristic({"itemName": "Bread"}, store),
                PickUpItemHeuristic({"itemName": "Bread"}, store)
            ],
            [
                GoToCheckoutHeuristic(store),
                PayForItemsHeuristic(store)
            ],
            [
                GoToDoorHeuristic(store)
            ]
        ]

    def evaluateHeuristics(self, state: AgentState) -> float:
        # print("Evaluating heuristics", self.currentHeuristicSetIndex)
        # print("There are", len(self.heuristics), "heuristic sets")
        return sum([heuristic.evaluate(state) for heuristic in self.heuristics[self.currentHeuristicSetIndex]])

    def nextHeuristicSet(self):
        if self.currentHeuristicSetIndex < len(self.heuristics) - 1:
            self.currentHeuristicSetIndex += 1
        else:
            self.client.Close()
