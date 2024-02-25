from abc import abstractmethod, ABC

from Client.Agent.AgentState import AgentState
from Client.Store.Store import Store


class Heuristic(ABC):
    def __init__(self, store: Store):
        self.store = store

    @abstractmethod
    def evaluate(self, state: AgentState) -> float:
        raise NotImplementedError
