import pygame as pg

# Creating a surface for displaying the board
def make_surface(tile_size: int, surface_size_x: int, surface_size_y: int) -> pg.Surface:
    surf = pg.Surface((surface_size_x * tile_size, surface_size_y * tile_size))
    # Create each tile
    for x in range(surface_size_x):
        for y in range(surface_size_y):
            square = pg.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            pg.draw.rect(surf, pg.Color('#F3F9EF'), square)
    return surf


# Displaying the items over the surface
def display_items(screen, tile_size: int, surface_pos: tuple,
                  game_map: [list], player_positions: [tuple]):
    # Retrieving the positions of each item to display
    items_to_display = [(game_map[x][y], x, y) for x in range(len(game_map))
                        for y in range(len(game_map[0])) if game_map[x][y] is not None]
    items_to_display.extend([(('player', i), x, y) for i, (x, y) in enumerate(player_positions)])
    for item, x, y in items_to_display:
        if item == 'W':
            image_path = 'Assets/wall.png'
        elif item[0] == 'player':
            image_path = f'Assets/player{item[1] + 1}.png'
        else:
            image_path = 'Assets/milk.png'
        image = pg.image.load(image_path)
        square = pg.Rect(surface_pos[0] + y * tile_size + 1, surface_pos[1] + x * tile_size + 1,
                         tile_size, tile_size)
        screen.blit(image, image.get_rect(center=square.center))
