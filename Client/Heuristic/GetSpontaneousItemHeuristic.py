from Heuristic.GetItemHeuristic import GetItemHeuristic
from Heuristic.SpontaneityHeuristic import SpontaneityHeuristic
from Store.Store import Store


class GetSpontaneousItemHeuristic(SpontaneityHeuristic):
    def __init__(self, store: Store, params: dict):
        super().__init__(store, params)

        self.category = params["category"]
        self.setHeuristic(GetItemHeuristic(store, {"category": self.category}))
