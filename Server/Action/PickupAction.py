from Server.Action.Action import Action
from Server.Agent.IAgent import IAgent
from Server.Store.ItemState import ItemState


class PickupAction(Action):
    def __init__(self, itemState: ItemState):
        self.itemState = itemState

    def DoAction(self, agent: IAgent):
        # Add the item to the agent
        agent.addItem(self.itemState)
