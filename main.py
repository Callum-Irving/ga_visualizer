from random import randint, choice, random
from time import sleep


class Genome:
    x: int
    y: int

    def __init__(self, x: int, y: int, random=False):
        """Create a new random genome."""
        if random:
            self.x = randint(0, x)
            self.y = randint(0, y)
        else:
            self.x = x
            self.y = y


def fitness(guess: Genome, target: tuple[int, int]) -> float:
    """Return 1 / squared distance between vectors."""
    xdist = max(0.1, guess.x - target[0])
    ydist = max(0.1, guess.y - target[0])

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
            self.points.append(Genome(x, y, random=True))

        tx = randint(0, x)
        ty = randint(0, y)
        self.target = (tx, ty)
        self.generation = 0

    def do_generation(self, mut_rate=0.1, k=5, max_mut=5):
        """
        Do a generation of evolution.

        Returns mean fitness.
        """

        # Do tournament selection
        newpop = []
        parents = []
        best = max(self.points, key=lambda p: fitness(p, self.target))
        newpop.append(best)
        parents.append(best)
        for _ in range(len(self.points) // 2):
            # pick k points at random
            options = []
            for _ in range(k):
                options.append(choice(self.points))

            # Append the randomly selected point with greatest fitness
            parents.append(max(options, key=lambda p: fitness(p, self.target)))

        while len(newpop) < len(self.points):
            # select random parents
            p1 = choice(parents)
            p2 = choice(parents)

            # do crossover
            if random() < 0.5:
                child = Genome(p1.x, p2.y)
            else:
                child = p1

            newpop.append(child)

        # Do mutation
        for point in newpop[1:]:
            if random() < mut_rate:
                point.x += randint(-max_mut, max_mut)
                point.x = max(0, point.x)
            if random() < mut_rate:
                point.y += randint(-max_mut, max_mut)
                point.y = max(0, point.y)

        self.points = newpop
        self.generation += 1

    def avg_fitness(self) -> float:
        sum = 0
        for p in self.points:
            sum += fitness(p, self.target)

        return sum / len(self.points)


if __name__ == "__main__":
    pop = Population(100, 5000, 5000)
    while True:
        avg = pop.avg_fitness()
        print("Generation:", pop.generation, "- Average fitness:", avg)
        pop.do_generation(0.1, 2, 1)
        sleep(0.1)
    
