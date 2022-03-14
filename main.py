from random import randint, choice


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
    target: tuple[int, int]
    generation: int

    def __init__(self, size: int, x: int, y: int):
        """Create new population with `size` members."""
        self.points = []
        for _ in range(size):
            self.points.append(Genome(x, y))

        tx = randint(0, x)
        ty = randint(0, y)
        self.target = (tx, ty)

    def do_generation(self, k=5):
        """Do a generation of evolution."""

        # Do tournament selection
        newpop = []
        # TODO: Save best fitness
        for _ in range(len(self.points) // 2):
            # pick k points at random
            options = []
            for _ in range(k):
                options.append(choice(self.points))

            # Append the randomly selected point with greatest fitness
            newpop.append(max(options, key=lambda p: fitness(p, self.target)))

        # Do crossover

        # Do mutation
        pass
