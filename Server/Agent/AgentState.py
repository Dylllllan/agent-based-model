from Agent.AgentType import AgentType
from Agent.IAgent import IAgent
from Core.ISerializable import ISerializable
from Store.ItemState import ItemState


class AgentState(IAgent, ISerializable):
    def __init__(self, id: str, agentType: AgentType, position: tuple, items: list, paid: bool):
        self.id = id
        self.agentType = agentType
        self.position = position
        self.items = list(i.toItemState() for i in items)
        self.paid = paid

    def setPosition(self, position: tuple):
        self.position = position

    def addItem(self, itemState: ItemState):
        self.items.append(itemState)

    def hasItem(self, itemState: ItemState) -> bool:
        for item in self.items:
            if item.name == itemState.name:
                return True
        return False

    def setPaid(self, paid: bool):
        self.paid = paid

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "agentType": self.agentType,
            "position": self.position,
            "items": [i.toDict() for i in self.items],
            "paid": self.paid
        }
