import random

from Heuristic.DistanceFromItemAbovePriceHeuristic import DistanceFromItemAbovePriceHeuristic
from Heuristic.DistanceFromPreviousTargetHeuristic import DistanceFromPreviousTargetHeuristic
from Heuristic.DistanceFromSelfHeuristic import DistanceFromSelfHeuristic
from Heuristic.ExitStoreHeuristic import ExitStoreHeuristic
from Heuristic.GetNearbyItemAbovePriceHeuristic import GetNearbyItemAbovePriceHeuristic
from Heuristic.GetSpontaneousNearbyItemHeuristic import GetSpontaneousNearbyItemHeuristic
from Heuristic.WanderingHeuristic import WanderingHeuristic
from Store.Store import Store
from Utils import createListOfLists

MAXIMUM_SHOPLIFTER_ITEMS = 5


class ShoplifterHeuristicFactory:
    @staticmethod
    def createRandomHeuristics(store: Store) -> list:
        heuristicSet = []

        # Shoppers pick a targeted collection of items, and can choose to wander around the store
        numberOfItems = 0

        while numberOfItems < MAXIMUM_SHOPLIFTER_ITEMS:
            # Choose a minimum price of item to target
            price = random.randint(300, 700)

            # Choose a number of approaches between 0 and 5
            approaches = random.randint(0, 5)

            distanceFromItemHeuristic = DistanceFromItemAbovePriceHeuristic(store, {
                "price": price,
                "distance": -1
            })

            for i in range(approaches):
                # Choose a random distance to get close to the item
                approachDistance = random.randint(1, 3) * -1
                heuristicSet.append(DistanceFromPreviousTargetHeuristic(store, {
                    "distance": approachDistance
                }, distanceFromItemHeuristic))

                backOffSet = []

                # Choose a random distance to back off from the item
                backOffDistance = random.randint(1, 5)

                if approachDistance == -1:
                    # Backoff from self position
                    backOffSet.append(DistanceFromSelfHeuristic(store, {
                        "distance": backOffDistance
                    }))
                else:
                    # Backoff from item position
                    backOffSet.append(DistanceFromPreviousTargetHeuristic(store, {
                        "distance": backOffDistance
                    }, distanceFromItemHeuristic))

                # 20% chance of picking up a nearby item spontaneously
                if random.random() < 0.2 and numberOfItems < MAXIMUM_SHOPLIFTER_ITEMS - 1:
                    spontaneousDistance = random.randint(1, 5)
                    backOffSet.append(GetSpontaneousNearbyItemHeuristic(store, {
                        "distance": spontaneousDistance,
                        "probability": 0.1
                    }))

                    numberOfItems += 1

                heuristicSet.append(backOffSet)

            # Go close to the targeted item
            heuristicSet.append(distanceFromItemHeuristic)
            # There should only be one item within distance for the shoplifter to pick up
            heuristicSet.append(GetNearbyItemAbovePriceHeuristic(store, {
                "price": price,
                "distance": 1
            }))

            numberOfItems += 1

            # Decreasing chance of wandering before choosing the next item
            wanderingChance = 0.2 + (1 - (numberOfItems / MAXIMUM_SHOPLIFTER_ITEMS)) * 0.3
            if random.random() < wanderingChance:
                # Choice between wandering nearby or to a random point in the store
                if random.random() < (numberOfItems / MAXIMUM_SHOPLIFTER_ITEMS):
                    heuristicSet.append(DistanceFromSelfHeuristic(store, {
                        "distance": random.randint(1, 10)
                    }))
                else:
                    heuristicSet.append(WanderingHeuristic(store))

            # Increasing random chance of being done shoplifting
            if random.random() < (numberOfItems / MAXIMUM_SHOPLIFTER_ITEMS):
                break

        # Exit the store
        heuristicSet.append(ExitStoreHeuristic(store))

        # Make sure the heuristic set is a list of lists
        return createListOfLists(heuristicSet)
