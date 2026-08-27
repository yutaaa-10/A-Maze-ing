from .constants import Coord


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
