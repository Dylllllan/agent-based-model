from Agent.Agent import Agent
from Agent.AgentType import AgentType
from Agent.IAgentChannel import IAgentChannel
from Game.GameTimeStep import GameTimeStep
from Network.StateMessage import StateMessage
from Store.ItemObserver import ItemObserver
from Store.Store import Store

CONFIGURATION_PATH = "Configuration/store1.json"
MIN_PLAYERS = 1


class Game:
    def __init__(self):
        self.store = Store(CONFIGURATION_PATH)

        self.agents = []
        self.addedAgentQueue = []
        self.removedAgentQueue = []

        self.timeStep = 0
        self.currentStep = None
        self.running = False

    def addAgent(self, agentChannel: IAgentChannel, agentType: AgentType) -> Agent:
        agent = Agent(agentChannel, agentType)
        self.addedAgentQueue.append(agent)

        itemObserver = agent.ItemObservable.subscribe(
            lambda item: item.addPositionObserver(
                ItemObserver(item.id, self.timeStep, self.store)
            )
        )
        agent.compositeDisposable.add(itemObserver)

        # Send an initial message to the agent
        agent.channel.SendInit(agent.id, self.store)

        # agent.addItem(ItemState("item1", 0))

        if len(self.addedAgentQueue) == MIN_PLAYERS and not self.running:
            # Start the game
            self.nextTimeStep()

        return agent

    def removeAgent(self, agent: Agent):
        # Queue the agent as removed on the next round
        self.removedAgentQueue.append(agent)

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
            agent.dispose()
            self.agents.remove(agent)

        self.removedAgentQueue.clear()

        # If there are no agents, pause the game
        if len(self.agents) == 0:
            print("No agents remaining. Pausing game.")
            self.running = False
            return

        print("Continuing game with " + str(len(self.agents)) + " agents.")

        # Increment the time step
        self.timeStep += 1
        self.running = True

        # Create a state message for the current time step
        state = StateMessage(self.timeStep, self.agents)

        # Send the next time step state to all agents
        for agent in self.agents:
            agent.channel.SendState(state)

        # Create the next time step
        self.currentStep = GameTimeStep(self.timeStep, self.agents, self.store)

        # Subscribe to the complete observable
        completeObserver = self.currentStep.CompleteObservable.subscribe(
            on_completed=lambda: self.nextTimeStep()
        )
        # Add the complete observer to the composite disposable
        self.currentStep.compositeDisposable.add(completeObserver)
