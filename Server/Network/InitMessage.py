from Server.Core.ISerializable import ISerializable
from Server.Store.Store import Store


class InitMessage(ISerializable):
    def __init__(self, agentId: str, store: Store):
        self.agentId = agentId
        self.store = store

    def toDict(self) -> dict:
        return {
            "agentId": self.agentId,
            "store": self.store.toDict()
        }
