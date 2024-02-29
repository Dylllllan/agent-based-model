from abc import ABC, abstractmethod

from Store.ItemState import ItemState


class IAgent(ABC):
    @abstractmethod
    def setPosition(self, position: tuple):
        raise NotImplementedError

    @abstractmethod
    def addItem(self, item: ItemState):
        raise NotImplementedError

    @abstractmethod
    def setPaid(self, paid: bool):
        raise NotImplementedError
