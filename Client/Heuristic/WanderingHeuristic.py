import random

from Heuristic.NavigationHeuristic import NavigationHeuristic
from Store.Store import Store


class WanderingHeuristic(NavigationHeuristic):
    def __init__(self, store: Store):
        super().__init__(store)

        self.store.MapObservable.subscribe(lambda _: self.chooseRandomTile())

    def chooseRandomTile(self):
        # Choose a random tile that can be moved to
        self.setDestination(random.choice(self.store.getMovableTiles()).position)
        # Output the destination that was chosen
        # print("Wandering destination: ", self.destination)
