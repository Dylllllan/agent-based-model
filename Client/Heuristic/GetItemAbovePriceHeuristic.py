import random

from Agent.AgentState import AgentState
from Heuristic.HeuristicWithParameters import HeuristicWithParameters
from Heuristic.NavigationHeuristic import NavigationHeuristic
from Store.Store import Store


class GetItemAbovePriceHeuristic(NavigationHeuristic, HeuristicWithParameters):
    def __init__(self, store: Store, params: dict):
        super().__init__(store)

        self.price = params["price"]
        self.shelf = None

        self.store.MapObservable.subscribe(lambda _: self.getShelf())

    def getShelf(self):
        self.shelf = random.choice([shelf for shelf in self.store.getShelves() if shelf.price >= self.price])
        self.setDestination(self.shelf.position)

    def evaluate(self, state: AgentState) -> float:
        # If the agent has the item, return 0
        if state.hasItemName(self.shelf.name):
            return 0.0
        else:
            return super().evaluate(state)
