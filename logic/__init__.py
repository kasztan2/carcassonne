# magic from stackoverflow: https://stackoverflow.com/questions/16852811/python-how-to-from-from-all-modules-in-dir
# likely a bad practice

# __all__ = ["game", "player", "tile", "feature", "const", "utils"]
from logic.game import *
from logic.player import *
from logic.tile import *
from logic.feature import *
from logic.const import *
from logic.utils import *

# __all__ = ["game", "player", "const", "tile", "feature", "utils"]
