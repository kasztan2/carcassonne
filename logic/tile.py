from logic.feature import Feature
from typing import TYPE_CHECKING, Sequence
import uuid

if TYPE_CHECKING:
    from logic.game import CarcassonneGame
    from logic.feature import Connection


class Tile(object):
    def __init__(self, game: "CarcassonneGame", features: Sequence[Feature]) -> None:
        self.game = game
        self.features = features
        self.uuid = uuid.uuid4()
        self.coords = None

    def rotate(self, times: int) -> None:
        for feature in self.features:
            feature.rotate(times)

    def ensureCorrect(self) -> None:
        conns = set()
        for feature in self.features:
            feature.parent_tile = self
            for conn in feature.connections:
                if conn in conns:
                    raise AssertionError("Duplicate connection in a tile")
                conns.add(conn)

        if len(conns) != 12:
            raise AssertionError("A tile must have exactly 12 connections")

    def placeMeeple(self, ind, player):
        player.minusMeeple()
        self.features[ind].meeple = player

    def get_feature_by_connection(self, connection: "Connection") -> Feature:
        for feature in self.features:
            if connection in feature.connections:
                return feature

    def __repr__(self):
        return f"Tile[{';'.join([x.__repr__() for x in self.features])}]"

    def __eq__(self, other):
        return self.uuid == other.uuid

    def __hash__(self):
        # a really bad practice here
        return 0  # hash(self.features)
