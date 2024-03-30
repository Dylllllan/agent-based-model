from reactivex import Observable
from reactivex.subject import ReplaySubject

from Agent.AgentState import AgentState
from Agent.AgentType import AgentType
from Store.Tile import Tile, Shelf
from Store.TileType import TileType
from Utils import getPositionInDirection


class Store:
    def __init__(self, mapObservable: Observable, stateObservable: Observable):
        self.width = 0
        self.height = 0

        self.map = []
        self.agents = []

        mapObservable.subscribe(lambda data: self.fromMapData(data))
        stateObservable.subscribe(lambda data: self.fromStateData(data))

        self.mapSubject = ReplaySubject(1)
        self.agentsSubject = ReplaySubject(1)

    @property
    def MapObservable(self) -> Observable:
        return self.mapSubject

    @property
    def AgentsObservable(self) -> Observable:
        return self.agentsSubject

    def fromMapData(self, data: dict):
        self.width = data["size"]["width"]
        self.height = data["size"]["height"]

        self.map = [Store.createTile(tileData) for tileData in data["map"]]
        self.mapSubject.on_next(self.map)

    def fromStateData(self, data: dict):
        self.agents = [AgentState(agentData) for agentData in data["agents"]]
        self.agentsSubject.on_next(self.agents)

    def getTile(self, position: tuple) -> Tile:
        return self.map[(position[1] * self.width) + position[0]]

    def getTilesOfType(self, tileType: TileType) -> list:
        return [tile for tile in self.map if tile.type == tileType]

    def getMovableTiles(self) -> list:
        # Union a list of type TILE and WAYPOINT
        return self.getTilesOfType(TileType.TILE) + self.getTilesOfType(TileType.WAYPOINT)

    def getShelves(self) -> list:
        return self.getTilesOfType(TileType.SHELF)

    def getCheckouts(self) -> list:
        return self.getTilesOfType(TileType.CHECKOUT)

    def getDoors(self) -> list:
        return self.getTilesOfType(TileType.DOOR)

    def getWaypoints(self) -> list:
        return self.getTilesOfType(TileType.WAYPOINT)

    # Get a list of all unique item categories in the store
    def getItemCategories(self) -> list:
        return list(set([shelf.category for shelf in self.getShelves()]))

    def getAgent(self, agentId: str) -> AgentState:
        return next(agent for agent in self.agents if agent.id == agentId)

    def getAgentsByType(self, agentType: AgentType) -> list:
        return [agent for agent in self.agents if agent.agentType == agentType]

    def isPositionInBounds(self, position: tuple) -> bool:
        return 0 <= position[0] < self.width and 0 <= position[1] < self.height

    def isPositionCorner(self, position: tuple) -> bool:
        # Get the directions from the position
        directions = self.getDirectionsFromPosition(position)
        # Filter the directions to only include tiles that are TILE or WAYPOINT
        # If there are only 2 or fewer directions, the position is a corner
        return len([direction for direction in directions if self.getTile(
            getPositionInDirection(position, direction)).type in [TileType.TILE, TileType.WAYPOINT]]) <= 2

    def getDirectionsFromPosition(self, position: tuple) -> list:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        # Exclude directions that would go out of bounds
        return [direction for direction in directions if
                self.isPositionInBounds((position[0] + direction[0], position[1] + direction[1]))]

    @staticmethod
    def createTile(tileData: dict) -> Tile:
        position = (tileData["position"][0], tileData["position"][1])
        tileType = TileType(tileData["type"])

        if tileType == TileType.SHELF:
            return Shelf(position, tileData["name"], tileData["category"], tileData["price"], tileData["icon"])
        else:
            return Tile(position, tileType)
