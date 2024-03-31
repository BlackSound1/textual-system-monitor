from typing import List

from psutil import net_io_counters, cpu_count, cpu_percent, virtual_memory

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
        pct = f"[green]{pct:.1f}[/]"
    elif 75 < pct < 90:
        pct = f"[yellow]{pct:.1f}[/]"
    else:
        pct = f"[red]{pct:.1f}[/]"

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


def update_network_static(new: list, old: list) -> str:
    """
    Update the Network pane with new info for each network interface by generating a
    string containing the new info for each interface

    :param new: The updated network stats
    :param old: The old network stats
    :return: The string needed to update the Static widget with the new info
    """

    static_content = ""

    # For each interface, calculate the new info and add it to the string to return
    for i, item in enumerate(old):
        interface = item["interface"]
        download = bytes2human(new[i]["bytes_recv"])
        upload = bytes2human(new[i]["bytes_sent"])
        upload_speed = bytes2human(
            round(
                (new[i]["bytes_sent"] - item["bytes_sent"]) / NET_INTERVAL,
                2
            )
        )
        download_speed = bytes2human(
            round(
                (new[i]["bytes_recv"] - item["bytes_recv"]) / NET_INTERVAL,
                2
            )
        )

        # Add the new info for this interface to the content of the Static widget
        static_content += (f"[green]{interface}[/]: [blue]Download[/]: {download} at "
                           f"{download_speed} /s | [blue]Upload[/]: {upload} at {upload_speed} /s\n\n")

    return static_content


"""
CPU UTILITIES
"""


def get_cpu_data() -> dict:
    """
    Return a dictionary containing CPU data with keys 'cores', 'overall', and 'individual'

    :return: The dictionary containing CPU data
    """
    return {
        "cores": cpu_count(),
        "overall": cpu_percent(percpu=False),
        "individual": cpu_percent(percpu=True)
    }


def display_percentages_CPU(percentages: list) -> str:
    """
    Display the percentages of each core in a string

    :param percentages: The list of CPU load percentages for each core
    :return: The string containing the formatted percentages
    """

    string = "\n"

    # For each core, colorize the percentage and add it to the string
    for i, pct in enumerate(percentages):
        pct = compute_percentage_color(pct)

        separator = " | " if i < len(percentages) - 1 else ""

        string += f"Core {i + 1}: {pct} % {separator}"

    return string


def update_CPU_static(cpu_data: dict) -> str:
    """
    Generates a string of updated CPU data to update the CPU Screen Static with

    :param cpu_data: The updated CPU data
    :return: The string of updated CPU data
    """

    # Get updated CPU data
    cores = cpu_data['cores']
    overall = cpu_data['overall']
    individual = display_percentages_CPU(cpu_data['individual'])  # Colorize the percentages

    # Return the string to update the relevant Static with
    return f"Cores: {cores}\n\nOverall: {compute_percentage_color(overall)} %\n\nPer Core: {individual}\n\n"


"""
MEMORY UTILITIES
"""


def get_mem_data() -> dict:
    """
    Return a dictionary containing information about the memory usage.

    :return: A dictionary with keys 'total', 'available', 'used', and 'percent'
              representing total memory, available memory, used memory, and percentage used.
    """
    return {
        "total": virtual_memory().total,
        "available": virtual_memory().available,
        "used": virtual_memory().used,
        "percent": virtual_memory().percent
    }
