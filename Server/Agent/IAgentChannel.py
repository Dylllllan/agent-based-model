from abc import ABC, abstractmethod

from reactivex import Observable

from Server.Network.PreviewMessage import PreviewMessage
from Server.Network.StateMessage import StateMessage
from Server.Store.Store import Store


class IAgentChannel(ABC, object):
    @abstractmethod
    def SendInit(self, agentId: str, store: Store):
        raise NotImplementedError

    @abstractmethod
    def SendState(self, state: StateMessage):
        raise NotImplementedError

    @abstractmethod
    def SendPreview(self, preview: PreviewMessage):
        raise NotImplementedError

    @abstractmethod
    def Kick(self):
        raise NotImplementedError

    @property
    def LoginObservable(self) -> Observable:
        raise NotImplementedError

    @property
    def SelectObservable(self) -> Observable:
        raise NotImplementedError

    @property
    def CommitObservable(self) -> Observable:
        raise NotImplementedError
