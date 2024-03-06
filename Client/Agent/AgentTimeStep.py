import random

from reactivex import from_iterable, zip
from reactivex.disposable import CompositeDisposable
from reactivex.operators import min_by

from Agent.AgentState import AgentState
from Agent.IAgent import IAgent
from Agent.IAgentClient import IAgentClient
from Store.Store import Store


class AgentTimeStep:
    def __init__(self, agentId: str, store: Store, client: IAgentClient, agent: IAgent):
        self.agent = agent
        self.client = client

        self.store = store
        self.currentState = self.store.getAgent(agentId)

        directions = self.store.getDirectionsFromPosition(self.currentState.position)
        self.directions = iter(directions)

        self.compositeDisposable = CompositeDisposable()

        # Combine the directions with the resulting preview from the server
        zipObservable = zip(from_iterable(directions), self.client.PreviewObservable)

        # Get the next preview when the server sends a new preview
        zipObserver = zipObservable.subscribe(
            on_next=lambda _: self.getNextPreview(),
        )
        self.compositeDisposable.add(zipObserver)

        # Pipe the combined observable through an operator to find the direction with the lowest heuristic
        minOperator = min_by(lambda x: self.agent.evaluateHeuristics(AgentState(x[1])), lambda x, y: x - y)
        minObservable = zipObservable.pipe(minOperator)

        # When the combined observable completes, choose the best direction for the agent
        # If there is more than one, a direction will be chosen at random
        minObserver = minObservable.subscribe(
            on_next=lambda bestDirection: self.selectBestDirection(random.choice(bestDirection)[0])
        )
        self.compositeDisposable.add(minObserver)

        self.getNextPreview()

    def getNextPreview(self):
        try:
            direction = next(self.directions)
            position = self.getPosition(self.currentState.position, direction)
            self.client.sendSelect(position)
        except StopIteration:
            # No more directions to send
            pass

    def selectBestDirection(self, bestDirection: tuple):
        # Dispose of the observer subscriptions
        self.compositeDisposable.dispose()

        self.client.sendSelect(self.getPosition(self.currentState.position, bestDirection))
        # print("Selected tile: ", self.getPosition(self.currentState.position, bestDirection))

        self.client.sendCommit()

    @staticmethod
    def getPosition(position: tuple, direction: tuple) -> tuple:
        return position[0] + direction[0], position[1] + direction[1]
