from logic.feature import Feature
from typing import TYPE_CHECKING, Sequence
from logic.const import FEATURE_TYPES
from collections import Counter
from logic.utils import is_nearby_feature

if TYPE_CHECKING:
    from logic.player import Player


class Scorer(object):
    def __init__(self, parent):
        self.parent = parent

    def get_connected_features(self, feature: Feature) -> Sequence[Feature]:
        """
        Get all features that can be reached from a given feature (including itself)
        """
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
        """Check whether the feature is closed"""
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
        """Get winning players on a given feature (with most meeples)"""
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

    def check_any_meeples(self, feature: Feature) -> bool:
        """Check if there are any meeples on the feature"""
        features = self.get_connected_features(feature)

        print("check any meeples:")
        print([feature.parent_tile.coords for feature in features])

        for feature in features:
            if feature.meeple is not None:
                return True

        return False

    def remove_meeples(self, feature: Feature) -> set:
        """Return meeples to their owners when a feature is completed"""
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
        """Calculate points for a closed feature (returns 0 for open features)"""
        if not self.check_closed(feature) or feature.type == FEATURE_TYPES.FARM:
            return 0
        features = self.get_connected_features(feature)

        tiles = set()

        s = 0

        for feature in features:
            feature.scored = True
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

    def get_city_features_near(self, farm_feature: Feature) -> list:
        """Get city features on the same tile that are touching the given feature (farm)"""
        tile = farm_feature.parent_tile
        return [
            feature
            for feature in tile.features
            if is_nearby_feature(farm_feature, feature)
        ]

    def count_closed_cities_near_farm(self, feature: Feature) -> int:
        """Counts the number of cities touching the farm"""
        features = self.get_connected_features(feature)
        visited_cities = set()

        for feature in features:
            feature.scored = True
            cities = [
                frozenset(self.get_connected_features(f))
                for f in self.get_city_features_near(feature)
            ]
            visited_cities.update(cities)

        return len(visited_cities)

    def calculate_points_for_open(self, feature: Feature) -> int:
        """Calculates the points for an open feature (returns 0 for a closed feature)"""
        if self.check_closed(feature) or feature.scored:
            return 0
        features = self.get_connected_features(feature)

        tiles = set()

        s = 0

        if feature.type == FEATURE_TYPES.CLOISTER:
            coords = feature.parent_tile.coords
            around = coords.get_coords_around()
            return sum([x in self.parent.board.keys() for x in around])

        if feature.type == FEATURE_TYPES.FARM:
            return 3 * self.count_closed_cities_near_farm(feature)

        for feature in features:
            if feature.scored:
                return 0
            feature.scored = True
            if feature.parent_tile in tiles:
                continue

            if feature.type == FEATURE_TYPES.CITY:
                s += 1
            elif feature.type == FEATURE_TYPES.PENNANT_CITY:
                s += 2
            elif feature.type == FEATURE_TYPES.ROAD:
                s += 1
            else:
                raise ValueError("Unknown feature type")

        return s

    def score_closed_feature(self, feature: Feature) -> set:
        """Calculate points for closed feature -> update scores -> remove meeples"""
        if not self.check_closed(feature):
            return set()

        score = self.calculate_points_for_closed(feature)
        players = self.get_players_on_feature(feature)

        for player in players:
            player.addScore(score)

        return self.remove_meeples(feature)

    def score_open_feature(self, feature: Feature) -> None:
        """Calculate points for open features -> update scores -> remove meeples (just in case)"""
        if self.check_closed(feature) or feature.scored:
            return

        score = self.calculate_points_for_open(feature)
        players = self.get_players_on_feature(feature)

        for player in players:
            player.addScore(score)

        return self.remove_meeples(feature)
