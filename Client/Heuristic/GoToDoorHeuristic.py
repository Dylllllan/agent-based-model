from Client.Agent.AgentState import AgentState
from Client.Heuristic.Heuristic import Heuristic
from Client.Store.Store import Store
from Client.Utils import distanceBetweenPoints


class GoToDoorHeuristic(Heuristic):
    def __init__(self, store: Store):
        super().__init__(store)

        self.doorPositions = []
        self.store.MapObservable.subscribe(lambda _: self.getDoorPositions())

    def getDoorPositions(self):
        self.doorPositions = [checkout.position for checkout in self.store.getDoors()]

    def evaluate(self, state: AgentState) -> float:
        # Get the distance to the closest door
        distanceToClosestDoor = min(
            [distanceBetweenPoints(state.position, doorPosition) for doorPosition in self.doorPositions])

        return distanceToClosestDoor
