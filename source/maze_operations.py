from secrets import randbits

from mazegen.MazeGenerator import (
    Maze,
    MazeGenerator,
    to_hex,
)

from .constants import Coord, SEED_BITS


def regenerate_maze(
    generator: MazeGenerator,
    perfect: bool,
    start: Coord,
    blocked: set[Coord]
) -> tuple[Maze, str, int]:
    """Generate a new maze with a fresh random seed.

    Args:
        generator: Maze generator used to create the maze.
        perfect: Whether to generate a perfect maze.
        start: Starting coordinate of the maze generation.
        blocked: Coordinates that cannot be used in the maze.

    Returns:
        The generated maze, its hexadecimal representation,
        and the seed used for generation.
    """

    seed = randbits(SEED_BITS)
    maze = generator.generate(seed, perfect, start, blocked)
    hex_text = to_hex(maze)
    return maze, hex_text, seed


def blocked_add(PATTERN: list[list[bool]],  top_left: Coord) -> set[Coord]:
    """Create blocked coordinates from a boolean pattern.

    Args:
        pattern: Boolean pattern representing blocked cells.
        top_left: Top-left coordinate where the pattern is placed.

    Returns:
        A set of coordinates corresponding to blocked cells.
    """

    blocked: set[Coord] = set()
    wid = len(PATTERN[0])
    hei = len(PATTERN)
    x0, y0 = top_left

    for r in range(hei):
        for c in range(wid):
            if PATTERN[r][c]:
                blocked.add((x0 + c, y0 + r))
    return blocked


def is_addable_42(
    width: int,
    height: int,
    width_42: int,
    height_42: int,
) -> bool:
    """Check whether the 42 pattern fits inside the maze.

    Args:
        width: Width of the maze.
        height: Height of the maze.
        width_42: Width of the 42 pattern.
        height_42: Height of the 42 pattern.

    Returns:
        True if the 42 pattern fits inside the maze, otherwise False.
    """

    return width >= width_42 + 2 and height >= height_42 + 2


def is_inside(cell: Coord, width: int, height: int) -> bool:
    x, y = cell
    """Check whether a coordinate is inside the maze.

    Args:
        cell: Coordinate to check.
        width: Width of the maze.
        height: Height of the maze.

    Returns:
        True if the coordinate is inside the maze, otherwise False.
    """

    return x >= 0 and x < width and y >= 0 and y < height
