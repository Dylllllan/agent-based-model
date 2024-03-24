from Agent.AgentType import AgentType
from Agent.IAgentClient import IAgentClient
from Store.Store import Store
from Store.TileType import TileType
from Utils import getPositionInDirection


class Controller:
    def __init__(self, agentType: AgentType, client: IAgentClient, store: Store):
        self.client = client
        self.store = store

        # When the client is connected, send the agent type to the server
        self.client.ConnectionObservable.subscribe(lambda _: self.client.sendInit(agentType))

        self.agentId = None
        self.client.AgentIdObservable.subscribe(lambda agentId: self.setAgentId(agentId))

        self.store.AgentsObservable.subscribe(lambda agents: self.checkIfEndGame())

    def setAgentId(self, agentId: str):
        print("Received agent id: ", agentId)
        self.agentId = agentId

    def checkIfEndGame(self):
        # Get the current agent state
        agentState = self.store.getAgent(self.agentId)

        # If the agent has more than one item and is on a door, end the game
        if len(agentState.items) > 0 and self.store.getTile(agentState.position).type == TileType.DOOR:
            self.client.Close()

    def moveInDirection(self, direction: tuple):
        # Get the current agent state
        currentPosition = self.store.getAgent(self.agentId).position

        validDirections = self.store.getDirectionsFromPosition(currentPosition)
        if direction not in validDirections:
            print("ERROR: Invalid direction")
            return

        nextPosition = getPositionInDirection(currentPosition, direction)

        # Send the position to the server and commit
        self.client.sendSelect(nextPosition)
        self.client.sendCommit()
