from dataclasses import dataclass
import random
from error_handling import check_date


Coord = tuple[int, int]
Edge = frozenset[Coord]
Edges = set[Edge]


class MazeGenerator:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def generate(self, seed: int | None = None) -> "Maze":
        rng = random.Random(seed)
        # Making unique random number generator
        edges: Edges = set()
        visited_nodes: set[Coord] = set()
        stack: list[Coord] = []
        start: Coord = (0, 0)
        visited_nodes.add(start)
        stack.append(start)
        self._explore(rng, edges, visited_nodes, stack)
        return Maze(self.width, self.height, edges)

    def generate_42(self, visited_nodes: set[Coord]) -> None:
        PATTERN: list[list[bool]] = [[True, False, False, False, True, True, True],
                                     [True, False, False, False,
                                         False, False, True],
                                     [True, True, True, False, True, True, True],
                                     [False, False, True, False,
                                         True, False, False],
                                     [False, False, True, False, True, True, True]]
        
        x0 = (self.width - 7) // 2
        y0 = (self.height - 5) // 2

    def _explore(
            self,
            rng: random.Random,
            edges: Edges,
            visited_nodes: set[Coord],
            stack: list[Coord],
    ) -> None:
        self.generate_42(visited_nodes)
        while stack:
            cur = stack[-1]
            unvisited: list[Coord] = self._unvisited_neighbors(
                cur, visited_nodes)
            if unvisited:
                nxt = rng.choice(unvisited)
                edges.add(frozenset((cur, nxt)))
                visited_nodes.add(nxt)
                stack.append(nxt)
            else:
                stack.pop()

    def _unvisited_neighbors(
        self, cell: Coord, visited_nodes: set[Coord]
    ) -> list[Coord]:
        x, y = cell
        neighbors: list[Coord] = [
            (x, y - 1),  # north
            (x + 1, y),  # east
            (x, y + 1),  # south
            (x - 1, y),  # west
        ]
        return [
            n for n in neighbors
            if self._is_inside(n) and n not in visited_nodes
        ]

    def _is_inside(self, cell: Coord) -> bool:
        x, y = cell
        return x >= 0 and x < self.width and y >= 0 and y < self.height


@dataclass
class Maze:
    width: int
    height: int
    edges: Edges


def wall_bits(edges: Edges, cell: Coord) -> int:
    x, y = cell
    value = 0
    # North
    if frozenset(((x, y), (x, y - 1))) not in edges:
        value += 1
    # East
    if frozenset(((x, y), (x + 1, y))) not in edges:
        value += 2
    # South
    if frozenset(((x, y), (x, y + 1))) not in edges:
        value += 4
    # West
    if frozenset(((x, y), (x - 1, y))) not in edges:
        value += 8
    return value


# @dataclass
# class Cell:
#     cell: tuple[int, int]
#     value: int
#     visited: bool = False


def expression_hex(maze: "Maze") -> str:
    width = maze.width
    height = maze.height
    x, y = 0, 0
    tmp: list[str] = []
    for y in range(height):
        for x in range(width):
            value = wall_bits(maze.edges, (x, y))
            tmp.append(format(value, "x"))
        tmp.append('\n')
    return "".join(tmp)


# def get_shortest_path(maze: "Maze", ent: Coord, ext: Coord) -> str:
#     stack: list[Coord] = []
#     visited: set[Coord] = set()
#     value = 0
if __name__ == "__main__":
    config = check_date()
    print(config)
    gen = MazeGenerator(15, 20)
    maze = gen.generate(42)
    print(expression_hex(maze))
    ent = 0, 0
    ext = 14, 19
