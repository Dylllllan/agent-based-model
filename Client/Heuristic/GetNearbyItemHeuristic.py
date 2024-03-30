import random

from Agent.AgentState import AgentState
from Heuristic.HeuristicWithParameters import HeuristicWithParameters
from Heuristic.NavigationHeuristic import NavigationHeuristic
from Store.Store import Store
from Utils import distanceBetweenPoints


class GetNearbyItemHeuristic(NavigationHeuristic, HeuristicWithParameters):
    def __init__(self, store: Store, params: dict):
        super().__init__(store)

        self.distance = params["distance"]
        self.shelf = None

    def chooseShelf(self, agentPosition: tuple):
        while self.shelf is None:
            # Get all items within a certain distance of the initial position
            nearbyShelves = [shelf for shelf in self.store.getShelves() if
                             distanceBetweenPoints(agentPosition, shelf.position) <= self.distance]

            # Randomly choose and set a nearby shelf
            if len(nearbyShelves) > 0:
                self.shelf = random.choice(nearbyShelves)
                self.setDestination(self.shelf.position)
            else:
                # Increase the distance if no shelves are found
                self.distance += 1

    def evaluate(self, state: AgentState) -> float:
        # If the shelf is not set, we should choose one
        if self.shelf is None:
            self.chooseShelf(self.store.getAgent(state.id).position)

        # If the agent has the shelf item, return 0
        if state.hasItemName(self.shelf.name):
            return 0.0
        else:
            return super().evaluate(state)
