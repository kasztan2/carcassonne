from logic.feature import Feature
from typing import Sequence


class Tile(object):
    def __init__(self, game: "CarcassonneGame", features: Sequence[Feature]) -> None:
        self.game = game
        self.features = features

    def rotate(self, times: int) -> None:
        for feature in self.features:
            feature.rotate(times)

    def ensureCorrect(self) -> None:
        conns = set()
        for feature in self.features:
            for conn in feature.connections:
                if conn in conns:
                    raise AssertionError("Duplicate connection in a tile")
                conns.add(conn)

        if len(conns) != 12:
            raise AssertionError("A tile must have exactly 12 connections")
