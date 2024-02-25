from reactivex import Observer

from Server.Store.Store import Store

OUTPUT_DIRECTORY = "Output"


class ItemObserver(Observer):
    def __init__(self, itemId: str, startTime: int, store: Store):
        super().__init__()

        self.itemId = itemId
        self.startTime = startTime

        self.filePath = f"{OUTPUT_DIRECTORY}/{itemId}.csv"

        # Add the first line "time, x, y"
        self.writeLine("time, x, y")

        # Save the store layout for calculating statistics later
        self.store = store

        print("item observer created")

    def writeLine(self, text: str):
        with open(self.filePath, "a") as file:
            file.write(text + "\n")

    def on_next(self, value):
        print(f"Item {self.itemId} at position {value}")
        # Write the time and position to the file
        self.writeLine(f"{self.startTime}, {value[0]}, {value[1]}")
        # Increment the time
        self.startTime += 1
