import random

from Agent.AgentState import AgentState
from Heuristic.HeuristicWithParameters import HeuristicWithParameters
from Heuristic.NavigationHeuristic import NavigationHeuristic
from Store.Store import Store


# Navigate to the shelf of a specific category and pick up an item
class GetItemHeuristic(NavigationHeuristic, HeuristicWithParameters):
    def __init__(self, store: Store, params: dict):
        super().__init__(store)

        self.category = params["category"]

        self.store.MapObservable.subscribe(lambda _: self.getShelf())

    def getShelf(self):
        shelf = random.choice([shelf for shelf in self.store.getShelves() if shelf.category == self.category])
        self.setDestination(shelf.position)

    def evaluate(self, state: AgentState) -> float:
        # If the agent has the item, return 0
        if state.hasItemCategory(self.category):
            return 0.0
        else:
            return super().evaluate(state)
