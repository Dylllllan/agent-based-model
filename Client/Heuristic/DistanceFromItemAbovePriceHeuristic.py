import random

from Heuristic.DistanceHeuristic import DistanceHeuristic
from Store.Store import Store


class DistanceFromItemAbovePriceHeuristic(DistanceHeuristic):
    def __init__(self, store: Store, params: dict):
        super().__init__(store, params)

        self.price = params["price"]

        self.store.MapObservable.subscribe(lambda _: self.getShelfTarget())

    def getShelfTarget(self):
        shelf = random.choice([shelf for shelf in self.store.getShelves() if shelf.price >= self.price])
        self.setTarget(shelf.position)
