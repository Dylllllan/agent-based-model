from Action.Action import Action
from Agent.IAgent import IAgent


class MoveAction(Action):
    def __init__(self, position: tuple):
        self.position = position

    def DoAction(self, agent: IAgent):
        # Update the agent position to match the action position
        agent.setPosition(self.position)
