import uuid

from reactivex import Observer
from reactivex.abc import DisposableBase
from reactivex.disposable import CompositeDisposable
from reactivex.subject import BehaviorSubject

from Server.Store.ItemState import ItemState


class Item(DisposableBase):
    def __init__(self, itemState: ItemState, position: tuple):
        self.id = str(uuid.uuid4())
        self.compositeDisposable = CompositeDisposable()

        self.name = itemState.name
        self.price = itemState.price

        self.position = position
        self.positionSubject = BehaviorSubject(self.position)

    def addPositionObserver(self, observer: Observer):
        positionObserver = self.positionSubject.subscribe(observer)
        self.compositeDisposable.add(positionObserver)

    def setPosition(self, position: tuple):
        self.position = position
        self.positionSubject.on_next(position)

    def toItemState(self) -> ItemState:
        return ItemState(self.name, self.price)

    def dispose(self):
        self.compositeDisposable.dispose()
