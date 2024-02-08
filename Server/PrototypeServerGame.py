import socket
from pickle import dumps, loads

VERSION = "0.4"

OUTPUT = "out/out1.txt"


# Sending serialised data using pickle to the client
def send_data(sock: socket.socket, data) -> None: sock.send(dumps(data))


# Receiving data from client
def receive_data(sock: socket.socket): return loads(sock.recv(1024))


class Game:
    def __init__(self, game_map: str, number_players: int):
        self.game_map = self.build_map(game_map)  # Sets up the initial state of the map from a file
        self.number_players = number_players  # Starts at 1, not 0
        self.players = [Player(i + 1, self.game_map) for i in range(number_players)]
        for i, player in enumerate(self.players):
            player.set_position(self.initial_player_positions[i])

    def get_player_positions(self): return [player.get_position() for player in self.players]

    # Returns the map as a 2D matrix
    # Players are not present in the map, because several could be on the same square
    def build_map(self, config: str) -> [list]:
        # Opening and reading map file
        with open(config, 'r') as f:
            game_map_data = f.readlines()
        # Creating a 2D matrix with rows and columns filled with None as specified in map file
        n_rows, n_cols = game_map_data[0].replace('\n', '').split()
        game_map = [[None] * int(n_cols) for _ in range(int(n_rows))]

        # Retrieving wall positions in format x,y
        for wall_pos in game_map_data[1].replace('\n', '').split():
            wall_pos = wall_pos.split(',')
            game_map[int(wall_pos[0])][int(wall_pos[1])] = 'W'

        # Retrieving shelf data in format x,y,item,item_price,capacity
        self.shelves = []
        for shelf_data in game_map_data[2].replace('\n', '').split():
            d = shelf_data.split(',')
            shelf = Shelf((int(d[0]), int(d[1])), d[2], float(d[3]), int(d[4]))
            game_map[int(d[0])][int(d[1])] = str(shelf)
            self.shelves.append(shelf)

        # Retrieving initial position for each player
        self.initial_player_positions = [tuple(map(int, pos.split(',')))
                                         for pos in game_map_data[3].split()]

        return game_map

    # Called only once, the game lasts for the whole duration of this method
    def start(self):
        self.played_moves = [None] * self.number_players
        self.game_over = False

        # Writing each player's move at each time step in an external file
        with open(OUTPUT, 'w') as f:
            while self.game_over is False:
                if 'stop' in self.played_moves:
                    self.game_over = True
                elif None not in self.played_moves:
                    f.write(' '.join([move for move in self.played_moves]) + '\n')
                    self.update_game()
                    self.played_moves = [None] * self.number_players

    def update_game(self):
        for move, player in zip(self.played_moves, self.players):
            if move == 'pick':
                player.add_item(player.neighbour_shelf.pick(1))  # Only 1 item at a time for now
            # Moving the character
            else:
                x, y = player.get_position()
                directions = {'left': (x, y - 1), 'up': (x - 1, y),
                              'right': (x, y + 1), 'down': (x + 1, y)}
                player.set_position(directions[move])

    # Method called by each client thread to handle server-client communication
    def play(self, player_number: int, sock):
        player = self.players[player_number - 1]
        # Send initial game state to client
        send_data(sock, (self.game_map, player_number,
                         player.compute_legal_moves(self.shelves), self.get_player_positions()))
        # Prevent receiving data from being a blocking call, allows player to change their mind
        # while waiting for the other players to make their move
        sock.setblocking(False)
        sent = True  # Used to track whether legal moves have already been sent or not
        while self.game_over is False:
            try:
                if self.played_moves[player_number - 1] is None and sent is False:
                    send_data(sock, (player.compute_legal_moves(self.shelves),
                                     self.get_player_positions()))
                    sent = True
                data = receive_data(sock)
                sent = False
                self.played_moves[player_number - 1] = data

            # No data available to read
            except (BlockingIOError, EOFError):
                pass


class Shelf:
    def __init__(self, position: tuple, item: str, item_price: float, capacity: int):
        self.position = position
        self.item = item
        self.item_price = item_price
        self.capacity = capacity

    def __str__(self): return "EMPTY" if self.capacity == 0 else self.item  # str interpretation

    def pick(self, n: int) -> str:
        self.capacity -= n
        return self.item


class Player:
    def __init__(self, player_number, game_map):
        self.player_number = player_number
        self.game_map = game_map
        self.items = {}

    def set_position(self, position: tuple): self.position = position

    def get_position(self) -> tuple: return self.position

    def add_item(self, item: str):
        if item in self.items:
            self.items[item] += 1
        else:
            self.items[item] = 1
        print(f"Player {self.player_number} has {self.get_items()}")

    def get_items(self) -> dict: return self.items

    def compute_legal_moves(self, shelves: list) -> list:
        x, y = self.get_position()
        self.neighbour_shelf = None

        directions = [('left', (0, -1)), ('up', (-1, 0)), ('right', (0, 1)), ('down', (1, 0))]
        legal_moves = []

        for direction, (dx, dy) in directions:
            new_x, new_y = x + dx, y + dy

            # Check if the move would send the player out of the map
            if 0 <= new_x < len(self.game_map) and 0 <= new_y < len(self.game_map[0]):
                neighbour = self.game_map[new_x][new_y]

                if neighbour is None:
                    legal_moves.append(direction)
                else:
                    for shelf in shelves:
                        if shelf.position == (new_x, new_y):
                            legal_moves.append('pick')
                            self.neighbour_shelf = shelf
                            break  # Players can be next to only one shelf at a given time step

        return legal_moves
