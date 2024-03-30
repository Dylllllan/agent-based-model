from Heuristic.GetNearbyItemHeuristic import GetNearbyItemHeuristic
from Heuristic.SpontaneityHeuristic import SpontaneityHeuristic
from Store.Store import Store


class GetSpontaneousNearbyItemHeuristic(SpontaneityHeuristic):
    def __init__(self, store: Store, params: dict):
        super().__init__(store, params)

        self.distance = params["distance"]
        self.setHeuristic(GetNearbyItemHeuristic(store, {"distance": self.distance}))
