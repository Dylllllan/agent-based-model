from abc import ABC

from Agent.AgentState import AgentState
from Heuristic.Heuristic import Heuristic
from Store.Store import Store
from Store.Tile import Tile
from Utils import distanceBetweenPoints


class NavigationHeuristic(Heuristic, ABC):
    def __init__(self, store: Store):
        super().__init__(store)

        self.waypoint = None
        self.destination = None

        self.passedWaypoint = False
        self.destinationOffset = 0.0

    def setDestination(self, destination: tuple, offset: float = 0.0):
        self.waypoint = None
        self.passedWaypoint = False

        self.destination = destination
        self.destinationOffset = offset

    def findWaypoint(self) -> Tile:
        waypoints = self.store.getWaypoints()
        # Get the waypoint closest to the destination
        closestWaypoint = min(waypoints,
                              key=lambda waypoint: distanceBetweenPoints(waypoint.position, self.destination))
        # Return the closest waypoint
        return closestWaypoint

    def evaluate(self, state: AgentState) -> float:
        if self.destination is None:
            raise ValueError("Destination is not set")

        if self.waypoint is None:
            # Find the waypoint that is closest to the destination
            self.waypoint = self.findWaypoint()
            # print("Found waypoint at", self.waypoint.position)

        if not self.passedWaypoint:
            # Get the current distance from the agent to the waypoint
            currentAgentState = self.store.getAgent(state.id)
            currentDistanceToWaypoint = distanceBetweenPoints(currentAgentState.position, self.waypoint.position)

            if currentDistanceToWaypoint < 1.0:
                # print("Agent passed waypoint at ", self.waypoint.position, "for destination", self.destination)
                self.passedWaypoint = True

        # If the agent has passed the waypoint, the heuristic should return the distance to the destination
        if self.passedWaypoint:
            # Get the distance from the agent to the destination
            distanceToDestination = distanceBetweenPoints(state.position, self.destination)

            return distanceToDestination + self.destinationOffset
        else:
            # Otherwise, the heuristic should return the distance to the waypoint
            # Add 1.0 to the distance so the heuristic will always return a value greater than 0

            # Get the distance from the agent to the waypoint
            distanceToWaypoint = distanceBetweenPoints(state.position, self.waypoint.position)

            return distanceToWaypoint + 1.0
