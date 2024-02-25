from Server.Action.MoveAction import MoveAction
from Server.Agent.IAgent import IAgent


class LeaveAction(MoveAction):
    def DoAction(self, agent: IAgent):
        super().DoAction(agent)
        # Can we do some kind of post-action to disconnect the agent?
