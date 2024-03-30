from Agent.AgentState import AgentState
from Heuristic.DistanceHeuristic import DistanceHeuristic
from Store.Store import Store


# Note: This heuristic allows passing another distance heuristic in its constructor
# This cannot be used when creating agents from a configuration file
class DistanceFromPreviousTargetHeuristic(DistanceHeuristic):
    def __init__(self, store: Store, params: dict, previousHeuristic: DistanceHeuristic):
        super().__init__(store, params)

        self.previousHeuristic = previousHeuristic

    def evaluate(self, state: AgentState) -> float:
        if self.target is None:
            print("Previous target: ", self.previousHeuristic.target)
            self.setTarget(self.previousHeuristic.target)

        return super().evaluate(state)
