import random

from Heuristic.DistanceHeuristic import DistanceHeuristic
from Store.Store import Store


class DistanceFromItemHeuristic(DistanceHeuristic):
    def __init__(self, store: Store, params: dict):
        super().__init__(store, params)

        self.category = params["category"]

        self.store.MapObservable.subscribe(lambda _: self.getShelfTarget())

    def getShelfTarget(self):
        shelf = random.choice([shelf for shelf in self.store.getShelves() if shelf.category == self.category])
        self.setTarget(shelf.position)
