import random

from Agent.Agent import Agent
from Agent.AgentType import AgentType
from Agent.IAgentChannel import IAgentChannel
from Game.GameTimeStep import GameTimeStep
from Network.StateMessage import StateMessage
from Store.ItemObserver import ItemObserver
from Store.Store import Store
from Store.TileType import TileType

MIN_PLAYERS = 1


class Game:
    def __init__(self, configFilePath: str):
        self.store = Store(configFilePath)

        self.agents = []
        self.addedAgentQueue = []
        self.removedAgentQueue = []

        self.timeStep = 0
        self.currentStep = None
        self.running = False

    def addAgent(self, agentChannel: IAgentChannel, agentType: AgentType) -> Agent:
        # Choose a random door from the store to spawn the agent on
        door = random.choice(self.store.getDoors())

        # Create the agent
        agent = Agent(agentChannel, agentType, door.position)
        self.addedAgentQueue.append(agent)

        itemObserver = agent.ItemObservable.subscribe(
            lambda item: item.addPositionObserver(
                ItemObserver(item, self.timeStep, self.store, agentType == AgentType.SHOPLIFTER)
            )
        )
        agent.compositeDisposable.add(itemObserver)

        # Send an initial message to the agent
        agent.channel.SendInit(agent.id, self.store)

        if len(self.getPendingPlayingAgents()) == MIN_PLAYERS and not self.running:
            # Start the game
            self.nextTimeStep()

        return agent

    def getPendingPlayingAgents(self) -> list:
        # The agents in the queue that are not spectators
        return [agent for agent in self.addedAgentQueue if agent.type != AgentType.SPECTATOR]

    def getPlayingAgents(self) -> list:
        return [agent for agent in self.agents if agent.type != AgentType.SPECTATOR]

    def removeAgent(self, agent: Agent):
        # Queue the agent as removed on the next round
        self.removedAgentQueue.append(agent)

    def sendStateToAgents(self):
        state = StateMessage(self.timeStep, self.getPlayingAgents())
        for agent in self.agents:
            agent.channel.SendState(state)

    def nextTimeStep(self):
        print("Time step " + str(self.timeStep) + " complete. Starting next time step.")

        if self.currentStep is not None:
            self.currentStep.dispose()

        # Add new agents
        for agent in self.addedAgentQueue:
            self.agents.append(agent)

        self.addedAgentQueue.clear()

        # Remove agents
        for agent in self.removedAgentQueue:
            agentOnDoor = self.store.getTile(agent.position).type == TileType.DOOR
            agent.leaveStore(agentOnDoor)

            self.agents.remove(agent)

        self.removedAgentQueue.clear()

        # If there are no playing agents, pause the game
        if len(self.getPlayingAgents()) == 0:
            print("No playing agents remaining. Pausing game.")

            self.running = False
            self.sendStateToAgents()

            return

        # print("Continuing game with " + str(len(self.agents)) + " agents.")

        # Increment the time step
        self.timeStep += 1
        self.running = True

        # Send the next timestep state to all agents
        self.sendStateToAgents()

        # Create the next time step
        self.currentStep = GameTimeStep(self.timeStep, self.getPlayingAgents(), self.store)

        # Subscribe to the complete observable
        completeObserver = self.currentStep.CompleteObservable.subscribe(
            on_completed=lambda: self.nextTimeStep()
        )
        # Add the complete observer to the composite disposable
        self.currentStep.compositeDisposable.add(completeObserver)
