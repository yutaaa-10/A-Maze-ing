import sys
from secrets import randbits
from typing import cast

from error_handling import check_date
from mazegen.MazeGenerator import (
    Maze,
    MazeGenerator,
    get_shortest_path,
    to_hex,
)
from visual import Color, display_maze


WALL_COLORS: tuple[Color, ...] = (
    Color.WHITE,
    Color.BLUE,
    Color.YELLOW,
    Color.GRAY,
)


SEED_BITS = 32


Coord = tuple[int, int]


def clear_terminal() -> None:
    """Clear the terminal and move the cursor to the top-left."""

    print("\x1b[2J\x1b[H", end="", flush=True)


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


def rotate_wall_color(
    current_index: int,
) -> tuple[int, Color]:
    """Advance to the next wall colour."""

    next_index = (current_index + 1) % len(WALL_COLORS)
    return next_index, WALL_COLORS[next_index]


def print_menu(
    show_solution: bool,
    current_seed: int,
) -> None:
    """Display currently available menu operations."""

    if show_solution:
        solution_label = "Hide Solution"
    else:
        solution_label = "Show Solution"

    print()
    print("===== A-MAZE-ING =====")
    print()
    print(f"Current seed: {current_seed}")
    print("1. Regenerate a New Maze")
    print(f"2. {solution_label}")
    print("3. Change Wall Color")
    print()
    print("0. Quit")
    print()


def pause(message: str) -> None:
    """Show a message and wait before redrawing the screen."""

    try:
        input(f"{message} Press Enter to continue.")
    except (EOFError, KeyboardInterrupt):
        print()


def solution_menu(
    hex_text: str,
    entry: Coord,
    exit_coord: Coord,
    solution: str,
    wall_color: Color,
    show_solution: bool,
) -> bool:
    """Show, hide, and preview the shortest solution path."""

    while True:
        clear_terminal()
        visible_path = solution if show_solution else None

        display_maze(
            hex_text,
            entry=entry,
            exit=exit_coord,
            solution_path=visible_path,
            wall_color=wall_color,
        )

        print()
        print("===== SOLUTION MENU =====")
        print()
        print("1. Show Solution")
        print("2. Hide Solution")
        print("0. Back to Main Menu")
        print()

        try:
            choice = input("select number: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return show_solution

        if choice == "1":
            show_solution = True
        elif choice == "2":
            show_solution = False
        elif choice == "0":
            return show_solution
        else:
            pause("Invalid input data.")


def write_hex_file(
    filename: str,
    hex_text: str,
    entry: Coord,
    exit_coord: Coord,
    solution: str,
) -> None:
    """Write the hexadecimal maze and coordinates to a file."""

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(hex_text)
            file.write("\n")
            file.write(f"{entry[0]},{entry[1]}\n")
            file.write(
                f"{exit_coord[0]},{exit_coord[1]}\n"
            )
            file.write(f"{solution}\n")

    except OSError as exc:
        raise RuntimeError(
            f"Could not write maze to {filename}: {exc}"
        ) from exc


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


def is_inside(cell: Coord, width: int, height: int) -> bool:
    x, y = cell
    return x >= 0 and x < width and y >= 0 and y < height


def main() -> int:
    """Run the maze generator and interactive menu."""

    if len(sys.argv) != 2:
        print(
            f"Usage: python3 {sys.argv[0]} config.txt",
            file=sys.stderr,
        )
        return 1

    config = check_date(sys.argv[1])
    if config is None:
        return 1

    width = cast(int, config["WIDTH"])
    height = cast(int, config["HEIGHT"])
    entry = cast(Coord, config["ENTRY"])
    exit_coord = cast(Coord, config["EXIT"])
    perfect = cast(bool, config["PERFECT"])
    output_file = cast(str, config["OUTPUT_FILE"])

    if not is_inside(entry, width, height):
        return 1
    if not is_inside(exit_coord, width, height):
        return 1

    current_seed = 42
    wall_color_index = 0
    show_solution = False

    PATTERN: list[list[bool]] = [[True, False, False, False, True, True, True],
                                 [True, False, False, False,
                                  False, False, True],
                                 [True, True, True, False, True, True, True],
                                 [False, False, True, False,
                                  True, False, False],
                                 [False, False, True, False, True, True, True]]
    width_42 = len(PATTERN[0])
    height_42 = len(PATTERN)

    gen = MazeGenerator(width, height)
    x = (width - width_42) // 2
    y = (height - height_42) // 2
    top_left = x, y
    if is_addable_42(width, height, width_42, height_42):
        blocked = blocked_add(PATTERN, top_left)
    else:
        blocked = set()
        print("There isn't enough space to place 42.")
    try:
        maze = gen.generate(42, perfect, entry, blocked)
    except IndexError as e:
        print(e)

    hex_text = to_hex(maze)

    try:
        solution = get_shortest_path(
            maze,
            entry,
            exit_coord,
        )
        write_hex_file(
            output_file,
            hex_text,
            entry,
            exit_coord,
            solution,
        )
    except (RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    while True:
        clear_terminal()

        wall_color = WALL_COLORS[wall_color_index]
        visible_path = solution if show_solution else None

        display_maze(
            hex_text,
            entry=entry,
            exit=exit_coord,
            solution_path=visible_path,
            wall_color=wall_color,
        )

        print_menu(show_solution, current_seed)

        try:
            choice = input("select number: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice == "1":
            try:
                new_maze, new_hex_text, new_seed = (
                    regenerate_maze(
                        gen,
                        perfect,
                        entry,
                        blocked
                    )
                )
                new_solution = get_shortest_path(
                    new_maze,
                    entry,
                    exit_coord,
                )

                write_hex_file(
                    output_file,
                    new_hex_text,
                    entry,
                    exit_coord,
                    new_solution,
                )

            except (RuntimeError, ValueError) as exc:
                pause(f"Could not regenerate maze: {exc}")
                continue

            maze = new_maze
            hex_text = new_hex_text
            current_seed = new_seed
            solution = new_solution
            show_solution = False

        elif choice == "2":
            show_solution = solution_menu(
                hex_text,
                entry,
                exit_coord,
                solution,
                wall_color,
                show_solution,
            )

        elif choice == "3":
            wall_color_index, _ = rotate_wall_color(
                wall_color_index
            )

        elif choice == "0":
            break

        else:
            pause("Invalid input data.")

    print("Goodbye!")
    return 0


if __name__ == "__main__":
    result = main()

    if result == 0:
        exit(0)
    else:
        exit(result)
