from Heuristic.CheckoutHeuristic import CheckoutHeuristic
from Heuristic.ExitStoreHeuristic import ExitStoreHeuristic
from Heuristic.GetItemHeuristic import GetItemHeuristic
from Heuristic.GetRandomItemHeuristic import GetRandomItemHeuristic
from Heuristic.GetSpontaneousItemHeuristic import GetSpontaneousItemHeuristic
from Heuristic.GetSpontaneousRandomItemHeuristic import GetSpontaneousRandomItemHeuristic
from Heuristic.Heuristic import Heuristic
from Heuristic.HeuristicWithParameters import HeuristicWithParameters
from Heuristic.WanderingHeuristic import WanderingHeuristic
from Store.Store import Store

HEURISTICS = [
    GetItemHeuristic,
    ExitStoreHeuristic,
    CheckoutHeuristic,
    GetRandomItemHeuristic,
    WanderingHeuristic,
    GetSpontaneousItemHeuristic,
    GetSpontaneousRandomItemHeuristic,
    WanderingHeuristic
]


class HeuristicFactory:
    @staticmethod
    def createHeuristic(configuration: dict, store: Store) -> Heuristic:
        heuristicName = configuration["name"]

        heuristicClass = next((heuristic for heuristic in HEURISTICS if heuristic.__name__ == heuristicName), None)
        if heuristicClass is None:
            raise ValueError("Invalid heuristic name")

        if issubclass(heuristicClass, HeuristicWithParameters):
            return heuristicClass(store, configuration["parameters"])
        else:
            return heuristicClass(store)

    @staticmethod
    def createHeuristicSet(configuration: list, store: Store) -> list:
        return [HeuristicFactory.createHeuristic(heuristic, store) for heuristic in configuration]

    @staticmethod
    def createHeuristics(configuration: list, store: Store) -> list:
        heuristicSets = []

        for setConfiguration in configuration:
            if isinstance(setConfiguration, list):
                heuristicSets.append(HeuristicFactory.createHeuristicSet(setConfiguration, store))
            elif isinstance(setConfiguration, dict):
                heuristicSets.append([HeuristicFactory.createHeuristic(setConfiguration, store)])
            else:
                raise ValueError("Invalid configuration")

        return heuristicSets
