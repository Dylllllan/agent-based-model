import random

from Heuristic.CheckoutHeuristic import CheckoutHeuristic
from Heuristic.DistanceFromSelfHeuristic import DistanceFromSelfHeuristic
from Heuristic.ExitStoreHeuristic import ExitStoreHeuristic
from Heuristic.GetNearbyItemHeuristic import GetNearbyItemHeuristic
from Heuristic.GetRandomItemHeuristic import GetRandomItemHeuristic
from Heuristic.GetSpontaneousNearbyItemHeuristic import GetSpontaneousNearbyItemHeuristic
from Heuristic.GetSpontaneousRandomItemHeuristic import GetSpontaneousRandomItemHeuristic
from Heuristic.WanderingHeuristic import WanderingHeuristic
from Store.Store import Store
from Utils import createListOfLists

MAXIMUM_SHOPPER_ITEMS = 10


class ShopperHeuristicFactory:

    @staticmethod
    def createRandomHeuristics(store: Store) -> list:
        heuristicSet = []

        # Shoppers pick a random collection of items, and can choose to wander around the store
        numberOfItems = 0

        while numberOfItems < MAXIMUM_SHOPPER_ITEMS:
            # Choose between picking a random item in the store or a nearby item
            # The likelihood of picking up nearby vs. random increases with number of items

            randomItemChance = 0.5 + (1 - (numberOfItems / MAXIMUM_SHOPPER_ITEMS)) * 0.5
            if random.random() < randomItemChance:
                heuristicSet.append(GetRandomItemHeuristic(store))
            else:
                # Pick a random distance to pick a nearby item
                heuristicSet.append(GetNearbyItemHeuristic(store, {
                    "distance": random.randint(1, 10)
                }))

            numberOfItems += 1

            # Decreasing chance of wandering before choosing the next item
            wanderingChance = 0.3 + (1 - (numberOfItems / MAXIMUM_SHOPPER_ITEMS)) * 0.2
            if random.random() < wanderingChance:
                wanderingHeuristics = []

                # Choice between wandering nearby or to a random point in the store
                if random.random() < (numberOfItems / MAXIMUM_SHOPPER_ITEMS):
                    wanderingHeuristics.append(DistanceFromSelfHeuristic(store, {
                        "distance": random.randint(1, 10)
                    }))
                else:
                    wanderingHeuristics.append(WanderingHeuristic(store))

                # Random chance of being able to spontaneously pick up an item
                if random.random() < 0.1 and numberOfItems < MAXIMUM_SHOPPER_ITEMS - 1:
                    # Choose between picking a random item in the store or a nearby item
                    if random.random() < (numberOfItems / MAXIMUM_SHOPPER_ITEMS):
                        wanderingHeuristics.append(GetSpontaneousRandomItemHeuristic(store, {
                            "probability": 0.01 + random.random() * 0.01
                        }))
                    else:
                        wanderingHeuristics.append(GetSpontaneousNearbyItemHeuristic(store, {
                            "distance": random.randint(1, 10),
                            "probability": 0.01 + random.random() * 0.01
                        }))

                    # This means there is the potential for another item to be picked up while wandering
                    numberOfItems += 1

                heuristicSet.append(wanderingHeuristics)

            # Increasing random chance of being done shopping
            if random.random() < (numberOfItems / MAXIMUM_SHOPPER_ITEMS):
                break

        # 20% chance of wandering a short distance before going to checkout
        if random.random() < 0.2:
            heuristicSet.append(DistanceFromSelfHeuristic(store, {
                "distance": random.randint(5, 10)
            }))

        # Go to the checkout
        heuristicSet.append(CheckoutHeuristic(store))

        # 10% chance of choosing to wander a small distance before exiting the store
        if random.random() < 0.1:
            heuristicSet.append(DistanceFromSelfHeuristic(store, {
                "distance": random.randint(1, 3)
            }))

        # Exit the store
        heuristicSet.append(ExitStoreHeuristic(store))

        # Make sure the heuristic set is a list of lists
        return createListOfLists(heuristicSet)
