from enum import Enum

from .canvas import (
    Canvas,
    CanvasPosition,
    cell_to_canvas_center,
    create_canvas,
    draw_cell,
    find_42_centers,
    parse_hex_maze,
    path_to_canvas_positions,
)


PIXEL_WIDTH = 2

class Color(Enum):
    """RGB colours available for walls and corridors."""

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

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
    solution_positions: set[CanvasPosition],
    wall_color: Color = Color.WHITE,
    corridor_color: Color = Color.BLACK,
    pattern_color: Color = Color.GRAY,
    entry_color: Color = Color.GREEN,
    exit_color: Color = Color.YELLOW,
    solution_color: Color = Color.RED,
) -> str:
    """Convert a logical canvas to an ANSI-coloured terminal string."""

    wall_block = color_block(wall_color)
    corridor_block = color_block(corridor_color)
    pattern_block = color_block(pattern_color)
    entry_block = color_block(entry_color)
    exit_block = color_block(exit_color)
    solution_block = color_block(solution_color)
    output: list[str] = []

    for canvas_y, row in enumerate(canvas):
        output_row: list[str] = []

        for canvas_x, is_wall in enumerate(row):
            position = (canvas_x, canvas_y)

            if position == entry_center:
                output_row.append(entry_block)
            elif position == exit_center:
                output_row.append(exit_block)
            elif position in solution_positions:
                output_row.append(solution_block)
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
    solution_path: str | None = None,
    wall_color: Color = Color.WHITE,
    corridor_color: Color = Color.BLACK,
    pattern_color: Color = Color.GRAY,
    entry_color: Color = Color.GREEN,
    exit_color: Color = Color.YELLOW,
    solution_color: Color = Color.RED,
) -> str:

    grid = parse_hex_maze(hex_text)
    height = len(grid)
    width = len(grid[0])
    canvas = create_canvas(width, height)
    entry_center = None
    exit_center = None
    solution_positions: set[CanvasPosition] = set()

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

    if solution_path is not None:
        if entry is None:
            raise ValueError(
                "ENTRY is required to draw the solution."
            )
        solution_positions = path_to_canvas_positions(
            entry,
            solution_path,
            width,
            height,
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
        solution_positions,
        wall_color=wall_color,
        corridor_color=corridor_color,
        pattern_color=pattern_color,
        entry_color=entry_color,
        exit_color=exit_color,
        solution_color=solution_color,
    )


def display_maze(
    hex_text: str,
    entry: tuple[int, int] | None = None,
    exit: tuple[int, int] | None = None,
    solution_path: str | None = None,
    wall_color: Color = Color.WHITE,
    corridor_color: Color = Color.BLACK,
    pattern_color: Color = Color.GRAY,
    entry_color: Color = Color.GREEN,
    exit_color: Color = Color.YELLOW,
    solution_color: Color = Color.RED,
) -> None:
    """Print hexadecimal maze data as a coloured terminal maze."""

    print(render_maze(
        hex_text,
        entry=entry,
        exit=exit,
        solution_path=solution_path,
        wall_color=wall_color,
        corridor_color=corridor_color,
        pattern_color=pattern_color,
        entry_color=entry_color,
        exit_color=exit_color,
        solution_color=solution_color,
    ))
