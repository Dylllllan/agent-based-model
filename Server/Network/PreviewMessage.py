from Agent.AgentState import AgentState
from Core.ISerializable import ISerializable


class PreviewMessage(ISerializable):
    def __init__(self, agentState: AgentState):
        self.agentState = agentState

    def toDict(self) -> dict:
        return {
            "agentState": self.agentState.toDict()
        }
