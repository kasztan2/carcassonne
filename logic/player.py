from logic.const import STARTING_MEEPLE_COUNT


class Player(object):
    def __init__(self, name: str, color: tuple[int, int, int]):
        self.name = name
        self.color = color
        self.score = 0
        self.meeplesLeft = STARTING_MEEPLE_COUNT

    def addScore(self, score_to_add: int) -> None:
        if score_to_add <= 0:
            raise ValueError("Score to be added must be positive")

        self.score += score_to_add

    def minusMeeple(self):
        if self.meeplesLeft == 0:
            raise Exception("Cannot place a meeple: no meeples left")

        self.meeplesLeft -= 1

    def plusMeeple(self):
        if self.meeplesLeft == STARTING_MEEPLE_COUNT:
            raise Exception("How come you return a meeple that was not placed?")

        self.meeplesLeft += 1
