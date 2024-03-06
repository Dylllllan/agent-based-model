import os

from reactivex import Observer

from Store.Item import Item
from Store.Store import Store

OUTPUT_DIRECTORY = "Output"
# If the directory does not exist, create it
if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

# If the CLEAR_OUTPUT environment variable is set, clear the directory
if os.environ.get("CLEAR_OUTPUT"):
    print("Clearing output directory")
    for file in os.listdir(OUTPUT_DIRECTORY):
        os.remove(f"{OUTPUT_DIRECTORY}/{file}")


class ItemObserver(Observer):
    def __init__(self, item: Item, startTime: int, store: Store, shoplifter: bool = False):
        super().__init__()

        self.item = item
        self.currentTime = startTime

        self.filePath = f"{OUTPUT_DIRECTORY}/{item.category}_{item.id}.csv"

        # Add item information to the file
        self.writeLine("name, category, price, shoplifter")
        self.writeLine(f"\"{item.name}\", \"{item.category}\", {item.price}, {shoplifter}")

        # Add a divider line
        self.writeLine("---")

        # Add a header line for time steps and positions
        self.writeLine("time, x, y")

        # Save the store layout for calculating statistics later
        self.store = store

    def writeLine(self, text: str):
        with open(self.filePath, "a") as file:
            file.write(text + "\n")

    def on_next(self, value):
        print(f"Item {self.item.id} at position {value}")
        # Write the time and position to the file
        self.writeLine(f"{self.currentTime}, {value[0]}, {value[1]}")
        # Increment the time
        self.currentTime += 1

    def on_error(self, error):
        print(f"Error for item {self.item.id}: {error}")
        # Write a line "ERROR" to the file
        # Files with ERROR at the end should be removed from the training dataset
        self.writeLine("ERROR")

    def on_completed(self):
        # Write a line "COMPLETED" to the file
        self.writeLine("COMPLETED")
