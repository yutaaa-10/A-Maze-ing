from enum import Enum

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

PIXEL_WIDTH = 2

HexGrid = list[list[int]]
Canvas = list[list[bool]]


class Color(Enum):
    """RGB colours available for walls and corridors."""

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)


def parse_hex_maze(hex_text: str) -> HexGrid:

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

    if width <= 0 or height <= 0:
        raise ValueError("Canvas width and height must be greater than zero.")

    canvas_width = width * 2 + 1
    canvas_height = height * 2 + 1
    return [
        [False for _ in range(canvas_width)]
        for _ in range(canvas_height)
    ]


def draw_cell(canvas: Canvas, x: int, y: int, value: int) -> None:

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


def find_42_centers(grid: HexGrid) -> set[tuple[int, int]]:
    """Return canvas coordinates of fully closed cells."""

    centers: set[tuple[int, int]] = set()

    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value == 0xF:
                center_x = x * 2 + 1
                center_y = y * 2 + 1
                centers.add((center_x, center_y))

    return centers


def cell_to_canvas_center(
    cell: tuple[int, int],
    width: int,
    height: int,
    name: str,
) -> tuple[int, int]:
    """Convert a maze cell coordinate to its canvas centre."""

    x, y = cell
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(
            f"{name} {cell} is outside the maze "
            f"({width}x{height})."
        )

    center_x = x * 2 + 1
    center_y = y * 2 + 1
    return (center_x, center_y)


def color_block(color: Color) -> str:
    """Return one 2-character by 1-line block in an RGB colour."""

    red, green, blue = color.value
    spaces = " " * PIXEL_WIDTH
    return f"\x1b[48;2;{red};{green};{blue}m{spaces}\x1b[0m"


def render_canvas(
    canvas: Canvas,
    pattern_centers: set[tuple[int, int]],
    entry_center: tuple[int, int] | None,
    exit_center: tuple[int, int] | None,
    wall_color: Color = Color.WHITE,
    corridor_color: Color = Color.BLACK,
    pattern_color: Color = Color.GRAY,
    entry_color: Color = Color.GREEN,
    exit_color: Color = Color.YELLOW,
) -> str:
    """Convert a logical canvas to an ANSI-coloured terminal string."""

    wall_block = color_block(wall_color)
    corridor_block = color_block(corridor_color)
    pattern_block = color_block(pattern_color)
    entry_block = color_block(entry_color)
    exit_block = color_block(exit_color)
    output: list[str] = []

    for canvas_y, row in enumerate(canvas):
        output_row: list[str] = []

        for canvas_x, is_wall in enumerate(row):
            position = (canvas_x, canvas_y)

            if position == entry_center:
                output_row.append(entry_block)
            elif position == exit_center:
                output_row.append(exit_block)
            elif position in pattern_centers:
                output_row.append(pattern_block)
            elif is_wall:
                output_row.append(wall_block)
            else:
                output_row.append(corridor_block)

        output.append("".join(output_row))

    return "\n".join(output)


def render_maze(
    hex_text: str,
    entry: tuple[int, int] | None = None,
    exit: tuple[int, int] | None = None,
    wall_color: Color = Color.WHITE,
    corridor_color: Color = Color.BLACK,
    pattern_color: Color = Color.GRAY,
    entry_color: Color = Color.GREEN,
    exit_color: Color = Color.YELLOW,
) -> str:

    grid = parse_hex_maze(hex_text)
    height = len(grid)
    width = len(grid[0])
    canvas = create_canvas(width, height)
    entry_center = None
    exit_center = None

    if entry is not None:
        entry_center = cell_to_canvas_center(
            entry,
            width,
            height,
            "ENTRY",
        )

    if exit is not None:
        exit_center = cell_to_canvas_center(
            exit,
            width,
            height,
            "EXIT",
        )

    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            draw_cell(canvas, x, y, value)

    pattern_centers = find_42_centers(grid)

    return render_canvas(
        canvas,
        pattern_centers,
        entry_center,
        exit_center,
        wall_color=wall_color,
        corridor_color=corridor_color,
        pattern_color=pattern_color,
        entry_color=entry_color,
        exit_color=exit_color,
    )


def display_maze(
    hex_text: str,
    entry: tuple[int, int] | None = None,
    exit: tuple[int, int] | None = None,
    wall_color: Color = Color.WHITE,
    corridor_color: Color = Color.BLACK,
    pattern_color: Color = Color.GRAY,
    entry_color: Color = Color.GREEN,
    exit_color: Color = Color.YELLOW,
) -> None:
    """Print hexadecimal maze data as a coloured terminal maze."""

    print(render_maze(
        hex_text,
        entry=entry,
        exit=exit,
        wall_color=wall_color,
        corridor_color=corridor_color,
        pattern_color=pattern_color,
        entry_color=entry_color,
        exit_color=exit_color,
    ))
