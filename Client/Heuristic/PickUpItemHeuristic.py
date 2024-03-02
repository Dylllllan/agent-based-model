from Agent.AgentState import AgentState
from Heuristic.HeuristicWithParameters import HeuristicWithParameters
from Store.Store import Store


class PickUpItemHeuristic(HeuristicWithParameters):
    def __init__(self, store: Store, params: dict):
        super().__init__(store)

        self.category = params["category"]

    def evaluate(self, state: AgentState) -> float:
        # Check if the agent has the item or not
        if state.hasItemCategory(self.category):
            return 0.0
        else:
            return 1.0
