from logic.const import *
from logic.feature import Connection
from typing import Sequence
from itertools import product


def invert_side(side: int) -> int:
    return (side + 2) % 4


def parse_connection_number(connection_number: int) -> Connection:
    return Connection(connection_number // 3 + 1, connection_number % 3)


class Coords(object):
    """Class to manage coordinates on a board"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_adjacent_coords(self) -> Sequence["Coords"]:
        """Returns a list of adjacent coords (without itself)"""
        return [
            Coords(self.x + x, self.y + y)
            for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        ]

    def get_coords_around(self) -> Sequence["Coords"]:
        """Returns a list of coords around and itself (to manage cloisters)"""
        return [
            (Coords(self.x + x, self.y + y) for x, y in product([-1, 0, 1], repeat=2))
        ]
