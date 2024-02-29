from abc import ABC, abstractmethod

from Agent.IAgent import IAgent


class Action(ABC):
    @abstractmethod
    def DoAction(self, agent: IAgent):
        raise NotImplementedError
