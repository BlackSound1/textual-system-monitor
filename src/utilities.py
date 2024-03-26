from typing import List

from psutil import net_io_counters

COMMON_INTERVAL = 1 / 5
UNCOMMON_INTERVAL = 3
RARE_INTERVAL = 10
NET_INTERVAL = 1

"""
GLOBAL UTILITIES
"""


def compute_percentage_color(pct: float) -> str:
    """
    Takes a given percentage and returns that percentage, colored according to
    whether usage is high, medium, or low.

    :param pct: The uncolored percentage value
    :return: The colored percentage value as a string
    """

    # Make sure the percentage is within 0 and 100
    if pct < 0:
        pct = 0
    elif pct > 100:
        pct = 100

    # Set the color based on the percentage
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

    # If the number of bytes is negative, return '0.0 B'
    if n < 0:
        return "0.0 B"

    symbols = ('Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi')
    prefix = {}

    # Set the prefix for each symbol
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10

    # Find the largest symbol that is smaller than n
    for s in reversed(symbols):
        if abs(n) >= prefix[s]:
            value = float(n) / prefix[s]
            return f'{value:.1f} {s}B'

    # If no symbol was found, return '0.0 B'
    return f"{n:.1f} B"


"""
NETWORK UTILITIES
"""


def get_network_stats() -> List[dict]:
    """
    Utility function to get network statistics, per interface.

    :return: A list of dicts, each one containing the network statistics for a single interface. Sorted
             by highest download amount
    """

    # Go through each interface and its accompanying stats. Get the interface name and upload/ download info.
    # Append this as a dict to the stats list
    stats = [
        {
            "interface": interface,
            "bytes_sent": interface_io.bytes_sent,
            "bytes_recv": interface_io.bytes_recv
        }
        for interface, interface_io in net_io_counters(pernic=True).items()
    ]

    # Sort by highest download amount
    return sorted(stats, key=lambda x: x['bytes_recv'], reverse=True)
