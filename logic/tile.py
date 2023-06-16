from logic.feature import Feature
from typing import Sequence
import uuid


class Tile(object):
    def __init__(
        self, game: "logic.CarcassonneGame", features: Sequence[Feature]
    ) -> None:
        self.game = game
        self.features = features
        self.uuid = uuid.uuid4()

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

    def __repr__(self):
        return f"Tile[{';'.join([x.__repr__() for x in self.features])}]"

    def __eq__(self, other):
        return self.uuid == other.uuid
