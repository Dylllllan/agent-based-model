import random

from Agent.AgentState import AgentState
from Heuristic.NavigationHeuristic import NavigationHeuristic
from Store.Store import Store


# Navigate to a random checkout and pay for the items
class CheckoutHeuristic(NavigationHeuristic):
    def __init__(self, store: Store):
        super().__init__(store)

        self.store.MapObservable.subscribe(lambda _: self.chooseCheckout())

    def chooseCheckout(self):
        # Choose a random checkout
        self.setDestination(random.choice(self.store.getCheckouts()).position)

    def evaluate(self, state: AgentState) -> float:
        # If the agent is at the checkout, return 0
        if state.paid:
            return 0.0
        else:
            return super().evaluate(state)
