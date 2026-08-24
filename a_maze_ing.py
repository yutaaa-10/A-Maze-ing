from dataclasses import dataclass
import random
from error_handling import check_date
from visual import display_maze
import sys


Coord = tuple[int, int]
Edge = frozenset[Coord]
Edges = set[Edge]


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
    PERFECT = config["PERFECT"]

    gen = MazeGenerator(3, 3)
    maze = gen.generate(42, False)
    # gen = MazeGenerator(width, height)
    # maze = gen.generate(42)
    hex_text = to_hex(maze)
    print(hex_text)

    display_maze(hex_text)
    print()

    ent = 0, 0
    ext = 14, 19

    print(get_shortest_path(maze, ent, ext))
