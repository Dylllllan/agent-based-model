from reactivex import Observable
from reactivex.subject import ReplaySubject

from Agent.AgentState import AgentState
from Agent.AgentType import AgentType
from Store.Tile import Tile, Shelf
from Store.TileType import TileType


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

    def getShelves(self) -> list:
        return [tile for tile in self.map if tile.type == TileType.SHELF]

    def getCheckouts(self) -> list:
        return [tile for tile in self.map if tile.type == TileType.CHECKOUT]

    def getDoors(self) -> list:
        return [tile for tile in self.map if tile.type == TileType.DOOR]

    def getAgent(self, agentId: str) -> AgentState:
        return next(agent for agent in self.agents if agent.id == agentId)

    def getAgentsByType(self, agentType: AgentType) -> list:
        return [agent for agent in self.agents if agent.agentType == agentType]

    def isPositionInBounds(self, position: tuple) -> bool:
        return 0 <= position[0] < self.width and 0 <= position[1] < self.height

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
            return Shelf(tileData["name"], tileData["price"], position, tileData["icon"])
        else:
            return Tile(position, tileType)
