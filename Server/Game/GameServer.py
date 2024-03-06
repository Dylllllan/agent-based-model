from time import sleep

from PodSixNet.Server import Server

from Agent.AgentChannel import AgentChannel
from Agent.AgentType import AgentType
from Agent.IAgentChannel import IAgentChannel
from Game.Game import Game


class GameServer(Server):
    channelClass = AgentChannel

    def __init__(self, game: Game, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)

        self.channelObservables = {}
        self.agentChannels = {}

        self.game = game
        print("Server launched")

    def Connected(self, channel: IAgentChannel, address):
        print("Channel connected")
        channel.LoginObservable.subscribe(
            on_next=lambda agentType: self.addChannel(address, channel, agentType),
            on_completed=lambda: self.removeChannel(address),
        )
        self.channelObservables[address] = channel.LoginObservable

    def addChannel(self, address: tuple, channel: IAgentChannel, agentType: AgentType):
        print("Channel added")
        agent = self.game.addAgent(channel, agentType)
        self.agentChannels[address] = agent

    def removeChannel(self, address: tuple):
        if address in self.agentChannels:
            self.game.removeAgent(self.agentChannels[address])
            del self.agentChannels[address]

        if address in self.channelObservables:
            self.channelObservables[address].dispose()
            del self.channelObservables[address]

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)
