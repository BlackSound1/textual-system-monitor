import sys
from typing import Literal, cast
from collections.abc import Iterator

from psutil import net_io_counters, cpu_count, cpu_percent, virtual_memory, Process

if sys.platform == "win32":
    from wmi import WMI

"""
CONSTANTS
"""

COMMON_INTERVAL = 1 / 5
UNCOMMON_INTERVAL = 3
RARE_INTERVAL = 10
NET_INTERVAL = 1

AVAILABILITY_MAP = {
    1: "Other",
    2: "Unknown",
    3: "Running or Full Power",
    4: "Warning",
    5: "In Test",
    6: "Not Applicable",
    7: "Power Off",
    8: "Off Line",
    9: "Off Duty",
    10: "Degraded",
    11: "Not Installed",
    12: "Install Error",
    13: "Power Save - Unknown",
    14: "Power Save - Low Power Mode",
    15: "Power Save - Standby",
    16: "Power Cycle",
    17: "Power Save - Warning",
    18: "Paused",
    19: "Not Ready",
    20: "Not Configured",
    21: "Quiesced",
}

"""
GLOBAL UTILITIES
"""


def bytes_to_human(num_bytes: float, base: int = 1024) -> str:
    """
    Converts bytes to human-readable format.

    Can use either 1000 or 1024 as a base.

    If `base` is 1024 (default):

    >>> bytes_to_human(10000)
    '9.8 KB'
    >>> bytes_to_human(100001221)
    '95.4 MB'

    If `base` is 1000:

    >>> bytes_to_human(10000, base=1000)
    '10.0 KB'
    >>> bytes_to_human(100001221, base=1000)
    '100.0 MB'

    Originally inspired by: https://code.activestate.com/recipes/578019

    :param num_bytes: The number of bytes
    :param base: The base to use for the conversion (1000 or 1024)

    :return: A string representing a human-readable format of those bytes
    """

    # If the number of bytes is negative, return '0.0 B'
    if num_bytes < 0:
        return "0.0 B"

    # Determine the unit suffix based on the base
    if base == 1024:
        unit_suffix = 'i'
    else:
        unit_suffix = ''

    # Create a map of symbols and their corresponding thresholds
    symbol_map = {
        f'K{unit_suffix}': base ** 1,
        f'M{unit_suffix}': base ** 2,
        f'G{unit_suffix}': base ** 3,
        f'T{unit_suffix}': base ** 4,
        f'P{unit_suffix}': base ** 5,
        f'E{unit_suffix}': base ** 6,
        f'Z{unit_suffix}': base ** 7,
        f'Y{unit_suffix}': base ** 8,
    }

    # For each symbol, check if the number of bytes is greater than the corresponding threshold
    for symbol, threshold in reversed(list(symbol_map.items())):
        if abs(num_bytes) >= threshold:
            value = num_bytes / threshold
            return f'{value:.1f} {symbol}B'

    # If the number of bytes is lower than any threshold, return the number of bytes as-is
    return f'{num_bytes:.1f} B'


"""
NETWORK UTILITIES
"""


def get_network_stats() -> list[dict[str, str | int]]:
    """
    Get network statistics per interface, sorted by highest download amount.

    :return: A sorted list of dictionaries, each containing the network stats for a single interface.
    """
    return sorted(
        (
            {
                "interface": interface,
                "bytes_sent": stats.bytes_sent,
                "bytes_recv": stats.bytes_recv,
            }
            for interface, stats in net_io_counters(pernic=True).items()
        ),
        key=lambda stats: stats['bytes_recv'],
        reverse=True,
    )


def update_network_static(
        new_stats: list[dict[str,  str | int]],
        old_stats: list[dict[str,  str | int]],
        base: int,
        palette: dict[str, str],
) -> str:
    """
    Generate a string containing the updated network info for each interface

    :param new_stats: The updated network stats
    :param old_stats: The old network stats
    :param base: The base to use for the conversion (1000 or 1024)
    :param palette: The color palette to use for the current theme

    :return: The string needed to update the Static widget with the new info
    """

    static_content = ""

    # For each interface, calculate the new info and add it to the string to return
    for old_stat, new_stat in zip(old_stats, new_stats):
        interface = old_stat["interface"]
        new_bytes_sent = cast(int, new_stat["bytes_sent"])
        old_bytes_sent = cast(int, old_stat["bytes_sent"])
        new_bytes_recv = cast(int, new_stat["bytes_recv"])
        old_bytes_recv = cast(int, old_stat["bytes_recv"])

        download = bytes_to_human(new_bytes_recv, base)
        upload = bytes_to_human(new_bytes_sent, base)
        upload_speed = bytes_to_human(
            round((new_bytes_sent - old_bytes_sent) / NET_INTERVAL, 2),
            base,
        )
        download_speed = bytes_to_human(
            round((new_bytes_recv - old_bytes_recv) / NET_INTERVAL, 2),
            base,
        )

        static_content += (
            f"[bold {palette['green']}]{interface}[/]: [bold {palette['blue']}]Download[/]: {download} at "
            f"{download_speed} /s | [bold {palette['blue']}]Upload[/]: {upload} at {upload_speed} /s\n\n"
        )

    return static_content


