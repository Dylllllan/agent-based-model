import uuid

from reactivex import Observable, Subject
from reactivex.abc import DisposableBase
from reactivex.disposable import CompositeDisposable

from Agent.AgentState import AgentState
from Agent.AgentType import AgentType
from Agent.IAgent import IAgent
from Agent.IAgentChannel import IAgentChannel
from Store.Item import Item
from Store.ItemState import ItemState


class Agent(IAgent, DisposableBase):
    def __init__(self, channel: IAgentChannel, agentType: AgentType, position: tuple) -> None:
        self.id = str(uuid.uuid4())
        self.channel = channel
        self.compositeDisposable = CompositeDisposable()

        self.type = agentType
        self.position = position
        self.items = []
        self.paid = False

        self.itemSubject = Subject()
        self.compositeDisposable.add(self.itemSubject)

    def setPosition(self, position: tuple):
        self.position = position
        # Update the position of all items
        for item in self.items:
            item.setPosition(position)

    def addItem(self, itemState: ItemState):
        item = Item(itemState, self.position)
        self.compositeDisposable.add(item)

        # Set the position for the current timestep
        self.setPosition(self.position)

        self.items.append(item)
        self.itemSubject.on_next(item)

    def setPaid(self, paid: bool):
        self.paid = paid
        # Set the position for the current timestep
        self.setPosition(self.position)

    def toAgentState(self) -> AgentState:
        return AgentState(self.id, self.type, self.position, self.items, self.paid)

    @property
    def ItemObservable(self) -> Observable:
        return self.itemSubject

    def leaveStore(self, onDoor: bool):
        for item in self.items:
            item.remove(onDoor)

    def dispose(self):
        self.compositeDisposable.dispose()
        # Kick the network channel
        self.channel.Kick()
