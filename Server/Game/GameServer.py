from time import sleep

from PodSixNet.Server import Server

from Server.Agent.AgentChannel import AgentChannel
from Server.Agent.AgentType import AgentType
from Server.Agent.IAgentChannel import IAgentChannel
from Server.Game.Game import Game


class GameServer(Server):
    channelClass = AgentChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)

        self.channelObservables = {}
        self.agentChannels = {}

        self.game = Game()
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
        agent = self.agentChannels[address]
        self.game.removeAgent(agent)
        del self.agentChannels[address]

        self.channelObservables[address].dispose()
        del self.channelObservables[address]

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)
