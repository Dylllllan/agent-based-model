from Agent.AgentType import AgentType
from Store.ItemState import ItemState


class AgentState:
    def __init__(self, data: dict):
        self.id = data["id"]
        self.agentType = AgentType(data["agentType"])
        self.position = (data["position"][0], data["position"][1])
        self.items = [ItemState(item) for item in data["items"]]
        self.paid = data["paid"]

    def hasItemCategory(self, itemCategory: str) -> bool:
        return any(item.category == itemCategory for item in self.items)
