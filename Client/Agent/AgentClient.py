import json

from PodSixNet.Connection import ConnectionListener, connection
from reactivex import Subject, Observable
from reactivex.abc import DisposableBase
from reactivex.disposable import CompositeDisposable
from reactivex.subject import ReplaySubject

from Client.Agent.AgentType import AgentType
from Client.Agent.IAgentClient import IAgentClient


class AgentClient(ConnectionListener, DisposableBase, IAgentClient):
    def __init__(self, host, port, tickSubject: Subject):
        self.Connect((host, port))
        self.compositeDisposable = CompositeDisposable()

        self.connectionSubject = Subject()
        self.compositeDisposable.add(self.connectionSubject)

        self.agentIdSubject = ReplaySubject(1)
        self.compositeDisposable.add(self.agentIdSubject)

        self.storeSubject = ReplaySubject(1)
        self.compositeDisposable.add(self.storeSubject)

        self.stateSubject = Subject()
        self.compositeDisposable.add(self.stateSubject)

        self.previewSubject = Subject()
        self.compositeDisposable.add(self.previewSubject)

        tickObserver = tickSubject.subscribe(on_next=lambda _: self.Pump())
        self.compositeDisposable.add(tickObserver)

    # Observables
    @property
    def ConnectionObservable(self) -> Observable:
        return self.connectionSubject

    @property
    def AgentIdObservable(self) -> Observable:
        return self.agentIdSubject

    @property
    def StoreObservable(self) -> Observable:
        return self.storeSubject

    @property
    def StateObservable(self) -> Observable:
        return self.stateSubject

    @property
    def PreviewObservable(self) -> Observable:
        return self.previewSubject

    # Client to server actions
    def sendInit(self, agentType: AgentType):
        self.Send({"action": "init", "type": agentType.value})

    def sendSelect(self, position: tuple):
        self.Send({"action": "select", "position": position})

    def sendCommit(self):
        self.Send({"action": "commit"})

    # Network specific callbacks
    def Network_init(self, data):
        # print("Map data: ", data["data"])

        data = json.loads(data["data"])
        self.agentIdSubject.on_next(data["agentId"])
        self.storeSubject.on_next(data["store"])

    def Network_state(self, data):
        # print("State data: ", data["data"])

        data = json.loads(data["data"])
        self.stateSubject.on_next(data)

    def Network_preview(self, data):
        # print("Preview data: ", data["data"])

        data = json.loads(data["data"])["agentState"]
        self.previewSubject.on_next(data)

    # Built-in network events
    def Network_connected(self, data):
        print("Connected to server")
        self.connectionSubject.on_next(None)

    def Network_error(self, data):
        print("Network error:", data["error"][1])
        connection.Close()
        self.dispose()

    def Network_disconnected(self, data):
        print("Disconnected from server")
        self.connectionSubject.on_completed()
        self.dispose()

    def Close(self):
        connection.Close()

    def Pump(self):
        connection.Pump()
        # Call the method on the super class
        super().Pump()

    def dispose(self):
        self.compositeDisposable.dispose()
        exit()
