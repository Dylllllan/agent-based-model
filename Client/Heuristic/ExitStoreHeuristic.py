import random

from Heuristic.NavigationHeuristic import NavigationHeuristic
from Store.Store import Store


class ExitStoreHeuristic(NavigationHeuristic):
    def __init__(self, store: Store):
        super().__init__(store)

        self.doorPositions = []
        self.store.MapObservable.subscribe(lambda _: self.chooseDoor())

    def chooseDoor(self):
        # Choose a random door
        self.setDestination(random.choice(self.store.getDoors()).position)
