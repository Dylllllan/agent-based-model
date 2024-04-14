import uuid

from reactivex import Observer
from reactivex.abc import DisposableBase
from reactivex.disposable import CompositeDisposable
from reactivex.subject import BehaviorSubject

from Store.ItemState import ItemState


class Item(DisposableBase):
    def __init__(self, itemState: ItemState, position: tuple):
        self.id = str(uuid.uuid4())
        self.compositeDisposable = CompositeDisposable()

        self.name = itemState.name
        self.category = itemState.category
        self.price = itemState.price
        self.prediction = itemState.prediction

        self.position = position
        self.positionSubject = BehaviorSubject(self.position)

    def addPositionObserver(self, observer: Observer):
        positionObserver = self.positionSubject.subscribe(observer)
        self.compositeDisposable.add(positionObserver)

    def setPosition(self, position: tuple):
        self.position = position
        self.positionSubject.on_next(position)

    def setPrediction(self, prediction: float):
        self.prediction = prediction

    def toItemState(self) -> ItemState:
        return ItemState(self.name, self.category, self.price, self.prediction)

    def remove(self, validState: bool):
        if validState:
            self.positionSubject.on_completed()
        else:
            self.positionSubject.on_error(Exception("Item removed at an invalid location"))

    def dispose(self):
        self.compositeDisposable.dispose()
