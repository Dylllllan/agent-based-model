from json import load

from Heuristic.GoToCheckoutHeuristic import GoToCheckoutHeuristic
from Heuristic.GoToDoorHeuristic import GoToDoorHeuristic
from Heuristic.GoToItemHeuristic import GoToItemHeuristic
from Heuristic.PayForItemsHeuristic import PayForItemsHeuristic
from Heuristic.PickUpItemHeuristic import PickUpItemHeuristic
from Store.Store import Store


class HeuristicFactory():
    def __init__(self, configFilePath: str, store: Store):
        self.configFilePath = configFilePath
        self.store = store
        # Use a dictionary to map class names to actual classes, to avoid using globals()
        self.heuristics_map = {"GoToCheckoutHeuristic": GoToCheckoutHeuristic,
                               "GoToDoorHeuristic": GoToDoorHeuristic,
                               "GoToItemHeuristic": GoToItemHeuristic,
                               "PayForItemsHeuristic": PayForItemsHeuristic,
                               "PickUpItemHeuristic": PickUpItemHeuristic}

    def createHeuristics(self) -> list:
        # Load config file
        with open(self.configFilePath, "r") as file:
            heuristic_super_dict = load(file)
        result = []
        for heuristic_set in heuristic_super_dict["heuristics"]:
            heuristic_objects = []
            for heuristic_dict in heuristic_set:
                # Check if there are parameters or not
                params = heuristic_dict.get("parameters", None)
                # Retrieve the correct heuristic class to instantiate
                heuristic_class = self.heuristics_map[heuristic_dict["name"]]
                if params is None:
                    heuristic_objects.append(heuristic_class(self.store))
                else:
                    heuristic_objects.append(heuristic_class(params, self.store))
            result.append(heuristic_objects)
        return result
