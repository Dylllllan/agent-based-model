import socket

from PrototypeClientLogic import start_game

VERSION = "0.4"

HOST = 'localhost'
PORT = 8000


# Called to connect to the server
def connect():
    try:
        # Define the client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the client socket to the host and port
        client_socket.connect((HOST, PORT))

        print(f"Connected to host {HOST} on port {PORT}")
        return client_socket

    except OSError as e:
        if e.errno == socket.errno.EADDRINUSE:
            print(f"Port {PORT} is already in use")
        else:
            print(f"Error while trying to bind to port {PORT}: {e}")
        return -1


def main():
    sock = connect()
    start_game(sock)
    if sock != -1:
        sock.close()


if __name__ == '__main__':
    main()
