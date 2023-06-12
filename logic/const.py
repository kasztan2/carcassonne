from collections import namedtuple

SIDES=namedtuple('SIDES', ["LEFT", "UP", "RIGHT", "DOWN"])(1, 2, 3, 4)

FEATURE_TYPES=namedtuple('FEATURE_TYPES', ["CITY", "PENNANT_CITY", "ROAD", "FARM"])(1, 2, 3, 4)