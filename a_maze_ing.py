import sys
from typing import cast

from config_check.error_handling import check_date
from mazegen.MazeGenerator import (
    MazeGenerator,
    get_shortest_path,
    to_hex,
)
from source.constants import Coord, WALL_COLORS
from source.maze_operations import (
    blocked_add,
    is_addable_42,
    is_inside,
    regenerate_maze,
)
from source.menu import (
    clear_terminal,
    pause,
    print_menu,
    rotate_wall_color,
    solution_menu,
)
from source.output import write_hex_file
from visual import display_maze

PATTERN_42: list[list[bool]] = [[True, False, False, False, True, True, True],
                                [True, False, False, False,
                                 False, False, True],
                                [True, True, True, False, True, True, True],
                                [False, False, True, False,
                                 True, False, False],
                                [False, False, True, False, True, True, True]]


def main() -> int:
    """Run the maze generator and interactive menu."""

    if len(sys.argv) != 2:
        print(
            f"Usage: python3 {sys.argv[0]} config.txt",
            file=sys.stderr,
        )
        return 0

    config = check_date(sys.argv[1])
    if config is None:
        return 0

    width = cast(int, config["WIDTH"])
    height = cast(int, config["HEIGHT"])
    entry = cast(Coord, config["ENTRY"])
    exit_coord = cast(Coord, config["EXIT"])
    perfect = cast(bool, config["PERFECT"])
    output_file = cast(str, config["OUTPUT_FILE"])
    current_seed = 42
    wall_color_index = 0
    show_solution = False

    width_42 = len(PATTERN_42[0])
    height_42 = len(PATTERN_42)

    gen = MazeGenerator(width, height)
    x = (width - width_42) // 2
    y = (height - height_42) // 2
    top_left = x, y
    if is_addable_42(width, height, width_42, height_42):
        blocked = blocked_add(PATTERN_42, top_left)
    else:
        blocked = set()
        print("There isn't enough space to place 42.")
    try:
        maze = gen.generate(42, perfect, entry, blocked)
    except ValueError as e:
        print(e)
        return 0

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
        return 0

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
