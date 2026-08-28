NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

HexGrid = list[list[int]]
Canvas = list[list[bool]]
Coord = tuple[int, int]
CanvasPosition = tuple[int, int]

DIRECTIONS: dict[str, Coord] = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}


def parse_hex_maze(hex_text: str) -> HexGrid:
    """Parse hexadecimal maze text into a grid.

    Args:
        hex_text: Hexadecimal text representing the maze.

    Returns:
        The parsed maze as a two-dimensional integer grid.
    """

    lines = hex_text.splitlines()
    if not lines:
        raise ValueError("Maze data is empty.")

    width = len(lines[0])
    if width == 0:
        raise ValueError("Maze width must be greater than zero.")

    grid: HexGrid = []
    for line_number, line in enumerate(lines, start=1):
        if len(line) != width:
            raise ValueError(
                f"Line {line_number} has a different maze width."
            )

        try:
            row = [int(character, 16) for character in line]
        except ValueError as exc:
            raise ValueError(
                f"Line {line_number} contains a non-hexadecimal character."
            ) from exc

        grid.append(row)

    return grid


def create_canvas(width: int, height: int) -> Canvas:
    """Create an empty canvas for drawing the maze.

    Args:
        width: Width of the maze.
        height: Height of the maze.

    Returns:
        An empty boolean canvas sized for the maze and its walls.
    """

    if width <= 0 or height <= 0:
        raise ValueError("Canvas width and height must be greater than zero.")

    canvas_width = width * 2 + 1
    canvas_height = height * 2 + 1
    return [
        [False for _ in range(canvas_width)]
        for _ in range(canvas_height)
    ]


def draw_cell(canvas: Canvas, x: int, y: int, value: int) -> None:
    """Draw the walls of a maze cell on the canvas.

    Args:
        canvas: Canvas on which the cell is drawn.
        x: Horizontal coordinate of the maze cell.
        y: Vertical coordinate of the maze cell.
        value: Bitmask representing the walls of the cell.
    """

    center_x = x * 2 + 1
    center_y = y * 2 + 1

    if value & NORTH:
        for offset in (-1, 0, 1):
            canvas[center_y - 1][center_x + offset] = True

    if value & EAST:
        for offset in (-1, 0, 1):
            canvas[center_y + offset][center_x + 1] = True

    if value & SOUTH:
        for offset in (-1, 0, 1):
            canvas[center_y + 1][center_x + offset] = True

    if value & WEST:
        for offset in (-1, 0, 1):
            canvas[center_y + offset][center_x - 1] = True

    canvas[center_y - 1][center_x - 1] = True


def find_42_centers(grid: HexGrid) -> set[tuple[int, int]]:
    """Find canvas centers of fully closed cells.

    Args:
        grid: Maze grid containing hexadecimal wall values.

    Returns:
        A set of canvas coordinates for fully closed cells.
    """

    centers: set[tuple[int, int]] = set()

    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value == 0xF:
                center_x = x * 2 + 1
                center_y = y * 2 + 1
                centers.add((center_x, center_y))

    return centers


def cell_to_canvas_center(
    cell: Coord,
    width: int,
    height: int,
    name: str,
) -> tuple[int, int]:
    """Convert a maze cell coordinate to its canvas center.

    Args:
        cell: Maze cell coordinate to convert.
        width: Width of the maze.
        height: Height of the maze.
        name: Name used to identify the coordinate in error messages.

    Returns:
        The corresponding center coordinate on the canvas.
    """

    x, y = cell
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(
            f"{name} {cell} is outside the maze "
            f"({width}x{height})."
        )

    center_x = x * 2 + 1
    center_y = y * 2 + 1
    return (center_x, center_y)


def path_to_canvas_positions(
    start: Coord,
    path: str,
    width: int,
    height: int,
) -> set[CanvasPosition]:
    """Convert a solution path into connected canvas positions.

    Args:
        start: Starting coordinate of the solution path.
        path: Solution path represented by N, E, S, and W.
        width: Width of the maze.
        height: Height of the maze.

    Returns:
        A set of canvas positions representing the solution path.
    """

    x, y = start
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError("Solution start is outside the maze.")

    center_x = x * 2 + 1
    center_y = y * 2 + 1
    positions: set[CanvasPosition] = {(center_x, center_y)}

    for direction in path:
        if direction not in DIRECTIONS:
            raise ValueError(
                f"Invalid solution direction: {direction}"
            )

        dx, dy = DIRECTIONS[direction]
        next_x = x + dx
        next_y = y + dy
        if not (0 <= next_x < width and 0 <= next_y < height):
            raise ValueError("Solution path goes outside the maze.")

        next_center_x = next_x * 2 + 1
        next_center_y = next_y * 2 + 1
        middle_x = (center_x + next_center_x) // 2
        middle_y = (center_y + next_center_y) // 2

        positions.add((middle_x, middle_y))
        positions.add((next_center_x, next_center_y))

        x = next_x
        y = next_y
        center_x = next_center_x
        center_y = next_center_y

    return positions
