from dataclasses import dataclass
import random
from error_handling import check_date
from visual import Color, display_maze


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
# I changed `edges`, `visited_nodes`,
# and `stack` to local variables within the `generate` function.
# Since these variables are only needed for a single call to `generate`,
# there is no need to maintain them across the entire instance;
# this change is intended to improve the reusability of the `generate` function.

        start: Coord = (0, 0)
        visited_nodes.add(start)
        stack.append(start)
        self._explore(rng, edges, visited_nodes, stack)
        return Maze(self.width, self.height, edges)

    def set_42(self, visited_nodes: set[Coord]) -> None:
        #    define　a list defined as a constant
        # to form the number “42” in a 7-column by 5-row grid,
        # with one empty cell in the center
        PATTERN: list[list[bool]] = [[True, False, False, False, True, True, True],
                                     [True, False, False, False,
                                         False, False, True],
                                     [True, True, True, False, True, True, True],
                                     [False, False, True, False,
                                         True, False, False],
                                     [False, False, True, False, True, True, True]]
    #    define starting point from  upper left cause loop with "for range()"

        wide_42 = len(PATTERN[0])
        height_42 = len(PATTERN)
        x0 = (self.width - wide_42) // 2
        y0 = (self.height - height_42) // 2
        for r in range(height_42):
            for c in range(wide_42):
                if PATTERN[r][c]:
                    visited_nodes.add((x0 + c, y0 + r))

#         Simply by adding it to `visited_nodes`,
# a path through the spanning tree is created that avoids it.
# So, a single isolated “42” is created.

    def _explore(
            self,
            rng: random.Random,
            edges: Edges,
            visited_nodes: set[Coord],
            stack: list[Coord],
    ) -> None:
        self.set_42(visited_nodes)
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

    @staticmethod
    def open_corners(maze: "Maze") -> None:
        w, h = maze.width, maze.height
        maze.edges.update(
            {
                # top_left (0, 0) -> 右, 下
                frozenset(((0, 0), (1, 0))),
                frozenset(((0, 0), (0, 1))),
                # bottom_left (0, h - 1) -> 右, 上
                frozenset(((0, h - 1), (1, h - 1))),
                frozenset(((0, h - 1), (0, h - 2))),
                # top_right (w - 1, 0) -> 左, 下
                frozenset(((w - 1, 0), (w - 2, 0))),
                frozenset(((w - 1, 0), (w - 1, 1))),
                # bottom_right (w - 1, h - 1) -> 左, 上
                frozenset(((w - 1, h - 1), (w - 2, h - 1))),
                frozenset(((w - 1, h - 1), (w - 1, h - 2))),
            }
        )

    def neighbors_without_edge(self, cell: Coord, edges: Edges) -> list[Coord]:
        x, y = cell
        neighbors: list[Coord] = [
            (x, y - 1),  # north
            (x + 1, y),  # east
            (x, y + 1),  # south
            (x - 1, y),  # west
        ]
        return [
            n for n in neighbors
            if self._is_inside(n) and frozenset((cell, n)) not in edges
        ]

    def neighbors_with_edge(self, cell: Coord, edges: Edges) -> list[Coord]:
        x, y = cell
        neighbors: list[Coord] = [
            (x, y - 1),  # north
            (x + 1, y),  # east_unvisited_neighbors
            (x, y + 1),  # south
            (x - 1, y),  # west
        ]
        return [
            n for n in neighbors
            if self._is_inside(n) and frozenset((cell, n)) in edges
        ]

    def _is_addable_edge(self, p1: tuple[int, int], p2: tuple[int, int]) -> bool:
        x1, y1 = p1
        x2, y2 = p2
        lo_limit_x = max(x1, x2) - 2
        up_limit_x = min(x1, x2)
        lo_limit_y = max(y1, y2) - 2
        up_limit_y = min(y1, y2)



    def toPacmanField(self, maze: "Maze") -> None:
        self.open_corners(maze)
        for y in range(maze.height):
            for x in range(maze.width):
                if len(self.neighbors_with_edge((x, y), maze.edges)) == 1:
                    for cell in self.neighbors_without_edge(
                            (x, y), maze.edges):
                        if self._is_addable_edge((x, y), cell):
                            maze.edges.add(frozenset(((x, y), cell)))
                            break

                    # すべてのセルについて:
                    #     もしそれが行き止まりなら:
                    #         辺を持っていない隣を集める
                    #         そのうち、追加しても 3x3 を作らないものを選ぶ
                        # ->左上から3,3のループで見る
                    #         辺を追加する


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


def get_shortest_path(maze: "Maze", ent: Coord, ext: Coord) -> str:
    stack: list[Coord] = []
    visited: set[Coord] = set()
    value = 0

    love


if __name__ == "__main__":
    config = check_date()
    print(config)

    gen = MazeGenerator(20, 20)
    maze = gen.generate(42)
    hex_text = expression_hex(maze)
    print(hex_text)

    display_maze(hex_text)
    ent = 0, 0
    ext = 14, 19
