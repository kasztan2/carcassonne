


class Connection(object):
    def __init__(self, side, number) -> None:
        self.side=side
        self.number=number
        

class Feature(object):
    def __init__(self, _type, connections):
        self.type = _type
        self.connections = connections
