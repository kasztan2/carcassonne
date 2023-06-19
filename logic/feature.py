from typing import TYPE_CHECKING, Sequence
import uuid

if TYPE_CHECKING:
    from logic.player import Player


class Connection(object):
    """
    Represents a connection (ability to connect to certain point on the tile) from a feature

    Attributes
    ----------
    side : int
        Side, numbered from left side clockwise
    number : int
        Number of the connection on the side (0 to 2)
    """

    def __init__(self, side: int, number: int) -> None:
        self.side = side
        self.number = number

    def rotate_once(self) -> None:
        """
        Rotate 90 degrees to the right
        """
        self.side += 1
        self.side %= 4

    def to_number(self) -> int:
        """
        Returns a number from 0 to 11 (beginning with left side at the bottom)
        """
        return self.side * 3 + self.number

    def __eq__(self, other):
        return self.side == other.side and self.number == other.number

    def __hash__(self):
        return self.to_number()


class Feature(object):
    """
    Represents a feature (farm, road, city, city with pennant or cloister)

    Attributes
    ----------
    type : int
        Type of the feature
    connections : Sequence[Connection]
        Connections (open "ports") to other features
    meeple : Player
        Player that has a meeple on this feature (possibly None)
    uuid : UUID
        Effect of wrong debugging, probably could be ommited
    bindings : Sequence[Feature]
        The actual connections to the other features ("from this feature I *can get to* any other feature in this list")
    parent_tile : Tile
        The tile this feature belongs to
    scored : bool
        Whether it has been counted at the end (while counting open features)
    """

    def __init__(self, _type: int, connections: Sequence[Connection]) -> None:
        self.type = _type
        self.connections = connections
        self.meeple: Player = None
        self.uuid = uuid.uuid4()
        self.bindings = []
        self.parent_tile = None
        self.scored = False

    def rotate(self, times: int) -> None:
        """
        Rotate feature by 90 degrees clockwise `times` times
        """
        for i in range(times % 4):
            for connection in self.connections:
                connection.rotate_once()

    def bind(self, feature: "Feature") -> None:
        """
        Binds to the given feature (makes it able to go from one to another)
        """
        if feature == self:
            return
        print(
            f"Binding {self} at {self.parent_tile.coords} to {feature} at {feature.parent_tile.coords}"
        )
        self.bindings.append(feature)

    def __repr__(self):
        num_to_str = {1: "City", 2: "PCity", 3: "Road", 4: "Farm", 5: "Cloister"}
        return f"{num_to_str[self.type]}[{','.join([str(x.to_number()) for x in self.connections])}]"
