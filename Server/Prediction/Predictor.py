import asyncio

import requests

from Prediction.PredictionRequest import PredictionRequest

PREDICTION_API_ROOT = "http://localhost:8080"


class Predictor:
    def __init__(self, agents: list, timeStep: int):
        self.agents = agents

        self.items = []
        for agent in self.agents:
            for item in agent.items:
                self.items.append(item)

        self.timeStep = timeStep

    async def predict(self):
        if len(self.items) == 0:
            print("No items to predict for")
            return

        # Create the prediction request
        predictionRequest = PredictionRequest(self.items, self.timeStep)

        # Send the prediction request using requests
        response = await asyncio.to_thread(requests.post, PREDICTION_API_ROOT + "/predict",
                                           data=None, json=predictionRequest.toDict())

        if not response.ok:
            print("Prediction request failed with status code", response.status_code)
            return

        print("Prediction request successful")

        predictionMap = response.json()

        # For each key in the prediction map
        for key in predictionMap:
            # Find the item with the corresponding ID
            item = next((item for item in self.items if item.id == key), None)
            if item is None:
                continue

            # Update the item's prediction based on the last entry in the array
            predictions = predictionMap[key]
            if len(predictions) == 0:
                continue

            item.setPrediction(predictions[-1])
