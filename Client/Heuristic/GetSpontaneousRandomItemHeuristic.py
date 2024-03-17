from Heuristic.GetRandomItemHeuristic import GetRandomItemHeuristic
from Heuristic.SpontaneityHeuristic import SpontaneityHeuristic
from Store.Store import Store


class GetSpontaneousRandomItemHeuristic(SpontaneityHeuristic):
    def __init__(self, store: Store, params: dict):
        super().__init__(store, params)

        self.setHeuristic(GetRandomItemHeuristic(store))
