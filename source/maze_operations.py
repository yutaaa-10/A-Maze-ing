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
    """Generate a new maze with a fresh, reproducible seed."""

    seed = randbits(SEED_BITS)
    maze = generator.generate(seed, perfect, start, blocked)
    hex_text = to_hex(maze)
    return maze, hex_text, seed


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


def is_addable_42(
    width: int,
    height: int,
    width_42: int,
    height_42: int,
) -> bool:
    return width >= width_42 + 2 and height >= height_42 + 2


def is_inside(cell: Coord, width: int, height: int) -> bool:
    x, y = cell
    return x >= 0 and x < width and y >= 0 and y < height
