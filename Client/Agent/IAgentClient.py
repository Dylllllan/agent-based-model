from abc import ABC, abstractmethod

from reactivex import Observable

from Agent.AgentType import AgentType


class IAgentClient(ABC, object):
    @property
    def ConnectionObservable(self) -> Observable:
        raise NotImplementedError

    @property
    def AgentIdObservable(self) -> Observable:
        raise NotImplementedError

    @property
    def StoreObservable(self) -> Observable:
        raise NotImplementedError

    @property
    def StateObservable(self) -> Observable:
        raise NotImplementedError

    @property
    def PreviewObservable(self) -> Observable:
        raise NotImplementedError

    @abstractmethod
    def sendInit(self, agentType: AgentType):
        raise NotImplementedError

    @abstractmethod
    def sendSelect(self, position: tuple):
        raise NotImplementedError

    @abstractmethod
    def sendCommit(self):
        raise NotImplementedError

    @abstractmethod
    def Close(self):
        raise NotImplementedError
