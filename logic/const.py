from collections import namedtuple

SIDES = namedtuple("SIDES", ["LEFT", "UP", "RIGHT", "DOWN"])(0, 1, 2, 3)

FEATURE_TYPES = namedtuple(
    "FEATURE_TYPES", ["CITY", "PENNANT_CITY", "ROAD", "FARM", "CLOISTER"]
)(1, 2, 3, 4, 5)

STARTING_MEEPLE_COUNT = 7

PLAYER_COLORS = [(200, 50, 50), (50, 200, 50), (50, 50, 200), (200, 200, 50)]
