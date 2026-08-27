from dataclasses import dataclass
import random
# from error_handling import check_date
from visual import display_maze

Coord = tuple[int, int]
Edge = frozenset[Coord]
Edges = set[Edge]


class MazeGenerator:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def generate(self, seed: int | None = None, perfect: bool = True,  start: Coord = (0, 0), blocked: set[Coord] | None = None) -> "Maze":
        if blocked is None:
            blocked = set()
        rng = random.Random(seed)
        # Making unique random number generator
        edges: Edges = set()
        visited_nodes: set[Coord] = set()
        if start in blocked:
            raise ValueError(f"start {start} is in blocked")
        visited_nodes.add(start)
        visited_nodes.update(blocked)
        stack: list[Coord] = []
# I changed `edges`, `visited_nodes`,
# and `stack` to local variables within the `generate` function.
# Since these variables are only needed for a single call to `generate`,
# there is no need to maintain them across the entire instance;
# this change is intended to improve the reusability of the `generate` function.
        stack.append(start)
        self._explore(rng, edges, visited_nodes, stack)
        maze = Maze(self.width, self.height, edges)
        if not perfect:
            maze = self._braid(maze)
        return maze

    def _explore(
            self,
            rng: random.Random,
            edges: Edges,
            visited_nodes: set[Coord],
            stack: list[Coord],
    ) -> None:
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
            if _is_inside(n, self.width, self.height) and n not in visited_nodes
        ]

    def _is_addable_edge(self, p1: Coord, p2: Coord, n: int, edges: Edges) -> bool:
        candidate = frozenset((p1, p2))
        edges_after = edges | {candidate}
        x1, y1 = p1
        x2, y2 = p2
        lo_limit_x = max(x1, x2, n - 1) - (n - 1)
        up_limit_x = min(x1, x2, self.width - n)
        lo_limit_y = max(y1, y2, n - 1) - (n - 1)
        up_limit_y = min(y1, y2, self.height - n)
        max_edges_in_grid = 2 * n * (n-1)
        for y in range(lo_limit_y, up_limit_y + 1):
            for x in range(lo_limit_x, up_limit_x + 1):
                tmp: Edges = set()
                for r in range(3):
                    for c in range(3):
                        # if _is_inside((x + c, y + r), self.width, self.height):
                        # right
                        edge = frozenset(
                            ((x + c + 1, y + r), (x + c, y + r)))
                        if c + 1 < n and edge in edges_after:
                            tmp.add(edge)
                        # down
                        edge = frozenset(
                            ((x + c, y + r + 1), (x + c, y + r)))
                        if r + 1 < n and edge in edges_after:
                            tmp.add(edge)
                if len(tmp) == max_edges_in_grid:
                    return False
        return True

    def _braid(self, maze: "Maze") -> "Maze":
        maze_after = Maze(maze.width, maze.height, set(maze.edges))
        # self.open_corners(maze_after)
        for y in range(maze.height):
            for x in range(maze.width):
                if len(neighbors_with_edge((x, y), maze_after)) == 1:
                    for cell in neighbors_without_edge(
                            (x, y), maze_after):
                        if len(neighbors_with_edge(cell, maze_after)) == 0:
                            continue
                        if self._is_addable_edge((x, y), cell, 3, maze_after.edges):
                            maze_after.edges.add(frozenset(((x, y), cell)))
                            break
        return maze_after

        # すべてのセルについて:
        #     もしそれが行き止まりなら:
        #         辺を持っていない隣を集める
        #         そのうち、追加しても 3x3 を作らないものを選ぶ
        # ->左上から3,3のループで見る
        #         辺を追加する


def _to_path_string(results: list[Coord]) -> str:
    paths: list[str] = []
    cur = results[0]
    dr: dict[Coord, str] = {
        (0, -1): "N", (1, 0): "E", (0, 1): "S", (-1, 0): "W"}
    for cell in results[1:]:
        dx = cell[0] - cur[0]
        dy = cell[1] - cur[1]
        paths.append(dr[(dx, dy)])
        cur = cell
    return "".join(paths)


def get_shortest_path(maze: "Maze", start: Coord, goal: Coord) -> str:
    frontier: list[Coord] = [start]
    visited: set[Coord] = set()
    visited.add(start)
    came_from: dict[Coord, Coord] = {}
    while frontier and goal not in visited:
        next_frontier: list[Coord] = []
        for cur in frontier:
            for nxt in neighbors_with_edge(cur, maze):
                if nxt in visited:
                    continue
                next_frontier.append(nxt)
                visited.add(nxt)
                came_from[nxt] = cur
        frontier = next_frontier
    # If goal is impossible, frontier become Empty
    if goal not in visited:
        raise ValueError(f"no path from {start} to {goal}: "
                         f"{goal} is unreachable in this maze")
    results: list[Coord] = []
    cur = goal
    while cur != start:
        results.append(cur)
        cur = came_from[cur]
    results.append(start)
    results.reverse()
    return _to_path_string(results)


def neighbors_with_edge(cell: Coord, maze: "Maze") -> list[Coord]:
    x, y = cell
    neighbors: list[Coord] = [
        (x, y - 1),  # north
        (x + 1, y),  # east_unvisited_neighbors
        (x, y + 1),  # south
        (x - 1, y),  # west
    ]
    return [
        n for n in neighbors
        if _is_inside(n, maze.width, maze.height) and frozenset((cell, n)) in maze.edges
    ]


def neighbors_without_edge(cell: Coord, maze: "Maze") -> list[Coord]:
    x, y = cell
    neighbors: list[Coord] = [
        (x, y - 1),  # north
        (x + 1, y),  # east
        (x, y + 1),  # south
        (x - 1, y),  # west
    ]
    return [
        n for n in neighbors
        if _is_inside(n, maze.width, maze.height) and frozenset((cell, n)) not in maze.edges
    ]


def _is_inside(cell: Coord, width: int, height: int) -> bool:
    x, y = cell
    return x >= 0 and x < width and y >= 0 and y < height


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


def to_hex(maze: "Maze") -> str:
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


def blocked_add(PATTERN: list[list[bool]],  top_left: Coord) -> set[Coord]:
    #    define　a list defined as a constant
    # to form the number “42” in a 7-column by 5-row grid,
    # with one empty cell in the center

    #    define starting point from  upper left cause loop with "for range()"

    blocked: set[Coord] = set()
    wid = len(PATTERN[0])
    hei = len(PATTERN)
    x0, y0 = top_left

    for r in range(hei):
        for c in range(wid):
            if PATTERN[r][c]:
                blocked.add((x0 + c, y0 + r))
    return blocked


def is_addable_42(width: int, height: int, width_42: int, height_42: int) -> bool:
    return width >= width_42 + 2 and height >= height_42 + 2
