"""Maze generation and path finding.

A maze is stored as a set of edges. Each edge is a frozenset holding the
coordinates of two adjacent cells, and its presence means the two cells
are connected. Walls are the absence of an edge.
"""
from dataclasses import dataclass
import random


Coord = tuple[int, int]
Edge = frozenset[Coord]
Edges = set[Edge]


class MazeGenerator:
    """Builds mazes of a fixed size.

    Attributes:
        width: Board width in cells.
        height: Board height in cells.
    """

    def __init__(self, width: int, height: int) -> None:
        """Store the board size.

        Args:
            width: Board width in cells.
            height: Board height in cells.
        """
        self.width = width
        self.height = height

    def generate(self, seed: int | None = None,
                 perfect: bool = True,
                 start: Coord = (0, 0),
                 blocked: set[Coord] | None = None
                 ) -> "Maze":
        """Build a maze with the recursive backtracker algorithm.

        Args:
            seed: Seed for the random number generator.
            perfect: If False, extra edges are added so that loops exist.
            start: Cell the search begins from.
            blocked: Cells that must stay unreachable.

        Returns:
            The generated maze.

        Raises:
            ValueError: If start is one of the blocked cells.
        """
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
        """Walk to unvisited neighbours, backtracking at dead ends.

        Args:
            rng: Random number generator used to pick the next cell.
            edges: Edges collected so far. Modified in place.
            visited_nodes: Cells already reached. Modified in place.
            stack: Path to the current cell. Modified in place.

        Returns:
            None. A cell is entered once, so the edges form a spanning tree.
        """
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
        """Find the neighbours of a cell that have not been reached.

        Args:
            cell: Cell to look around.
            visited_nodes: Cells already reached.

        Returns:
            Neighbours inside the board, in north, east, south, west order.
        """
        x, y = cell
        neighbors: list[Coord] = [
            (x, y - 1),  # north
            (x + 1, y),  # east
            (x, y + 1),  # south
            (x - 1, y),  # west
        ]
        return [
            n for n in neighbors
            if _is_inside(n, self.width,
                          self.height) and n
            not in visited_nodes
        ]

    def _is_addable_edge(self,
                         p1: Coord,
                         p2: Coord,
                         n: int,
                         edges: Edges
                         ) -> bool:
        """Check that an edge can be added without opening an n x n area.

        Only blocks containing both endpoints can be affected, so the
        search is limited to that range.

        Args:
            p1: One endpoint of the candidate edge.
            p2: The other endpoint, adjacent to p1.
            n: Side length of the forbidden open area, in cells.
            edges: Current edges. Not modified.

        Returns:
            True if every n x n block keeps at least one wall inside it.
        """
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
                for r in range(n):
                    for c in range(n):
                        edge = frozenset(
                            ((x + c + 1, y + r), (x + c, y + r)))
                        if c + 1 < n and edge in edges_after:
                            tmp.add(edge)
                        edge = frozenset(
                            ((x + c, y + r + 1), (x + c, y + r)))
                        if r + 1 < n and edge in edges_after:
                            tmp.add(edge)
                if len(tmp) == max_edges_in_grid:
                    return False
        return True

    def _braid(self, maze: "Maze") -> "Maze":
        """Open one wall at each dead end, so that loops exist.

        Cells with no edge at all are skipped, so blocked cells stay
        closed. A dead end is left as it is when every candidate would
        open a 3 x 3 area.

        Args:
            maze: Maze to braid. Not modified.

        Returns:
            A new maze holding a copy of the edges plus the added ones.
        """
        maze_after = Maze(maze.width, maze.height, set(maze.edges))
        for y in range(maze.height):
            for x in range(maze.width):
                if len(neighbors_with_edge((x, y), maze_after)) == 1:
                    for cell in neighbors_without_edge(
                            (x, y), maze_after):
                        if len(neighbors_with_edge(cell, maze_after)) == 0:
                            continue
                        if self._is_addable_edge((x, y),
                                                 cell,
                                                 3,
                                                 maze_after.edges):
                            maze_after.edges.add(frozenset(((x, y), cell)))
                            break
        return maze_after


def _to_path_string(results: list[Coord]) -> str:
    """Turn a list of cells into a string of direction letters.

    Args:
        results: Adjacent cells, from start to goal.

    Returns:
        One letter per step, using N, E, S and W.
    """
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
    """Find the shortest path between two cells.

    The maze is explored one layer at a time, so a cell is always reached
    by a shortest route the first time it is seen.

    Args:
        maze: Maze to walk through.
        start: Cell to start from.
        goal: Cell to reach.

    Returns:
        One letter per step, using N, E, S and W.

    Raises:
        ValueError: If goal cannot be reached from start.
    """
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
    """Find the neighbours a cell can be reached from.

    Args:
        cell: Cell to look around.
        maze: Maze holding the edges.

    Returns:
        Neighbours inside the board, in north, east, south, west order.
    """
    x, y = cell
    neighbors: list[Coord] = [
        (x, y - 1),  # north
        (x + 1, y),  # east
        (x, y + 1),  # south
        (x - 1, y),  # west
    ]
    return [
        n for n in neighbors
        if _is_inside(n, maze.width, maze.height)
        and frozenset((cell, n)) in maze.edges
    ]


def neighbors_without_edge(cell: Coord, maze: "Maze") -> list[Coord]:
    """Find the neighbours a cell is walled off from.

    Args:
        cell: Cell to look around.
        maze: Maze holding the edges.

    Returns:
        Neighbours inside the board, in north, east, south, west order.
    """
    x, y = cell
    neighbors: list[Coord] = [
        (x, y - 1),  # north
        (x + 1, y),  # east
        (x, y + 1),  # south
        (x - 1, y),  # west
    ]
    return [
        n for n in neighbors
        if _is_inside(n, maze.width, maze.height) and
        frozenset((cell, n)) not in maze.edges
    ]


def _is_inside(cell: Coord, width: int, height: int) -> bool:
    """Check that a cell lies within the board.

    Args:
        cell: Cell to test.
        width: Board width in cells.
        height: Board height in cells.

    Returns:
        True if both coordinates are within range.
    """
    x, y = cell
    return x >= 0 and x < width and y >= 0 and y < height


@dataclass
class Maze:
    """A generated maze.

    Attributes:
        width: Board width in cells.
        height: Board height in cells.
        edges: Connections between cells. Each entry is a frozenset of two
            adjacent coordinates, and its presence means the two cells are
            connected.
    """

    width: int
    height: int
    edges: Edges


def wall_bits(edges: Edges, cell: Coord) -> int:
    """Encode the walls of one cell as a bit field.

    Args:
        edges: Connections between cells.
        cell: Cell to encode.

    Returns:
        A value between 0 and 15, setting 1 north, 2 east, 4 south, 8 west
        for each closed wall. The outer border counts as closed.
    """
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
    """Convert a maze to its hexadecimal representation.

    Args:
        maze: Maze to convert.

    Returns:
        One digit per cell and one line per row. See wall_bits for the
        meaning of a digit.
    """
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
