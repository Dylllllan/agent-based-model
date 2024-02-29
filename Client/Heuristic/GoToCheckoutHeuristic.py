from Agent.AgentState import AgentState
from Heuristic.Heuristic import Heuristic
from Store.Store import Store
from Utils import distanceBetweenPoints


class GoToCheckoutHeuristic(Heuristic):
    def __init__(self, store: Store):
        super().__init__(store)

        self.checkoutPositions = []
        self.store.MapObservable.subscribe(lambda _: self.getCheckoutPositions())

    def getCheckoutPositions(self):
        self.checkoutPositions = [checkout.position for checkout in self.store.getCheckouts()]

    def evaluate(self, state: AgentState) -> float:
        # Get the distance to the closest checkout
        distanceToClosestCheckout = min(
            [distanceBetweenPoints(state.position, checkoutPosition) for checkoutPosition in self.checkoutPositions])

        return distanceToClosestCheckout - 1.0
