import uuid

from reactivex import Observable, Subject
from reactivex.abc import DisposableBase
from reactivex.disposable import CompositeDisposable

from Server.Agent.AgentState import AgentState
from Server.Agent.AgentType import AgentType
from Server.Agent.IAgent import IAgent
from Server.Agent.IAgentChannel import IAgentChannel
from Server.Store.Item import Item
from Server.Store.ItemState import ItemState


class Agent(IAgent, DisposableBase):
    def __init__(self, channel: IAgentChannel, agentType: AgentType) -> None:
        self.id = str(uuid.uuid4())
        self.channel = channel
        self.compositeDisposable = CompositeDisposable()

        self.type = agentType
        self.position = (0, 0)
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

        self.items.append(item)
        self.itemSubject.on_next(item)

    def setPaid(self, paid: bool):
        self.paid = paid

    def toAgentState(self) -> AgentState:
        return AgentState(self.id, self.type, self.position, self.items, self.paid)

    @property
    def ItemObservable(self) -> Observable:
        return self.itemSubject

    def dispose(self):
        self.compositeDisposable.dispose()
        # Kick the network channel
        self.channel.Kick()
