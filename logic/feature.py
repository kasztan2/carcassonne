from typing import Sequence

class Connection(object):
    def __init__(self, side: int, number: int) -> None:
        self.side=side
        self.number=number
        
    def rotate_once(self) -> None:
        self.side+=1
        self.side%=4

class Feature(object):
    def __init__(self, _type: int, connections: Sequence[Connection]) -> None:
        self.type = _type
        self.connections = connections

    def rotate(self, times: int) -> None:
        for connection in self.connections:
            connection.rotate_once()
        
        if times != 0:
            self.rotate(times - 1)