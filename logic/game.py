from typing import Sequence
from logic.tile import Tile
from logic.utils import Coords, parse_connection_number, invert_side, get_side_conn_list
from logic.player import Player
from logic.const import PLAYER_COLORS, FEATURE_TYPES
from logic.feature import Feature, Connection
from copy import copy, deepcopy
import random
from logic.scoring import Scorer
import traceback


class CarcassonneGame:
    def __init__(
        self, starting_tile: Tile, tileset: Sequence[Tile], players: Sequence[Player]
    ):
        random.seed(1)
        self.tileset = copy(tileset)
        random.shuffle(self.tileset)
        self.players = copy(players)
        random.shuffle(self.players)
        self.turn = 0
        self.board = dict()
        starting_tile.coords = Coords(0, 0)
        starting_tile.ensureCorrect()
        self.board[Coords(0, 0)] = starting_tile
        self.lastTile = None
        self.phase = 0
        self.scorer = Scorer(self)
        self.tilesChanged = set()

    def get_current_player_name(self):
        return self.players[self.turn].name

    def get_current_player_color(self):
        return self.players[self.turn].color

    def get_current_tile(self):
        print(f"Current tile: {self.tileset[-1]}")
        return self.tileset[-1]

    def is_finished(self):
        return len(self.tileset) == 0

    def get_winners(self):
        if not self.is_finished():
            raise Exception("Game has not finished yet")

        max_score = max([player.score for player in self.players])

        return [player for player in self.players if player.score == max_score]

    def place_tile(
        self, tile: Tile, coords: Coords | tuple[int, int] | list[int, int]
    ) -> None:
        if self.phase != 0:
            raise Exception("Can't place tile while placing a meeple")

        if len(self.tileset) == 0:
            raise ValueError("No tiles left")

        if isinstance(coords, tuple) or isinstance(coords, list):
            coords = Coords(coords[0], coords[1])

        if coords in self.board.keys():
            raise ValueError("Tile already there")

        tile = self.get_current_tile()
        sides = range(4)

        adjacent_tiles = coords.get_adjacent_coords()

        anyAdjacent = False
        for side in sides:
            if adjacent_tiles[side] in self.board.keys():
                anyAdjacent = True
                adjacent_tile = self.board[adjacent_tiles[side]]
                my_side = get_side_conn_list(tile, side)
                neighbor_side = list(
                    reversed(get_side_conn_list(adjacent_tile, invert_side(side)))
                )
                for conn in range(3):
                    if my_side[conn] == neighbor_side[conn] or set(
                        [my_side[conn], neighbor_side[conn]]
                    ) == set([1, 2]):
                        continue
                    raise Exception("Not matching adjacent tile")

        if not anyAdjacent:
            raise Exception("No adjacent tile")

        tile.coords = coords

        for side in sides:
            if adjacent_tiles[side] in self.board.keys():
                adjacent_tile = self.board[adjacent_tiles[side]]
                my_features = [
                    tile.get_feature_by_connection(Connection(side, x))
                    for x in range(3)
                ]
                neighbor_features = list(
                    reversed(
                        [
                            adjacent_tile.get_feature_by_connection(
                                Connection(invert_side(side), x)
                            )
                            for x in range(3)
                        ]
                    )
                )

                tile.ensureCorrect()
                adjacent_tile.ensureCorrect()

                print(f"my tile: {my_features}")
                print(f"adjacent tile: {neighbor_features}")

                for i in range(3):
                    print(f"my feature: {my_features[i]}")
                    print(f"neighbor feature: {neighbor_features[i]}")
                    my_features[i].bind(neighbor_features[i])
                    neighbor_features[i].bind(my_features[i])

        self.board[coords] = tile
        self.tileset.pop()

        self.lastTile = tile

        self.phase = 1

    def placeMeeple(self, feature_index: int):
        self.tilesChanged = set()

        if self.phase != 1:
            raise Exception("Can't place meeple while placing a tile")

        try:
            if feature_index != -1:
                feature = self.lastTile.features[feature_index]
                if self.scorer.check_any_meeples(feature):
                    raise Exception("Feature already has a meeple")

                self.lastTile.placeMeeple(feature_index, self.players[self.turn])
                # closing features
            for feature in self.lastTile.features:
                tiles = self.scorer.score_closed_feature(feature)
                self.tilesChanged.update(tiles)
            self.next_turn()
            self.phase = 0
        except Exception as e:
            traceback.print_exc()
            raise Exception("Can't place meeple")

    def next_turn(self):
        self.turn += 1
        self.turn %= len(self.players)

    def handleEnd(self):
        if not self.is_finished():
            raise Exception(
                "Can't handle the end of game while it is still in progress"
            )

        for tile in self.board.values():
            for feature in tile.features:
                self.scorer.score_open_feature(feature)

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
                feature.parent_tile = tile

            if s_tile:
                startingTile = copy(tile)
                n -= 1

            for i in range(n):
                tileset.append(deepcopy(tile))

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
