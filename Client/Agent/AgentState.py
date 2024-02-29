from Store.ItemState import ItemState
from Agent.AgentType import AgentType


class AgentState:
    def __init__(self, data: dict):
        self.id = data["id"]
        self.agentType = AgentType(data["agentType"])
        self.position = (data["position"][0], data["position"][1])
        self.items = [ItemState(item) for item in data["items"]]
        self.paid = data["paid"]

    def hasItem(self, itemName: str) -> bool:
        return any(item.name == itemName for item in self.items)
