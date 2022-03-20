from random import randint, choice, random
import pygame
from pygame.surface import Surface
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count


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

    def fitness(self, target: tuple[int, int]) -> float:
        """Return the fitness of the genome."""
        xdist = max(0.1, abs(self.x - target[0]))
        ydist = max(0.1, abs(self.y - target[1]))
        return 1 / (xdist**2 + ydist**2)


class Population:
    x: int
    y: int
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

        self.x = x
        self.y = y

        self.generation = 0

    def do_generation(self, mut_rate=0.1, k=5, max_mut=5):
        """
        Do a generation of evolution.

        Returns mean fitness.
        """

        # Do tournament selection
        newpop = []
        parents = []
        best = max(self.points, key=lambda p: p.fitness(self.target))
        newpop.append(best)
        parents.append(best)
        for _ in range(len(self.points) // 2):
            # pick k points at random
            options = []
            for _ in range(k):
                options.append(choice(self.points))

            # Append the randomly selected point with greatest fitness
            parents.append(max(options, key=lambda p: p.fitness(self.target)))

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
                point.x = min(max(0, point.x), self.x)
            if random() < mut_rate:
                point.y += randint(-max_mut, max_mut)
                point.y = min(max(0, point.y), self.y)

        self.points = newpop
        self.generation += 1

    def avg_fitness(self) -> float:
        """Compute the average fitness of the current population."""
        sum = 0
        for p in self.points:
            sum += p.fitness(self.target)

        return sum / len(self.points)


CELL_SIZE = 8


def draw_population(screen: Surface, pop: Population):
    # Draw population
    screen.fill((255, 255, 255))
    for p in pop.points:
        surf = pygame.Surface((CELL_SIZE, CELL_SIZE))
        surf.set_alpha(64)
        surf.fill((51, 153, 255))
        screen.blit(surf, (p.x * CELL_SIZE, p.y * CELL_SIZE))

    # Draw target
    pygame.draw.circle(
        screen,
        (255, 0, 0),
        (pop.target[0] * CELL_SIZE, pop.target[1] * CELL_SIZE),
        CELL_SIZE / 2,
    )

    pygame.display.flip()


if __name__ == "__main__":
    pop = Population(400, 120, 120)

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode([pop.x * CELL_SIZE, pop.y * CELL_SIZE])

    index = count()
    xs = []
    ys = []

    def step(_):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        pop.do_generation(0.1, 2, 1)
        fitness = pop.avg_fitness()
        xs.append(next(index))
        ys.append(fitness)
        plt.cla()
        plt.xlabel("Generation")
        plt.ylabel("Mean fitness")
        plt.plot(xs, ys)

        draw_population(screen, pop)

    ani = FuncAnimation(plt.gcf(), step, interval=100)

    plt.tight_layout()
    plt.show()
    pygame.quit()
