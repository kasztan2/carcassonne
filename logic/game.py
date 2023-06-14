from typing import Sequence
from logic.tile import Tile
from logic.utils import Coords, parse_connection_number
from logic.player import Player
from logic.const import PLAYER_COLORS, FEATURE_TYPES
from logic.feature import Feature
from copy import copy
import random


class CarcassonneGame:
    def __init__(
        self, starting_tile: Tile, tileset: Sequence[Tile], players: Sequence[Player]
    ):
        self.tileset = copy(tileset)
        random.shuffle(self.tileset)
        self.players = copy(players)
        random.shuffle(self.players)
        self.turn = 0
        self.board = dict()
        self.board[Coords(0, 0)] = starting_tile

    @staticmethod
    def parseFeatureText(feature: str) -> Feature:
        def parseConnections(t: str):
            return [parse_connection_number(int(x)) for x in t.split(",")]

        if feature[0] == "M":
            return Feature(FEATURE_TYPES.CLOISTER, [])
        elif feature[0] == "F":
            return Feature(FEATURE_TYPES.FARM, parseConnections(feature[1:]))
        elif feature[0] == "C":
            return Feature(FEATURE_TYPES.CITY, parseConnections(feature[1:]))
        elif feature[0] == "P":
            return Feature(FEATURE_TYPES.PENNANT_CITY, parseConnections(feature[1:]))
        elif feature[0] == "R":
            return Feature(FEATURE_TYPES.ROAD, parseConnections(feature[1:]))
        else:
            raise Exception("Unknown feature type")

    @classmethod
    def from_file_and_names(cls, filename: str, playerNames: Sequence[str]):
        tileset = []
        startingTile = None

        f = open(filename, "r")
        s_tile = False
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                continue

            s_tile = False

            arr = line.split(" ")
            if arr[0] == "S":
                s_tile = True
                arr = arr[1:]

            n = int(arr[0])

            features = []
            for feature in arr[1:]:
                features.append(CarcassonneGame.parseFeatureText(feature))

            tile = Tile(None, features)

            for feature in tile.features:
                feature.parentTile = tile

            if s_tile:
                startingTile = copy(tile)
                n -= 1

            for i in range(n):
                tileset.append(copy(tile))

            tileset[-1].ensureCorrect()

        f.close()

        players = []
        colors = copy(PLAYER_COLORS)
        for name in playerNames:
            players.append(Player(name, colors.pop()))

        obj = cls(startingTile, tileset, players)

        for tile in tileset:
            tile.game = obj

        return obj
