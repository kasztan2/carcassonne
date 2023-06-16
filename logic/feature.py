from typing import Sequence
import uuid


class Connection(object):
    def __init__(self, side: int, number: int) -> None:
        self.side = side
        self.number = number

    def rotate_once(self) -> None:
        self.side += 1
        self.side %= 4

    def to_number(self) -> int:
        return self.side * 3 + self.number

    def __eq__(self, other):
        return self.side == other.side and self.number == other.number

    def __hash__(self):
        return self.to_number()


class Feature(object):
    def __init__(self, _type: int, connections: Sequence[Connection]) -> None:
        self.type = _type
        self.connections = connections
        self.uuid = uuid.uuid4()

    def rotate(self, times: int) -> None:
        for i in range(times % 4):
            for connection in self.connections:
                connection.rotate_once()

    def __repr__(self):
        num_to_str = {1: "City", 2: "PCity", 3: "Road", 4: "Farm", 5: "Cloister"}
        return f"{num_to_str[self.type]}[{','.join([str(x.to_number()) for x in self.connections])}]"

    def __eq__(self, other):
        return self.uuid == other.uuid
