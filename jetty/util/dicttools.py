def merge(source, dest):
    """
    Merge dict and arrays (override scalar values).

    Keys from source override keys from dest, and elements from lists in source
    are appended to lists in dest.

    Args:
        source (dict): to copy from
        dest (dict): to copy to (modified in place)
    """
    for key, value in source.items():

        if key not in dest:
            dest[key] = value
            continue

        # Merge dict
        if isinstance(value, dict) and isinstance(dest[key], dict):
            merge(value, dest[key])
            continue

        if isinstance(value, list) and isinstance(dest[key], list):
            dest[key] = dest[key] + value
            continue

        dest[key] = value

    return dest
