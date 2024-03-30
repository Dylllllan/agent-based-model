from Agent.AgentState import AgentState
from Heuristic.DistanceHeuristic import DistanceHeuristic
from Store.Store import Store


class DistanceFromSelfHeuristic(DistanceHeuristic):
    def __init__(self, store: Store, params: dict):
        super().__init__(store, params)

    def evaluate(self, state: AgentState) -> float:
        if self.target is None:
            currentState = self.store.getAgent(state.id)
            super().setTarget(currentState.position)

        return super().evaluate(state)
