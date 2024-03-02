from Heuristic.GoToCheckoutHeuristic import GoToCheckoutHeuristic
from Heuristic.GoToDoorHeuristic import GoToDoorHeuristic
from Heuristic.GoToItemHeuristic import GoToItemHeuristic
from Heuristic.HeuristicWithParameters import HeuristicWithParameters
from Heuristic.PayForItemsHeuristic import PayForItemsHeuristic
from Heuristic.PickUpItemHeuristic import PickUpItemHeuristic
from Store.Store import Store

HEURISTIC_NAME_TO_CLASS = {"GoToCheckoutHeuristic": GoToCheckoutHeuristic,
                           "GoToDoorHeuristic": GoToDoorHeuristic,
                           "GoToItemHeuristic": GoToItemHeuristic,
                           "PayForItemsHeuristic": PayForItemsHeuristic,
                           "PickUpItemHeuristic": PickUpItemHeuristic}


class HeuristicFactory:
    @staticmethod
    def createHeuristics(configuration: list, store: Store) -> list:
        heuristicList = []

        for setConfiguration in configuration:
            heuristicSet = []
            for heuristic in setConfiguration:
                heuristicClass = HEURISTIC_NAME_TO_CLASS[heuristic["name"]]
                if issubclass(heuristicClass, HeuristicWithParameters):
                    heuristicSet.append(heuristicClass(store, heuristic["parameters"]))
                else:
                    heuristicSet.append(heuristicClass(store))
            heuristicList.append(heuristicSet)

        return heuristicList
