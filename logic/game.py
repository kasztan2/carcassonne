from typing import Sequence
from logic.tile import Tile
from logic.utils import Coords, parse_connection_number, invert_side, get_side_conn_list
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

        self.boardCallback = None

    def get_current_player_name(self):
        return self.players[self.turn].name

    def get_current_tile(self):
        return self.tileset[-1]

    def place_tile(self, coords: Coords | tuple[int, int]):
        if len(self.tileset) == 0:
            raise ValueError("No tiles left")

        if isinstance(coords, tuple):
            coords = Coords(coords[0], coords[1])
        tile = self.get_current_tile()
        sides = range(4)
        adjacent_tiles = coords.get_adjacent_coords()

        anyAdjacent = False
        for side in sides:
            if adjacent_tiles[side] in self.board.keys():
                anyAdjacent = True
                adjacent_tile = self.board[adjacent_tiles[side]]
                if (
                    get_side_conn_list(tile, side)
                    != get_side_conn_list(adjacent_tile, invert_side(side)).reverse()
                ):
                    return False

        if not anyAdjacent:
            return False

        self.board[coords] = tile
        self.tileset.pop()

        if self.boardCallback is not None:
            self.boardCallback(tile, coords)

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
