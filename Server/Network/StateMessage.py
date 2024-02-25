from Server.Core.ISerializable import ISerializable


class StateMessage(ISerializable):
    def __init__(self, step: int, agents: list):
        self.step = step
        self.agents = list(a.toAgentState() for a in agents)

    def toDict(self) -> dict:
        return {
            "step": self.step,
            "agents": list(a.toDict() for a in self.agents)
        }
