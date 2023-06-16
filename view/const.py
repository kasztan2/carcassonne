from pygame.locals import *
from collections import namedtuple

COLORS = namedtuple("COLORS", ["FARM", "ROAD", "CITY", "PENNANT_CITY", "CLOISTER"])(
    Color("mediumseagreen"),
    Color("gray"),
    Color("firebrick"),
    Color("darkblue"),
    Color("gold"),
)
