from Client.Agent.AgentState import AgentState
from Client.Heuristic.Heuristic import Heuristic


class PayForItemsHeuristic(Heuristic):
    def evaluate(self, state: AgentState) -> float:
        if state.paid:
            return 0.0
        else:
            return 1.0
