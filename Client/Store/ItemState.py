class ItemState:
    def __init__(self, data: dict):
        self.name = data["name"]
        self.category = data["category"]
        self.price = data["price"]
        self.prediction = data["prediction"]
