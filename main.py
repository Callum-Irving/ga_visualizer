from random import randint


class Genome:
    x: int
    y: int

    def __init__(self, xmax: int, ymax: int):
        """Create a new random genome."""
        self.x = randint(0, xmax)
        self.y = randint(0, ymax)


def get_err(guess: Genome, target: tuple[int, int]) -> float:
    """Return squared distance between vectors."""
    xdist = guess.x - target[0]
    ydist = guess.y - target[0]

    # a^2 + b^2 = c^2
    return xdist**2 + ydist**2
