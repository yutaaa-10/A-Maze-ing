from dataclasses import dataclass
import random
from error_handling import check_date
from visual import display_maze
import sys
from mazegen import MazeGenerator


Coord = tuple[int, int]
Edge = frozenset[Coord]
Edges = set[Edge]



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


def write_hex_file(filename: str, hex_text: str, entry: Coord, exit: Coord) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(hex_text)
            file.write("\n")
            file.write(f"{entry[0]},{entry[1]}\n")
            file.write(f"{exit[0]},{exit[1]}\n")
    except OSError as e:
        raise RecursionError(
            f"Could not write maze to {filename}: {e}"
        ) from e

# from secrets import randbits
# SEED_BITS = 32

# def regenerate_maze(
#     generator: MazeGenerator,
#     perfect: bool,
# ) -> tuple[Maze, str, int]:
#     """Generate a new maze with a fresh, reproducible seed."""

#     seed = randbits(SEED_BITS)
#     maze = generator.generate(seed, perfect)
#     hex_text = to_hex(maze)
#     return maze, hex_text, seed

# from visual import Color


# WALL_COLORS: tuple[Color, ...] = (
#     Color.WHITE,
#     Color.BLUE,
#     Color.RED,
# )


# def rotate_wall_color(
#     current_index: int,
# ) -> tuple[int, Color]:
#     """Advance to the next available wall colour."""

#     next_index = (current_index + 1) % len(WALL_COLORS)
#     next_color = WALL_COLORS[next_index]
#     return next_index, next_color



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            f"Usage: python3 {sys.argv[0]} config.txt",
            file=sys.stderr,
        )
        raise SystemExit(1)
    config = check_date(sys.argv[1])
    if config is None:
        raise SystemExit(1)
    print(config)
    width = config["WIDTH"]
    height = config["HEIGHT"]
    entry = config["ENTRY"]
    exit = config["EXIT"]
    perfect = config["PERFECT"]
    output_file = config["OUTPUT_FILE"]

    gen = MazeGenerator(3, 3)
    maze = gen.generate(42, False)
    # gen = MazeGenerator(width, height)
    # maze = gen.generate(42)
    hex_text = to_hex(maze)

    try:
        write_hex_file(output_file, hex_text, entry, exit)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.strderr)
        raise SyntaxError(1)
    
    display_maze(hex_text)
    print()

    wall_color_index = 0
    show_solution = False
    solution = None

    # while True:
    #     clear_terminal()

    #     wall_color = WALL_COLORS[wall_color_index]

    #     print("===== A-Maze-ing =====")
    #     print(f"Current seed: {current_seed}")
    #     print()

    #     display_maze(
    #         hex_text,
    #         entry=entry,
    #         exit=exit,
    #         wall_color=wall_color,
    #     )

    #     print_menu(show_solution, current_seed)

    #     try:
    #         choice = input("Select: ").strip()
    #     except (EOFError, KeyboardInterrupt):
    #         print()
    #         break

    #     if choice == "1":
    #         maze, hex_text, current_seed = regenerate_maze(
    #             gen,
    #             perfect,
    #         )
    #         solution = None
    #         show_solution = False

    #     elif choice == "2":
    #         pass

    #     elif choice == "3":
    #         wall_color_index, _ = rotate_wall_color(
    #             wall_color_index
    #         )   

    #     elif choice == "0":
    #         break

    #     else:
    #         try:
    #             input(
    #                 "Invalid input data. "
    #                 "Press Enter to continue."
    #             )
    #         except (EOFError, KeyboardInterrupt):
    #             print()
    #             break


    # print(get_shortest_path(maze, ent, ext))


