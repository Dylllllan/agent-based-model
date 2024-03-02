import random

from Heuristic.NavigationHeuristic import NavigationHeuristic
from Store.Store import Store


class GoToCheckoutHeuristic(NavigationHeuristic):
    def __init__(self, store: Store):
        super().__init__(store)

        self.store.MapObservable.subscribe(lambda _: self.chooseCheckout())

    def chooseCheckout(self):
        # Choose a random checkout
        self.setDestination(random.choice(self.store.getCheckouts()).position, -1.0)