"""
CPU UTILITIES
"""


def get_cpu_data() -> dict[str, int | None | float | list[float]]:
    """
    Return a dictionary containing CPU data with keys 'cores', 'overall', and 'individual'

    :return: The dictionary containing CPU data
    """
    return {
        "cores": cpu_count(),
        "overall": cpu_percent(percpu=False),
        "individual": cpu_percent(percpu=True),
    }


def display_percentages_CPU(percentages: list[float], palette: dict[str, str]) -> str:
    """
    Display the percentages of each core in a string

    :param percentages: The list of CPU load percentages for each core
    :param palette: The palette to use for the current theme
    :return: The string containing the formatted percentages
    """

    formatted_percentages = "\n"

    # For each core, colorize the percentage and add it to the string
    for core_index, core_percentage in enumerate(percentages):
        formatted_percentage = get_color_formatted_string(palette, core_percentage)
        separator = " | " if core_index < len(percentages) - 1 else ""
        formatted_percentages += f"Core {core_index + 1}: {formatted_percentage} % {separator}"

    return formatted_percentages


def update_CPU_static(cpu_data: dict[str, int | float | list[float] | None], palette: dict[str, str]) -> str:
    """
    Generates a string of updated CPU data to update the CPU Screen Static with

    :param cpu_data: The updated CPU data
    :param palette: The palette to use for the current theme
    :return: The string of updated CPU data
    """

    # Get updated CPU data
    cores = cpu_data['cores']
    overall = cast(float, cpu_data['overall'])
    individual = display_percentages_CPU(cast(list[float], cpu_data['individual']), palette)  # Colorize the percentages

    # Return the string to update the relevant Static with
    return f"Cores: {cores}\n\nOverall: {get_color_formatted_string(palette, overall)} %\n\nPer Core: {individual}\n\n"


"""
MEMORY UTILITIES
"""


def get_mem_data() -> dict[str, int | float]:
    """
    Return a dictionary containing information about the memory usage.

    :return: A dictionary with keys 'total', 'available', 'used', and 'percent'
              representing total memory, available memory, used memory, and percentage used.
    """
    return {
        "total": virtual_memory().total,
        "available": virtual_memory().available,
        "used": virtual_memory().used,
        "percent": virtual_memory().percent,
    }


"""
GPU UTILITIES
"""


def get_gpu_data() -> list[dict[str, str | int] | None]:
    """
    Get GPU data from WMI

    :return: The list of GPU data, per video controller.
    """

    if sys.platform != "win32":
        return []

    wmi_object = WMI()
    video_controllers = wmi_object.Win32_VideoController()

    gpu_data_list = []

    for controller in video_controllers:
        gpu_data_list.append({
            "gpu": controller.Name,
            "driver_version": controller.DriverVersion,
            "resolution": f"{controller.CurrentHorizontalResolution} x {controller.CurrentVerticalResolution}",
            "adapter_ram": bytes_to_human(controller.AdapterRAM),
            "availability": AVAILABILITY_MAP.get(controller.Availability),
            "refresh": controller.CurrentRefreshRate,
            "status": controller.Status,
        })

    return gpu_data_list


def convert_adapter_ram(adapter_ram: str, kb_size: int) -> str:
    """
    Actually convert the adapter RAM to a human-readable string.

    Given a string like '1.0 GiB', separate this into '1.0' and 'GiB', convert the '1.0' to a quantity of bytes,
    then send that number of bytes to `bytes2human`.

    :param adapter_ram: The string corresponding to the given adapters RAM
    :param kb_size: The KB size to use in conversion
    :return: The string corresponding to the given adapters RAM, converted to a human-readable string
    """
    ram = int(float(adapter_ram.split(' ')[0]) * 1e9)
    return bytes_to_human(ram, kb_size)


"""
PROCESS UTILITIES
"""


def get_non_zero_procs(procs: Iterator[Process]) -> Iterator[Process]:
    """
    Yield processes with non-zero PID.
    Windows SYSTEM IDLE Process is excluded.

    :param procs: Iterable of processes to iterate through
    :return: The processes with a non-zero PID
    """
    for process in procs:
        if process.pid != 0:
            yield process


"""
COLOR UTILITIES
"""


