from typing import List, Union, Dict, Iterator
import platform

from psutil import net_io_counters, cpu_count, cpu_percent, virtual_memory, Process

WINDOWS = platform.system() == "Windows"

if WINDOWS:
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


def compute_percentage_color(
        percentage: Union[int, float],
        combine_output: bool = True
) -> Union[str, tuple[int, str]]:
    """
    Takes a given percentage and returns that percentage, colored according to
    whether usage is high, medium, or low.

    :param percentage: The uncolored percentage value
    :param combine_output: Whether to combine the output into a single string
    :return: The colored percentage value as a string
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

    # Decide whether we should combine the output into a single string
    if combine_output:
        return f"[{color}]{percentage:.1f}[/]"
    else:
        return percentage, color


def bytes_to_human(num_bytes: int, base: int = 1024) -> str:
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
        f'Y{unit_suffix}': base ** 8
    }

    # For each symbol, check if the number of bytes is greater than the corresponding threshold
    for symbol, threshold in reversed(list(symbol_map.items())):
        if abs(num_bytes) >= threshold:
            value = float(num_bytes) / threshold
            return f'{value:.1f} {symbol}B'

    # If the number of bytes is lower than any threshold, return the number of bytes as-is
    return f'{num_bytes:.1f} B'


"""
NETWORK UTILITIES
"""


def get_network_stats() -> List[Dict[str, int]]:
    """
    Get network statistics per interface, sorted by highest download amount.

    :return: A sorted list of dictionaries, each containing the network stats for a single interface.
    """

    return sorted(
        (
            {
                "interface": interface,
                "bytes_sent": stats.bytes_sent,
                "bytes_recv": stats.bytes_recv
            }
            for interface, stats in net_io_counters(pernic=True).items()
        ),
        key=lambda stats: stats['bytes_recv'],
        reverse=True
    )


def update_network_static(new_stats: list, old_stats: list, base: int) -> str:
    """
    Generate a string containing the updated network info for each interface

    :param new_stats: The updated network stats
    :param old_stats: The old network stats
    :param base: The base to use for the conversion (1000 or 1024)

    :return: The string needed to update the Static widget with the new info
    """

    static_content = ""

    # For each interface, calculate the new info and add it to the string to return
    for old_stat, new_stat in zip(old_stats, new_stats):
        interface = old_stat["interface"]
        download = bytes_to_human(new_stat["bytes_recv"], base)
        upload = bytes_to_human(new_stat["bytes_sent"], base)
        upload_speed = bytes_to_human(
            round((new_stat["bytes_sent"] - old_stat["bytes_sent"]) / NET_INTERVAL, 2),
            base
        )
        download_speed = bytes_to_human(
            round((new_stat["bytes_recv"] - old_stat["bytes_recv"]) / NET_INTERVAL, 2),
            base
        )

        static_content += (
            f"[green]{interface}[/]: [blue]Download[/]: {download} at "
            f"{download_speed} /s | [blue]Upload[/]: {upload} at {upload_speed} /s\n\n"
        )

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

    formatted_percentages = "\n"

    # For each core, colorize the percentage and add it to the string
    for core_index, core_percentage in enumerate(percentages):
        formatted_percentage = compute_percentage_color(core_percentage)
        separator = " | " if core_index < len(percentages) - 1 else ""
        formatted_percentages += f"Core {core_index + 1}: {formatted_percentage} % {separator}"

    return formatted_percentages


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


"""
GPU UTILITIES
"""


def get_gpu_data() -> List[Dict[str, Union[str, int]]]:
    """
    Get GPU data from WMI

    :return: The list of GPU data, per video controller.
    """

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

    adapter_ram = int(float(adapter_ram.split(' ')[0]) * 1e9)
    return bytes_to_human(adapter_ram, kb_size)


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
