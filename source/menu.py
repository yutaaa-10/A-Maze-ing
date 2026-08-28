from visual import Color, display_maze

from .constants import Coord, WALL_COLORS


def clear_terminal() -> None:
    """Clear the terminal and move the cursor to the top-left."""

    print("\x1b[2J\x1b[H", end="", flush=True)


def rotate_wall_color(
    current_index: int,
) -> tuple[int, Color]:
    """Advance to the next wall colour.

    Args:
        current_index: Index of the current wall colour.

    Returns:
        The next colour index and its corresponding colour.
    """

    next_index = (current_index + 1) % len(WALL_COLORS)
    return next_index, WALL_COLORS[next_index]


def print_menu(
    show_solution: bool,
) -> None:
    """Display currently available menu operations.

    Args:
        show_solution: Whether the solution is currently displayed.
    """

    if show_solution:
        solution_label = "Hide Solution"
    else:
        solution_label = "Show Solution"

    print()
    print("===== A-MAZE-ING =====")
    print()
    print("1. Regenerate a New Maze")
    print(f"2. {solution_label}")
    print("3. Change Wall Color")
    print()
    print("0. Quit")
    print()


def pause(message: str) -> None:
    """Show a message and wait before redrawing the screen.

    Args:
        message: Message displayed before waiting for user input.
    """

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
    """Show, hide, and preview the shortest solution path.

    Args:
        hex_text: Hexadecimal representation of the maze.
        entry: Entry coordinate of the maze.
        exit_coord: Exit coordinate of the maze.
        solution: Shortest solution path.
        wall_color: Colour used to display the maze walls.
        show_solution: Whether the solution is currently displayed.

    Returns:
        True if the solution should be displayed, otherwise False.
    """

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
