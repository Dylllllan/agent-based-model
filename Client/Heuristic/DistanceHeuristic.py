from _ast import Store
from abc import ABC

from Agent.AgentState import AgentState
from Heuristic.HeuristicWithParameters import HeuristicWithParameters
from Heuristic.NavigationHeuristic import NavigationHeuristic
from Store.TileType import TileType
from Utils import distanceBetweenPoints


class DistanceHeuristic(HeuristicWithParameters, ABC):
    def __init__(self, store: Store, params: dict):
        super().__init__(store)

        self.distance = params["distance"]
        if self.distance < 0:
            # If we are trying to move closer to a position, embed a navigation heuristic
            self.navigationHeuristic = NavigationHeuristic(store)

        self.target = None

    def setTarget(self, position: tuple):
        self.target = position

        if self.distance < 0:
            # If we are trying to move closer to a position, set the destination of the navigation heuristic
            self.navigationHeuristic.setDestination(self.target)

    def evaluate(self, state: AgentState) -> float:
        if self.store.getTile(state.position).type == TileType.DOOR:
            # If the agent is trying to move to a door, the heuristic should return a high score to deter
            return 1000

        currentAgentState = self.store.getAgent(state.id)

        # If the agent is stuck in a corner, immediately satisfy the heuristic
        if self.store.isPositionCorner(currentAgentState.position):
            # If the agent is trying to pick an item or pay while stuck in a corner,
            # the heuristic should return a high score to deter the action
            if len(currentAgentState.items) < len(state.items) or currentAgentState.paid != state.paid:
                return 1000
            else:
                return 0

        if self.distance < 0:
            # The aim of the heuristic is for the agent to move closer to the target

            navigationScore = self.navigationHeuristic.evaluate(state)

            # If the agent has not passed the waypoint, the heuristic should return the navigation score
            if not self.navigationHeuristic.passedWaypoint:
                return navigationScore
            else:
                # Otherwise, the heuristic should add the distance to the navigation score
                return navigationScore + self.distance
        else:
            # The aim of the heuristic is for the agent to move away from the target
            return self.distance - distanceBetweenPoints(state.position, self.target)
