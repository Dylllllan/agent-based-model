from Heuristic.HeuristicWithParameters import HeuristicWithParameters
from Heuristic.NavigationHeuristic import NavigationHeuristic
from Store.Store import Store


class GoToItemHeuristic(NavigationHeuristic, HeuristicWithParameters):
    def __init__(self, store: Store, params: dict):
        super().__init__(store)

        self.category = params["category"]
        self.shelf = None

        self.store.MapObservable.subscribe(lambda _: self.getShelf())

    def getShelf(self):
        self.shelf = next(shelf for shelf in self.store.getShelves() if shelf.category == self.category)
        self.setDestination(self.shelf.position, -1.0)
