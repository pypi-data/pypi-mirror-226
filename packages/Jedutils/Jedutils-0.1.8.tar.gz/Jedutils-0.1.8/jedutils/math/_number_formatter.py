def format_bytes(size):
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


def parse_bytes(size_str):
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
        raise ValueError("Invalid size format.")

    try:
        size = float(size)
    except ValueError:
        raise ValueError("Invalid size format.")

    power = suffixes.index(suffix)
    size *= 1024**power
    return int(size)
