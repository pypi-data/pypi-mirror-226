def format_bytes(size: int):
    """
    Converts a size in bytes to a human-readable format

    Args:
        size (``int``):
            The size in bytes

    Returns:
        ``str``:
            The formatted size with the appropriate suffix

    """

    suffixes = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size >= 1024 and i < len(suffixes) - 1:
        size /= 1024
        i += 1
    return f"{size:.2f} {suffixes[i]}"


def parse_bytes(size_str: str):
    """
    Converts a size in a human-readable format to bytes

    Args:
        size_str (``str``):
            The size in a human-readable format, e.g., ``2.00 KB``

    Returns:
        ``int``:
            The size in bytes

    Raises:
        ``ValueError``:
            If the input ``size_str`` is in an invalid format

    """

    suffixes = ["B", "KB", "MB", "GB", "TB"]
    size_str = size_str.strip()
    size, suffix = size_str[:-2], size_str[-2:].upper()

    if suffix not in suffixes:
        raise ValueError("Invalid size format")

    try:
        size = float(size)
    except ValueError:
        raise ValueError("Invalid size format")

    power = suffixes.index(suffix)
    size *= 1024**power
    return int(size)


units = [
    ("year", 365 * 24 * 60 * 60),
    ("day", 24 * 60 * 60),
    ("hour", 60 * 60),
    ("minute", 60),
    ("second", 1),
]


def format_duration(seconds: int, format_option: str = "short"):
    """
    Formats the given duration in seconds into a human-readable string representation

    Args:
        seconds (``int``):
            The duration in seconds

        format_option (``str``, *optional*):
            The formatting option either ``long`` or ``short``. Default is "short"

    Returns:
        ``str``:
            The formatted duration string

    Raises:
        ``ValueError``:
            If the duration is a negative number
    """

    if seconds < 0:
        raise ValueError("Duration must be a non-negative number")

    parts = []
    for unit, duration in units:
        if seconds >= duration:
            count = seconds // duration
            seconds %= duration

            if count > 1:
                unit += "s"

            parts.append(f"{count} {unit}")

    if not parts:
        return "0 seconds"

    if format_option == "long":
        if len(parts) == 1:
            return parts[0]
        last_part = parts.pop()
        return ", ".join(parts) + " and " + last_part
    elif format_option == "short":
        hours = int(seconds // 3600)
        minutes = int((seconds // 60) % 60)
        seconds = int(seconds % 60)

        time_parts = []
        if hours > 0:
            time_parts.append(str(hours))
        time_parts.append(f"{minutes:02d}")
        time_parts.append(f"{seconds:02d}")
        return ":".join(time_parts)
    else:
        raise ValueError("Invalid format option. Available options: 'long', 'short'")
