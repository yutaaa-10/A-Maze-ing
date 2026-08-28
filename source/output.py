from .constants import Coord


def write_hex_file(
    filename: str,
    hex_text: str,
    entry: Coord,
    exit_coord: Coord,
    solution: str,
) -> None:
    """Write the maze data to an output file.

    Args:
        filename: Path of the output file.
        hex_text: Hexadecimal representation of the maze.
        entry: Entry coordinate of the maze.
        exit_coord: Exit coordinate of the maze.
        solution: Shortest solution path.

    Raises:
        RuntimeError: If the output file cannot be written.
    """

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
