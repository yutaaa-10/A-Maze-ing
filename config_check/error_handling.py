from typing import Union


ConfigValue = Union[int, bool, str, tuple[int, int]]


class ConfigError(Exception):
    """Raised when the configuration file is invalid."""


def parse_coordinate(value: str, key: str) -> tuple[int, int]:
    """Parse a configuration value as a coordinate.

    Args:
        value: Coordinate value in x,y format.
        key: Configuration key associated with the value.

    Returns:
        The parsed x and y coordinates.
    """

    parts = value.split(",")

    if len(parts) != 2:
        raise ConfigError(
            f"{key} must have the format x,y. Got: {value!r}"
        )

    try:
        x = int(parts[0].strip())
        y = int(parts[1].strip())
    except ValueError as exc:
        raise ConfigError(
            f"{key} coordinates must be integers. Got: {value!r}"
        ) from exc

    return (x, y)


def parse_bool(value: str, key: str) -> bool:
    """Parse a configuration value as a boolean.

    Args:
        value: Boolean value represented as True or False.
        key: Configuration key associated with the value.

    Returns:
        The parsed boolean value.
    """

    if value == "True":
        return True

    if value == "False":
        return False

    raise ConfigError(
        f"{key} must be True or False. Got: {value!r}"
    )


def read_config(filename: str) -> dict[str, ConfigValue]:
    """Read and validate a maze configuration file.

    Args:
        filename: Path to the configuration file.

    Returns:
        A dictionary containing the parsed configuration values.
    """

    config: dict[str, ConfigValue] = {}

    required_keys = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()

                # Empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # KEY=VALUE syntax check
                if "=" not in line:
                    raise ConfigError(
                        f"Line {line_number}: expected KEY=VALUE. "
                        f"Got: {line!r}"
                    )

                key, value = line.split("=", 1)

                key = key.strip()
                value = value.strip()

                if not key:
                    raise ConfigError(
                        f"Line {line_number}: key cannot be empty."
                    )

                if not value:
                    raise ConfigError(
                        f"Line {line_number}: "
                        f"{key} cannot have an empty value."
                    )

                # Duplicate keys
                if key in config:
                    raise ConfigError(
                        f"Line {line_number}: "
                        f"duplicate key {key!r}."
                    )

                if key in ("WIDTH", "HEIGHT"):
                    try:
                        number = int(value)
                    except ValueError as exc:
                        raise ConfigError(
                            f"Line {line_number}: "
                            f"{key} must be an integer. "
                            f"Got: {value!r}"
                        ) from exc

                    if number <= 0:
                        raise ConfigError(
                            f"Line {line_number}: "
                            f"{key} must be greater than 0."
                        )

                    config[key] = number

                elif key in ("ENTRY", "EXIT"):
                    config[key] = parse_coordinate(value, key)

                elif key == "PERFECT":
                    config[key] = parse_bool(value, key)

                elif key == "OUTPUT_FILE":
                    config[key] = value

                else:
                    # Additional keys are allowed by the subject.
                    config[key] = value

    except FileNotFoundError as exc:
        raise ConfigError(
            f"Configuration file not found: {filename}"
        ) from exc

    except PermissionError as exc:
        raise ConfigError(
            f"Permission denied while reading: {filename}"
        ) from exc

    except OSError as exc:
        raise ConfigError(
            f"Could not read configuration file: {exc}"
        ) from exc

    # Check mandatory keys
    missing_keys = required_keys - config.keys()

    if missing_keys:
        missing = ", ".join(sorted(missing_keys))
        raise ConfigError(
            f"Missing required configuration keys: {missing}"
        )

    validate_config(config)

    return config


def validate_config(config: dict[str, ConfigValue]) -> None:
    """Validate configuration values for the maze.

    Args:
        config: Parsed configuration values to validate.
    """

    width = config["WIDTH"]
    height = config["HEIGHT"]
    entry = config["ENTRY"]
    exit = config["EXIT"]

    if not isinstance(width, int):
        raise ConfigError("WIDTH must be an integer.")

    if not isinstance(height, int):
        raise ConfigError("HEIGHT must be an integer.")

    if not isinstance(entry, tuple):
        raise ConfigError("ENTRY must be coordinates.")

    if not isinstance(exit, tuple):
        raise ConfigError("EXIT must be coordinates.")

    entry_x, entry_y = entry
    exit_x, exit_y = exit

    if not (0 <= entry_x < width and 0 <= entry_y < height):
        raise ConfigError(
            f"ENTRY {entry} is outside the maze "
            f"({width}x{height})."
        )

    if not (0 <= exit_x < width and 0 <= exit_y < height):
        raise ConfigError(
            f"EXIT {exit} is outside the maze "
            f"({width}x{height})."
        )

    if entry == exit:
        raise ConfigError(
            "ENTRY and EXIT must be different."
        )


def check_data(
        filename: str,
) -> dict[str, ConfigValue] | None:
    """Read the configuration and handle configuration errors.

    Args:
        filename: Path to the configuration file.

    Returns:
        The parsed configuration, or None if validation fails.
    """

    try:
        config = read_config(filename)

    except ConfigError as exc:
        print(f"Error: {exc}")
        return None

    return config
