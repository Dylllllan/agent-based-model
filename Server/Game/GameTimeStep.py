from reactivex import Subject, fork_join
from reactivex.abc import DisposableBase
from reactivex.disposable import CompositeDisposable

from Agent.AgentTimeStep import AgentTimeStep
from Store.Store import Store


class GameTimeStep(DisposableBase):
    def __init__(self, timeStep: int, agents: list, store: Store):
        self.compositeDisposable = CompositeDisposable()

        self.completeSubject = Subject()
        self.compositeDisposable.add(self.completeSubject)

        self.timeStep = timeStep
        self.agentTimeSteps = list(AgentTimeStep(a) for a in agents)
        self.store = store

        # Add the agent time steps to the composite disposable
        for agentTimeStep in self.agentTimeSteps:
            self.compositeDisposable.add(agentTimeStep)

        # For each agent time step, subscribe to the select observable
        for agentTimeStep in self.agentTimeSteps:
            selectObserver = agentTimeStep.SelectObservable.subscribe(
                on_next=lambda position, ats=agentTimeStep: self.onSelectTile(position, ats),
            )
            self.compositeDisposable.add(selectObserver)

        # Fork join all the select observables and wait for all to complete
        commitObserver = fork_join(
            *[agentTimeStep.SelectObservable for agentTimeStep in self.agentTimeSteps]).subscribe(
            on_completed=lambda: self.onAllCommit()
        )
        self.compositeDisposable.add(commitObserver)

    def onSelectTile(self, position: tuple, agentTimeStep: AgentTimeStep):
        if position is None:
            return

        tile = self.store.getTile(position)
        agentTimeStep.previewAction(tile.getAction())

    def onAllCommit(self):
        for agentTimeStep in self.agentTimeSteps:
            agentTimeStep.commitAction()
        self.completeSubject.on_completed()

    @property
    def CompleteObservable(self):
        return self.completeSubject

    def dispose(self):
        self.compositeDisposable.dispose()
