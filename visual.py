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


def color_block(color: Color) -> str:
    """Return one 2-character by 1-line block in an RGB colour."""

    red, green, blue = color.value
    spaces = " " * PIXEL_WIDTH
    return f"\x1b[48;2;{red};{green};{blue}m{spaces}\x1b[0m"


def render_canvas(
    canvas: Canvas,
    wall_color: Color = Color.WHITE,
    corridor_color: Color = Color.BLACK,
) -> str:
    """Convert a logical canvas to an ANSI-coloured terminal string."""

    wall_block = color_block(wall_color)
    corridor_block = color_block(corridor_color)
    output: list[str] = []

    for row in canvas:
        output.append("".join(
            wall_block if is_wall else corridor_block
            for is_wall in row
        ))

    return "\n".join(output)


def render_maze(
    hex_text: str,
    wall_color: Color = Color.WHITE,
    corridor_color: Color = Color.BLACK,
) -> str:

    grid = parse_hex_maze(hex_text)
    height = len(grid)
    width = len(grid[0])
    canvas = create_canvas(width, height)

    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            draw_cell(canvas, x, y, value)

    return render_canvas(canvas, wall_color, corridor_color)


def display_maze(
    hex_text: str,
    wall_color: Color = Color.WHITE,
    corridor_color: Color = Color.BLACK,
) -> None:
    """Print hexadecimal maze data as a coloured terminal maze."""

    print(render_maze(hex_text, wall_color, corridor_color))
