from random import randint


class Genome:
    x: int
    y: int

    def __init__(self, xmax: int, ymax: int):
        """Create a new random genome."""
        self.x = randint(0, xmax)
        self.y = randint(0, ymax)


def fitness(guess: Genome, target: tuple[int, int]) -> float:
    """Return 1 / squared distance between vectors."""
    xdist = guess.x - target[0]
    ydist = guess.y - target[0]

    # a^2 + b^2 = c^2
    return 1 / (xdist**2 + ydist**2)


class Population:
    points: list[Genome]
    generation: int

    def __init__(self, size: int, x: int, y: int):
        """Create new population with `size` members."""
        self.points = []
        for _ in range(size):
            self.points.append(Genome(x, y))

    def do_generation(self):
        # TODO
        pass
