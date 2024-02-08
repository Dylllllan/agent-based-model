import socket
from threading import Thread, Event

from PrototypeServerGame import Game, send_data

VERSION = "0.4"

HOST = 'localhost'
PORT = 8000

MAX_PLAYERS = 2
GAME_MAP = "game_maps/map1.txt"


# Main class, to handle client connections
class PrototypeServer:
    def __init__(self, max_players: int, game_map: str):
        self.game = None
        self.max_players = max_players
        self.game_map = game_map  # str: path to .txt file
        self.connected = []  # Currently connected clients (sockets)
        self.game_start_event = Event()  # Event triggered when a game starts

    def get_game(self): return self.game

    # Creates a Game object (defined in PrototypeServerGame) and launches the game
    def play_game(self):
        self.game = Game(self.game_map, self.max_players)
        # Let every client know the game is starting
        self.game_start_event.set()
        self.game.start()
        self.reset()

    # Called when a game is finished, allows the server to be ready for the next game
    def reset(self):
        self.game = None
        # Close connection with all clients
        for client in self.connected:
            send_data(client, "stop")
            client.close()
        self.game_start_event = Event()
        self.connected = []

    # Called by an individual client thread upon connecting with the server
    def handle_connection(self, s: socket.socket, player_number: int):
        # If no game is available, wait for one to start
        if self.get_game() is None:
            self.game_start_event.wait()
        # Each thread calls the .play() method of the Game class when the game starts
        self.get_game().play(player_number, s)

    # Listens for incoming connections and launches individual threads for each new user
    def start_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(self.max_players)  # Only accept enough players simultaneously to start a game
            print(f"Listening on port {PORT} on host {HOST}")
            while True:
                try:
                    # Accept incoming client connections
                    client_sock, client_add = s.accept()
                    # Add client socket to list of connected clients
                    self.connected.append(client_sock)
                    print(f"Currently connected: {len(self.connected)}")

                    # Create a new thread to handle the client connection
                    client_thread = Thread(target=self.handle_connection,
                                           args=(client_sock, len(self.connected)))
                    client_thread.start()

                    # Create a new game on a separate thread if enough clients are ready connected
                    if self.get_game() is None and len(self.connected) == self.max_players:
                        game_thread = Thread(target=self.play_game)
                        game_thread.start()

                except KeyboardInterrupt:
                    print("Server Shutting Down...")
                    break


def main():
    try:
        # Create a new server
        server = PrototypeServer(MAX_PLAYERS, GAME_MAP)
        server.start_listening()

    except OSError as e:
        if e.errno == socket.errno.EADDRINUSE:
            print(f"Port {PORT} is already in use")
        else:
            print(f"Error while trying to bind to port {PORT}: {e}")


if __name__ == '__main__':
    main()
