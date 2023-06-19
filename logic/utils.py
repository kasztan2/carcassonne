from logic.const import *
from logic.feature import Connection
from typing import TYPE_CHECKING, Sequence
from itertools import product

if TYPE_CHECKING:
    from logic.feature import Feature


def invert_side(side: int) -> int:
    return (side + 2) % 4


def get_side_conn_list(tile, side) -> list:
    output = {}
    for feature in tile.features:
        for conn in feature.connections:
            if conn.side == side:
                output[conn.number] = feature.type
    return [output[0], output[1], output[2]]


def parse_connection_number(connection_number: int) -> Connection:
    return Connection(connection_number // 3, connection_number % 3)


def is_nearby_connection(conn1, conn2) -> bool:
    n1 = conn1.to_number()
    n2 = conn2.to_number()
    return abs(n1 - n2) == 1 or set([n1, n2]) == set([0, 12])


def is_nearby_feature(f1: "Feature", f2: "Feature") -> bool:
    conns1 = f1.connections
    conns2 = f2.connections
    for conn1, conn2 in product(conns1, conns2):
        if is_nearby_connection(conn1, conn2):
            return True

    return False


class Coords(object):
    """Class to manage coordinates on a board"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_adjacent_coords(self) -> Sequence["Coords"]:
        """Returns a list of adjacent coords (without itself)"""
        return [
            Coords(self.x + x, self.y + y)
            for x, y in [(-1, 0), (0, -1), (1, 0), (0, 1)]
        ]

    def get_coords_around(self) -> Sequence["Coords"]:
        """Returns a list of coords around and itself (to manage cloisters)"""
        return [
            (Coords(self.x + x, self.y + y) for x, y in product([-1, 0, 1], repeat=2))
        ]

    def to_tuple(self) -> tuple:
        return (self.x, self.y)

    def __eq__(self, __value: object) -> bool:
        return self.x == __value.x and self.y == __value.y

    def __repr__(self):
        return f"Coords({self.x}, {self.y})"

    def __hash__(self) -> int:
        return self.x * 1000 + self.y
