INTERVAL = 1 / 5


def compute_percentage_color(pct: float) -> str:
    """
    Takes a given percentage and returns that percentage, colored according to
    whether usage is high, medium, or low.

    :param pct: The uncolored percentage value
    :return: The colored percentage value as a string
    """

    if pct <= 75:
        pct = f"[green]{pct:.1f}[/green]"
    elif 75 < pct < 90:
        pct = f"[yellow]{pct:.1f}[/yellow]"
    else:
        pct = f"[red]{pct:.1f}[/red]"

    return pct


def bytes2human(n: int) -> str:
    """
    Converts bytes to human-readable format.

    >>> bytes2human(10000)
    '9.8K'
    >>> bytes2human(100001221)
    '95.4M'

    https://code.activestate.com/recipes/578019

    :param n: The number of bytes
    :return: A string representing a human-readable format of those bytes
    """

    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}

    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10

    for s in reversed(symbols):
        if abs(n) >= prefix[s]:
            value = float(n) / prefix[s]
            return f'{value:.1f} {s}B'

    return f"{n} B"
