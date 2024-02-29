from Agent.AgentState import AgentState
from Heuristic.Heuristic import Heuristic
from Store.Store import Store
from Utils import distanceBetweenPoints


class GoToItemHeuristic(Heuristic):
    def __init__(self, params: dict, store: Store):
        super().__init__(store)

        self.itemName = params["itemName"]
        self.shelf = None

        self.store.MapObservable.subscribe(lambda _: self.getShelf())

    def getShelf(self):
        self.shelf = next(shelf for shelf in self.store.getShelves() if shelf.name == self.itemName)

    def evaluate(self, state: AgentState) -> float:
        return distanceBetweenPoints(state.position, self.shelf.position) - 1.0
