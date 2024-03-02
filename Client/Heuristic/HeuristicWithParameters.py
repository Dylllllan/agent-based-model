from abc import ABC

from Heuristic.Heuristic import Heuristic
from Store.Store import Store


class HeuristicWithParameters(Heuristic, ABC):
    def __init__(self, store: Store, params: dict = None):
        Heuristic.__init__(self, store)
