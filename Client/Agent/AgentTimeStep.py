from reactivex import from_iterable, zip

from Client.Agent.AgentState import AgentState
from Client.Agent.IAgent import IAgent
from Client.Agent.IAgentClient import IAgentClient
from Client.Store.Store import Store


class AgentTimeStep:
    def __init__(self, agentId: str, store: Store, client: IAgentClient, agent: IAgent):
        self.agent = agent
        self.client = client

        self.store = store
        self.currentState = self.store.getAgent(agentId)
        print(self.currentState.position)

        directions = self.store.getDirectionsFromPosition(self.currentState.position)
        self.directions = iter(directions)

        self.directionToHeuristicMap = {}

        # Observable aggregation (likely to use zip)
        # How do we map the two together while also requesting the next one? Do we have to track the index?
        # No! Let's use an iterator. One the zip has completed, we can then evaluate the best heuristics
        self.zipObserver = zip(from_iterable(directions), self.client.PreviewObservable).subscribe(
            on_next=lambda preview: self.onPreviewReceived(preview[0], AgentState(preview[1]))
        )
        self.getNextPreview()

    def onPreviewReceived(self, direction: tuple, preview: AgentState):
        self.directionToHeuristicMap[direction] = self.agent.evaluateHeuristics(preview)
        self.getNextPreview()

    def getNextPreview(self):
        try:
            direction = next(self.directions)
            # print("Getting preview for direction: ", direction)
            position = self.getPosition(self.currentState.position, direction)
            self.client.sendSelect(position)
        except StopIteration:
            self.findBestPreview()

    def findBestPreview(self):
        self.zipObserver.dispose()

        bestDirection = min(self.directionToHeuristicMap, key=self.directionToHeuristicMap.get)
        bestHeuristic = self.directionToHeuristicMap[bestDirection]
        self.client.sendSelect(self.getPosition(self.currentState.position, bestDirection))
        print("Selected position: ", self.getPosition(self.currentState.position, bestDirection), "with heuristic: ",
              bestHeuristic)
        self.client.sendCommit()

        if bestHeuristic == 0:
            self.agent.nextHeuristicSet()

    @staticmethod
    def getPosition(position: tuple, direction: tuple) -> tuple:
        return position[0] + direction[0], position[1] + direction[1]
