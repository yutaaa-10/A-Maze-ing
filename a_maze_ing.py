from dataclasses import dataclass
import random


Coord = tuple[int, int]
Edge = frozenset[Coord]
Edges = set[Edge]


class MazeGenerator:
    def __init__(self, width: int, height: int) -> None:
        self.edges: Edges = set()
        self.visited_nodes: set[Coord] = set()
        self.stack: list[Coord] = []
        self.width = width
        self.height = height

    def generate(self, seed: int | None = None) -> "Maze":
        rng = random.Random(seed)
        # Making unique random number generator
        x, y = 0, 0
        self.visited_nodes.add((x, y))
        self.stack.append((x, y))
        while self.stack:
            x, y = self.stack[-1]
            unvisited: list[Coord] = self._unvisited_neighbors((x, y))
            unvisited[rng.randint(0, len(unvisited))]
        maze = self.Maze(self.width, self.height, self.edges)
        return maze

    def _is_inside(self, cell: Coord) -> bool:
        x, y = cell
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return True
        else:
            return False

    def _unvisited_neighbors(self, cell: Coord) -> list[Coord]:
        x, y = cell
        # north = x, y - 1
        # east = x + 1, y
        # south = x, y + 1
        # west = x - 1, y
        neighbors: list[Coord] = [
            (x, y - 1),
            (x + 1, y),
            (x, y + 1),
            (x - 1, y),
        ]
        unvisited: list[Coord] = []

        for i in neighbors:
            if (i) not in self.visited_nodes and self._is_inside(i):
                unvisited.append(i)
        return unvisited

    @dataclass
    class Maze:
        width: int
        height: int
        edges: Edges
