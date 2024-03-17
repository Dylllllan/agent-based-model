from abc import ABC
from random import random

from Agent.AgentState import AgentState
from Heuristic.Heuristic import Heuristic
from Heuristic.HeuristicWithParameters import HeuristicWithParameters
from Store.Store import Store


class SpontaneityHeuristic(HeuristicWithParameters, ABC):
    def __init__(self, store: Store, params: dict):
        super().__init__(store)

        # This is to out-weigh other heuristics occurring at the same time
        self.weight = int(params["weight"])
        # This is evaluated at each time step, and so should be quite low to be effective
        self.probability = float(params["probability"])

        self.active = False
        self.activated = False
        self.heuristic = None

        store.AgentsObservable.subscribe(on_next=lambda _: self.onTimeStep())

    def onTimeStep(self):
        if not self.active or self.activated:
            return

        # Randomly activate the heuristic based on the probability
        self.activated = random() < self.probability

        if self.activated:
            print("Spontaneity heuristic activated")

    def setHeuristic(self, heuristic: Heuristic):
        self.heuristic = heuristic

    def evaluate(self, state: AgentState) -> float:
        if self.heuristic is None:
            raise ValueError("No heuristic set")

        # Set the heuristic to active if it has been evaluated at least once
        self.active = True

        # If the spontaneity heuristic is not active, return 0
        if not self.activated:
            return 0.0
        else:
            # Otherwise, evaluate the heuristic and multiply by the weight
            return self.weight * self.heuristic.evaluate(state)
