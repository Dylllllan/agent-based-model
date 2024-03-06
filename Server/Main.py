import sys

from Game.Game import Game
from Game.GameServer import GameServer

HOST = "localhost"
PORT = 8000

if __name__ == '__main__':
    arguments = sys.argv[1:]

    # Configuration file path passed in as an argument
    game = Game(arguments[0])

    # Launch the game server
    GameServer(game, localaddr=(HOST, PORT)).Launch()
