import json

from PodSixNet.Channel import Channel
from reactivex import Subject, Observable
from reactivex.disposable import CompositeDisposable

from Agent.IAgentChannel import IAgentChannel
from Core.ISerializable import ISerializable
from Network.InitMessage import InitMessage
from Network.PreviewMessage import PreviewMessage
from Network.StateMessage import StateMessage
from Store.Store import Store


class AgentChannel(Channel, IAgentChannel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.isClosed = False
        self.compositeDisposable = CompositeDisposable()

        self.loginSubject = Subject()
        self.selectSubject = Subject()
        self.commitSubject = Subject()

        self.compositeDisposable.add(self.loginSubject)
        self.compositeDisposable.add(self.selectSubject)
        self.compositeDisposable.add(self.commitSubject)

    # Sending messages to the client
    def SendMessage(self, action: str, message: ISerializable):
        self.Send({"action": action, "data": json.dumps(message.toDict())})

    def SendInit(self, agentId: str, store: Store):
        message = InitMessage(agentId, store)
        self.SendMessage("init", message)

    def SendState(self, state: StateMessage):
        self.SendMessage("state", state)

    def SendPreview(self, preview: PreviewMessage):
        self.SendMessage("preview", preview)

    # Observables
    @property
    def LoginObservable(self) -> Observable:
        return self.loginSubject

    @property
    def SelectObservable(self) -> Observable:
        return self.selectSubject

    @property
    def CommitObservable(self) -> Observable:
        return self.commitSubject

    # Network specific callbacks
    def Network_init(self, data):
        self.loginSubject.on_next(data["type"])

    def Network_select(self, data):
        self.selectSubject.on_next(data["position"])

    def Network_commit(self, data):
        self.commitSubject.on_next(None)

    # Callback when the channel is closed
    def Close(self):
        if self.isClosed:
            return
        self.isClosed = True

        # Complete the login subject
        self.loginSubject.on_completed()
        # Dispose all subjects
        self.compositeDisposable.dispose()

    # Force closing the channel
    def Kick(self):
        self.handle_close()
