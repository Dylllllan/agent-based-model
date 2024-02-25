from Server.Game.GameServer import GameServer

HOST = "localhost"
PORT = 8000

if __name__ == '__main__':
    GameServer(localaddr=(HOST, PORT)).Launch()
