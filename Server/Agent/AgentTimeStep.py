from reactivex import Observable
from reactivex.abc import DisposableBase
from reactivex.disposable import CompositeDisposable
from reactivex.subject import BehaviorSubject

from Action.Action import Action
from Agent.Agent import Agent
from Network.PreviewMessage import PreviewMessage


class AgentTimeStep(DisposableBase):
    def __init__(self, agent: Agent):
        self.compositeDisposable = CompositeDisposable()

        self.agent = agent
        self.channel = self.agent.channel
        self.action = None

        self.selectSubject = BehaviorSubject(None)
        self.compositeDisposable.add(self.selectSubject)

        selectObserver = self.channel.SelectObservable.subscribe(
            on_next=lambda tile: self.selectSubject.on_next(tile)
        )
        self.compositeDisposable.add(selectObserver)

        commitObserver = self.channel.CommitObservable.subscribe(
            on_next=lambda _: self.selectSubject.on_completed()
        )
        self.compositeDisposable.add(commitObserver)

        # Handle an agent disconnecting during the time step
        loginObserver = self.channel.LoginObservable.subscribe(
            on_completed=lambda: self.selectSubject.on_completed()
        )
        self.compositeDisposable.add(loginObserver)

    def previewAction(self, action: Action):
        # Save the action
        self.action = action

        # Send a preview of the agent state after the action
        agentState = self.agent.toAgentState()

        if self.action is not None:
            self.action.DoAction(agentState)

        self.channel.SendPreview(PreviewMessage(agentState))

    def commitAction(self):
        if self.action is None:
            # No action to commit
            return

        # Commit the action to the agent
        self.action.DoAction(self.agent)

    @property
    def SelectObservable(self) -> Observable:
        return self.selectSubject

    def dispose(self):
        self.compositeDisposable.dispose()
