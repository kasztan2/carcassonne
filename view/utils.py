import numpy as np


# mouse position to coords
def alignMousePosition(mousePosition, screenSize, tileSize) -> tuple[int, int]:
    """Convert the mouse position to coordinates of a tile on board"""
    coords = [mousePosition[0], mousePosition[1]]
    coords[0] -= screenSize[0] / 2 - tileSize / 2
    coords[1] -= screenSize[1] / 2 - tileSize / 2
    coords[0] //= tileSize
    coords[1] //= tileSize
    return (int(coords[0]), int(coords[1]))


def deCornify(pos: tuple[float, float], tilesize: int) -> tuple[float, float]:
    """In fact: deEgify. Used to move a meeple away from the edge of a tile (to be visible as a whole)"""
    middle = (tilesize / 2, tilesize / 2)
    if pos[0] == 0 or pos[0] == tilesize or pos[1] == 0 or pos[1] == tilesize:
        return tuple(np.average([pos, middle], weights=[0.8, 0.2], axis=0))

    return pos
