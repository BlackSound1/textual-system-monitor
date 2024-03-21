COMMON_INTERVAL = 1 / 5
UNCOMMON_INTERVAL = 3
RARE_INTERVAL = 10
NET_INTERVAL = 1


def compute_percentage_color(pct: float) -> str:
    """
    Takes a given percentage and returns that percentage, colored according to
    whether usage is high, medium, or low.

    :param pct: The uncolored percentage value
    :return: The colored percentage value as a string
    """

    if pct < 0:
        pct = 0
    elif pct > 100:
        pct = 100

    if pct <= 75:
        pct = f"[#70f97E]{pct:.1f}[/]"
    elif 75 < pct < 90:
        pct = f"[#F9F070]{pct:.1f}[/]"
    else:
        pct = f"[#F76A5D]{pct:.1f}[/]"

    return pct


def bytes2human(n: int) -> str:
    """
    Converts bytes to human-readable format.

    >>> bytes2human(10000)
    '9.8 KB'
    >>> bytes2human(100001221)
    '95.4 MB'

    https://code.activestate.com/recipes/578019

    :param n: The number of bytes
    :return: A string representing a human-readable format of those bytes
    """

    if n < 0:
        return "0.0 B"

    symbols = ('Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi')
    prefix = {}

    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10

    for s in reversed(symbols):
        if abs(n) >= prefix[s]:
            value = float(n) / prefix[s]
            return f'{value:.1f} {s}B'

    return f"{n:.1f} B"
