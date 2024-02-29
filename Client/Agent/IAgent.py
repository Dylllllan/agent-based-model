from abc import ABC, abstractmethod

from Agent.AgentState import AgentState


class IAgent(ABC):
    @abstractmethod
    def evaluateHeuristics(self, state: AgentState) -> float:
        raise NotImplementedError

    @abstractmethod
    def nextHeuristicSet(self):
        raise NotImplementedError
