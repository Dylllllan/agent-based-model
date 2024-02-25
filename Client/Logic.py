import pygame as pg

from Graphics import make_surface, display_items

# AZERTY
CONTROLS = {'left': (pg.K_LEFT, pg.K_a), 'up': (pg.K_UP, pg.K_z),
            'right': (pg.K_RIGHT, pg.K_e), 'down': (pg.K_DOWN, pg.K_s)}
# QWERTY
# CONTROLS = {'left': (pg.K_LEFT, pg.K_a), 'up': (pg.K_UP, pg.K_w),
#             'right': (pg.K_RIGHT, pg.K_d), 'down': (pg.K_DOWN, pg.K_s)}


# Main function to handle a game
def start_game():
    pg.init()

    # Initial message from server to set up the game
    game_map, player_number, legal_moves, player_positions = receive_data(sock)
    # Declaring tile size and surface position
    tile_size = 48
    surface_size_x, surface_size_y = len(game_map), len(game_map[0])
    surface_pos = (10, 10)

    screen = pg.display.set_mode((surface_size_y * tile_size + 20, surface_size_x * tile_size + 20))
    pg.display.set_caption(f"ABM - Player {player_number}")
    pg.display.set_icon(pg.image.load('Assets/logo.png'))
    surf = make_surface(tile_size, surface_size_y, surface_size_x)
    clock = pg.time.Clock()

    # Called when the server indicates that the game is over
    def game_over():
        send_data(sock, "stop")
        pg.quit()
        sock.setblocking(True)

    # Set the socket to non-blocking mode for the user to be able to send instructions to server
    # while waiting for other players' moves
    sock.setblocking(False)

    # Main game loop
    while True:
        # Waiting for opponent's move
        try:
            # If no data is available, the rest of the loop runs since the socket is non-blocking
            result = receive_data(sock)
            if result == 'stop':
                game_over()
                return
            elif result is not None:
                legal_moves, player_positions = result

        # No data available to read, continue loop
        except BlockingIOError:
            pass

        # Event handling
        events = pg.event.get()
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE and 'pick' in legal_moves:
                    send_data(sock, 'pick')
                else:
                    for move in legal_moves:
                        if move != 'pick' and e.key in CONTROLS[move]:
                            send_data(sock, move)

            # Quitting by clicking on cross
            if e.type == pg.QUIT:
                game_over()
                return

        # Displaying the surface and items
        screen.fill(pg.Color('light grey'))
        screen.blit(surf, surface_pos)
        display_items(screen, tile_size, surface_pos, game_map, player_positions)

        pg.display.flip()
        clock.tick(60)
