from Client.Agent.AgentState import AgentState
from Client.Heuristic.Heuristic import Heuristic
from Client.Store.Store import Store


class PickUpItemHeuristic(Heuristic):
    def __init__(self, params: dict, store: Store):
        super().__init__(store)

        self.itemName = params["itemName"]

    def evaluate(self, state: AgentState) -> float:
        # Check if the agent has the item or not
        if state.hasItem(self.itemName):
            return 0.0
        else:
            return 1.0
