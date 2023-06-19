from logic.feature import Feature
from logic.tile import Tile
from typing import Sequence
from logic.const import FEATURE_TYPES
from logic.utils import Coords
from collections import Counter


class Scorer(object):
    def __init__(self, parent):
        self.parent = parent

    def get_connected_features(self, feature: Feature) -> Sequence[Feature]:
        visited = [feature]
        toVisit = [feature]

        while len(toVisit) > 0:
            current = toVisit.pop(0)

            for neighbor in current.bindings:
                if neighbor not in visited:
                    visited.append(neighbor)
                    toVisit.append(neighbor)

        print(f"bfs output: {visited}")

        return visited

    def check_closed(self, feature: Feature) -> bool:
        if feature.type == FEATURE_TYPES.FARM:
            return False

        if feature.type == FEATURE_TYPES.CLOISTER:
            coords = feature.parent_tile.coords
            around = coords.get_coords_around()
            return all([x in self.parent.board.keys() for x in around])

        features = self.get_connected_features(feature)
        # check whether all connected feature objects have the same number of bindings as connections
        print(
            f"check_closed on {feature}: {all([len(f.connections) == len(f.bindings) for f in features])}"
        )
        return all([len(f.connections) == len(f.bindings) for f in features])

    def get_players_on_feature(self, feature: Feature) -> Sequence["Player"]:
        """Get winning players on a given feature"""
        features = self.get_connected_features(feature)

        players = []
        for feature in features:
            if feature.meeple is not None:
                players.append(feature.meeple)

        counter = Counter(players)
        if len(counter) == 0:
            return []
        max_count = counter.most_common(1)[0][1]

        output = []
        for key, count in counter.items():
            if count == max_count:
                output.append(key)

        return output

    def check_any_meeples(self, feature: Feature):
        features = self.get_connected_features(feature)

        print("check any meeples:")
        print([feature.parent_tile.coords for feature in features])

        for feature in features:
            if feature.meeple is not None:
                return True

        return False

    def remove_meeples(self, feature: Feature) -> set:
        tiles = set()
        features = self.get_connected_features(feature)

        for feature in features:
            if feature.meeple is not None:
                feature.meeple.plusMeeple()
                feature.meeple = None
                tiles.add(feature.parent_tile)

        print(f"tiles: {tiles}")

        return tiles

    def calculate_points_for_closed(self, feature: Feature) -> int:
        if not self.check_closed(feature) or feature.type == FEATURE_TYPES.FARM:
            return 0
        features = self.get_connected_features(feature)

        tiles = set()

        s = 0

        for feature in features:
            if feature.parent_tile in tiles:
                continue

            if feature.type == FEATURE_TYPES.CITY:
                s += 2
            elif feature.type == FEATURE_TYPES.PENNANT_CITY:
                s += 4
            elif feature.type == FEATURE_TYPES.CLOISTER:
                s += 9
            elif feature.type == FEATURE_TYPES.ROAD:
                s += 1
            else:
                raise ValueError("Unknown feature type")

        return s

    def score_closed_feature(self, feature: Feature) -> set:
        if not self.check_closed(feature):
            return set()

        score = self.calculate_points_for_closed(feature)
        players = self.get_players_on_feature(feature)

        for player in players:
            player.addScore(score)

        return self.remove_meeples(feature)
