import random

from Agent.AgentState import AgentState
from Heuristic.GetItemHeuristic import GetItemHeuristic
from Heuristic.Heuristic import Heuristic
from Store.Store import Store


class GetRandomItemHeuristic(Heuristic):
    def __init__(self, store: Store):
        super().__init__(store)

        self.heuristic = None

        self.store.MapObservable.subscribe(lambda _: self.chooseCategory())

    def chooseCategory(self):
        category = random.choice(self.store.getItemCategories())
        print("Chosen category:", category)
        self.heuristic = GetItemHeuristic(self.store, {"category": category})

    def evaluate(self, state: AgentState) -> float:
        return self.heuristic.evaluate(state)