COLOR_MAP = {
    'textual-light': {
        'orange': "#FF8C00",
        'red': "#FF0000",
        'yellow': "#F3CD00",
        'blue': "#7272f6",
        'green': "#008000",
        'pink': "#FF1493",
    },
    'textual-dark': {
        'orange': "#FEA62B",
        'red': "#FF0000",
        'yellow': "#FFFF00",
        'blue': "#ADD8E6",
        'green': "#90EE90",
        'pink': "#FFC0CB",
    },
    'nord': {
        'orange': "#d08770",
        'red': "#bf616a",
        'yellow': "#ebcb8b",
        'blue': "#88c0d0",
        'green': "#a3be8c",
        'pink': "#b48ead",
    },
    'gruvbox': {
        'orange': "#fe8019",
        'red': "#fb4934",
        'yellow': "#fabd2f",
        'blue': "#83a598",
        'green': "#8ec07c",
        'pink': "#d3869b",
    },
    'catpuccin-mocha': {
        'orange': "#fab387",
        'red': "#f38ba8",
        'yellow': "#f9e2af",
        'blue': "#89b4fa",
        'green': "#a6e3a1",
        'pink': "#f5c2e7",
    },
    'catpuccin-latte': {
        'orange': "#fe640b",
        'red': "#d20f39",
        'yellow': "#df8e1d",
        'blue': "#1e66f5",
        'green': "#40a02b",
        'pink': "#ea76cb",
    },
    'catpuccin-frappe': {
        'orange': "#ef9f76",
        'red': "#e78284",
        'yellow': "#e5c890",
        'blue': "#8caaee",
        'green': "#a6d189",
        'pink': "#f4b8e4",
    },
    'catpuccin-macchiato': {
        'orange': "#f5a97f",
        'red': "#ed8796",
        'yellow': "#eed49f",
        'blue': "#8aadf4",
        'green': "#a6da95",
        'pink': "#f5bde6",
    },
    'dracula': {
        'orange': "#ffb86c",
        'red': "#ff5555",
        'yellow': "#f1fa8c",
        'blue': "#8be9fd",
        'green': "#50fa7b",
        'pink': "#ff79c6",
    },
    'tokyo-night': {
        'orange': "#ff9e64",
        'red': "#f7768e",
        'yellow': "#e0af68",
        'blue': "#7aa2f7",
        'green': "#41a6b5",
        'pink': "#9d7cd8",
    },
    'monokai': {
        'orange': "#ffb84d",
        'red': "#ff56ad",
        'yellow': "#ffff2f",
        'blue': "#7effff",
        'green': "#d6ff53",
        'pink': "#e4bfff",
    },
    'flexoki': {
        'orange': "#da702c",
        'red': "#d14d41",
        'yellow': "#d0a215",
        'blue': "#4385be",
        'green': "#879a39",
        'pink': "#ce5d97",
    },
    'solarized-light': {
        'orange': "#cb4b16",
        'red': "#dc322f",
        'yellow': "#b58900",
        'blue': "#268bd2",
        'green': "#859900",
        'pink': "#d33682",
    },
    'solarized-dark': {
        'orange': "#d75f00",
        'red': "#d70000",
        'yellow': "#af8700",
        'blue': "#0087ff",
        'green': "#5f8700",
        'pink': "#af005f",
    },
    'rose-pine': {
        'orange': "#ebbcba",
        'red': "#eb6f92",
        'yellow': "#f6c177",
        'blue': "#31748f",
        'green': "#9ccfd8",
        'pink': "#c4a7e7",
    },
    'rose-pine-moon': {
        'orange': "#ea9a97",
        'red': "#eb6f92",
        'yellow': "#f6c177",
        'blue': "#3e8fb0",
        'green': "#9ccfd8",
        'pink': "#c4a7e7",
    },
    'rose-pine-dawn': {
        'orange': "#d7827e",
        'red': "#b4637a",
        'yellow': "#ea9d34",
        'blue': "#286983",
        'green': "#56949f",
        'pink': "#907aa9",
    },
    'atom-one-dark': {
        'orange': "#e06c75",
        'red': "#be5046",
        'yellow': "#e5c07b",
        'blue': "#61afef",
        'green': "#98c379",
        'pink': "#c678dd",
    },
    'atom-one-light': {
        'orange': "#e45649",
        'red': "#ca1243",
        'yellow': "#c18401",
        'blue': "#4078f2",
        'green': "#50a14f",
        'pink': "#a626a4",
    },
}


def compute_percentage_color(percentage: int | float) -> tuple[float, Literal["green", "yellow", "red"]]:
    """
    Takes a given percentage and returns "green", "yellow", or "red" depending on how high the number is.

    :param percentage: The number to associate with a color.
    :return: The color associated with that percentage.
    """

    # Clamp the percentage between 0 and 100
    percentage = max(0, min(100, percentage))

    # Round the percentage to 1 decimal place
    percentage = round(percentage, 1)

    # Set the color based on the percentage
    if percentage <= 75:
        color = "green"
    elif 75 < percentage < 90:
        color = "yellow"
    else:
        color = "red"

    return percentage, color


def get_palette(name: str) -> dict[str, str]:
    """
    Get the current color pallette based on the current color theme.

    :param str name: The name of the current color theme.
    :return dict[str, str]: The color pallette as a dict.
    """
    return COLOR_MAP.get(name, COLOR_MAP['textual-dark'])


def get_color_formatted_string(palette: dict[str, str], num: int | float) -> str:
    """
    Produces a string like "[color]text[/]", based on the given theme and number.

    :param palette: The color palette to select a color based on.
    :param num: The number to turn into a formatted color string.

    :return str: The color-formatted string.
    """
    _, color_pre = compute_percentage_color(num)
    color_post = palette[color_pre]
    return f"[bold {color_post}]{num}[/]"
