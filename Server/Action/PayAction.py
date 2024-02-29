from Action.Action import Action
from Agent.IAgent import IAgent


class PayAction(Action):
    def DoAction(self, agent: IAgent):
        # Mark the agent as having paid
        agent.setPaid(True)
