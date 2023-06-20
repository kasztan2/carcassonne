from logic.const import STARTING_MEEPLE_COUNT


class Player(object):
    """
    Represents a player

    Attributes
    ----------
    name : str
        Name of the player
    color : tuple
        Color of the player (color of the meeples)
    score : int
        Current score
    meeplesLeft : int
        How many meeples the player has left
    """

    def __init__(self, name: str, color: tuple[int, int, int]):
        self.name = name
        self.color = color
        self.score = 0
        self.meeplesLeft = STARTING_MEEPLE_COUNT

    def addScore(self, score_to_add: int) -> None:
        """Updates the score"""
        if score_to_add < 0:
            raise ValueError("Score to be added must be positive")

        self.score += score_to_add

    def minusMeeple(self) -> None:
        """Subtract one meeple when placing it on the board"""
        if self.meeplesLeft == 0:
            raise Exception("Cannot place a meeple: no meeples left")

        self.meeplesLeft -= 1

    def plusMeeple(self) -> None:
        """Add one meeple when a feature is completed"""
        if self.meeplesLeft == STARTING_MEEPLE_COUNT:
            raise Exception("How come you return a meeple that was not placed?")

        self.meeplesLeft += 1
