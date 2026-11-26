"""
LINUX GPU UTILITIES

Collects GPU statistics on Linux, prioritising NVIDIA (via pynvml / NVML)
with a generic lspci + DRM fallback for other graphics hardware.
"""

import contextlib
import subprocess
from pathlib import Path
from typing import cast

try:
    import pynvml
except ImportError:  # pragma: no cover - pynvml is optional
    pynvml = None

NVIDIA_VENDOR_ID = "0x10de"  # Standard PCI vendor ID for NVIDIA


def _run_command(cmd: list[str]) -> str:
    """
    Run a command and return its stdout, or an empty string on any failure.

    :param cmd: The command and arguments to run
    :return: The command's stdout, stripped, or "" if it could not be run
    """
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return ""


def get_gpu_data_linux() -> list[dict[str, str | int] | None]:
    """
    Get GPU data on Linux.

    Tries NVIDIA via pynvml first, then falls back to generic lspci + DRM.

    :return: The list of GPU data, per GPU.
    """
    nvidia_data = _read_nvidia()
    if nvidia_data:
        return nvidia_data

    return _read_generic()


def _read_nvidia() -> list[dict[str, str | int] | None]:
    """
    Read GPU data from NVIDIA GPUs via the pynvml (NVML) bindings.

    Requires the proprietary NVIDIA driver and the ``nvidia-ml-py`` package.

    :return: The list of NVIDIA GPU data, or an empty list if unavailable
    """
    if pynvml is None:
        return []

    try:
        pynvml.nvmlInit()
    except pynvml.NVMLError:
        return []

    try:
        driver_version = cast(str, pynvml.nvmlSystemGetDriverVersion())
        device_count = pynvml.nvmlDeviceGetCount()

        results: list[dict[str, str | int]] = []
        for i in range(device_count):
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                name = cast(str, pynvml.nvmlDeviceGetName(handle))
                mem_info = cast(float, pynvml.nvmlDeviceGetMemoryInfo(handle).total)

                from textual_system_monitor.utilities import bytes_to_human

                results.append(
                    {
                        "gpu": name,
                        "driver_version": driver_version,
                        "resolution": _get_resolution(),
                        "adapter_ram": bytes_to_human(mem_info),
                        "availability": "Available",
                        "refresh": _get_refresh_rate(),
                        "status": "Ok",
                    }
                )
            except pynvml.NVMLError:
                continue

        return results
    finally:
        with contextlib.suppress(pynvml.NVMLError):
            pynvml.nvmlShutdown()


def _read_generic() -> list[dict[str, str | int] | None]:
    """
    Generic GPU fallback using lspci and DRM/KMS sysfs.

    Works for any graphics hardware with a kernel driver, though with limited
    detail (no VRAM, no utilization, etc.).

    :return: The list of generic GPU data, or an empty list if nothing found
    """
    results: list[dict[str, str | int]] = []

    # Try lspci to find VGA / 3D controllers
    lspci_output = _run_command(["lspci", "-nn"])
    for line in lspci_output.splitlines():
        if "VGA compatible controller" in line or "3D controller" in line:
            name = _parse_lspci_name(line)
            results.append(
                {
                    "gpu": name,
                    "driver_version": _get_driver_name(),
                    "resolution": _get_resolution(),
                    "adapter_ram": "N/A",
                    "availability": "Available",
                    "refresh": _get_refresh_rate(),
                    "status": "Ok",
                }
            )

    if results:
        return results

    # Last resort: check if any DRM cards exist at all
    drm_path = Path("/sys/class/drm")
    if drm_path.exists() and any(drm_path.glob("card*")):
        return [
            {
                "gpu": "Unknown GPU",
                "driver_version": "Unknown",
                "resolution": _get_resolution(),
                "adapter_ram": "N/A",
                "availability": "Available",
                "refresh": _get_refresh_rate(),
                "status": "Ok",
            }
        ]

    return []


def _parse_lspci_name(line: str) -> str:
    """
    Extract the human-readable GPU name from an lspci line.

    Example input:
        "00:02.0 VGA compatible controller: Intel Corporation UHD Graphics (rev 01)"
    Returns: "Intel Corporation UHD Graphics"

    :param line: A single line of lspci output
    :return: The GPU name portion
    """
    # Split off the PCI domain:bus.device prefix
    parts = line.split(":", maxsplit=2)
    if len(parts) < 3:
        return "Unknown GPU"

    # The remainder is " VGA compatible controller: Vendor Name [Model] (rev xx)"
    remainder = parts[2].strip()
    # Remove everything after " [" (the model in brackets)
    if " [" in remainder:
        remainder = remainder.split(" [", maxsplit=1)[0].strip()
    # Remove trailing "(rev xx)"
    if " (rev" in remainder:
        remainder = remainder.split(" (rev", maxsplit=1)[0].strip()

    return remainder or "Unknown GPU"


def _get_driver_name() -> str:
    """
    Get the kernel graphics driver name from lspci -k.

    :return: The driver name, or "Unknown" if it cannot be determined
    """
    output = _run_command(["lspci", "-k"])
    for line in output.splitlines():
        if "Kernel driver in use:" in line:
            return line.split(":", maxsplit=1)[1].strip()
    return "Unknown"


def _get_drm_resolution() -> str | None:
    """
    Try to read the current display resolution from DRM connector sysfs.

    :return: A resolution string like "1920x1080", or None if not found
    """
    drm_path = Path("/sys/class/drm")
    if not drm_path.exists():
        return None

    for card in sorted(drm_path.glob("card*")):
        for connector in sorted(card.glob("card*-*")):
            status_file = connector / "status"
            modes_file = connector / "modes"
            if status_file.exists() and modes_file.exists():
                try:
                    status = status_file.read_text(encoding="utf-8", errors="replace").strip()
                    if status == "connected":
                        modes = modes_file.read_text(encoding="utf-8", errors="replace").strip().splitlines()
                        if modes:
                            mode = modes[0].strip()
                            if " " in mode:
                                return mode.split()[0]
                            return mode
                except OSError:
                    continue

    return None


def _get_xrandr_resolution() -> str:
    """
    Try to read the current display resolution from xrandr.

    :return: A resolution string like "1920x1080", or "Unknown"
    """
    output = _run_command(["xrandr"])
    for line in output.splitlines():
        if "*" in line and "x" in line:
            parts = line.split()
            for part in parts:
                clean = part.replace("*", "").replace("+", "")
                if "x" in clean and any(c.isdigit() for c in clean):
                    return clean
            if parts:
                return parts[0].replace("*", "").replace("+", "")
    return "Unknown"


def _get_resolution() -> str:
    """
    Get the current display resolution.

    Reads DRM connector modes from sysfs first, then falls back to xrandr.

    :return: A resolution string like "1920x1080", or "Unknown"
    """
    drm_result = _get_drm_resolution()
    if drm_result is not None:
        return drm_result
    return _get_xrandr_resolution()


def _get_refresh_rate() -> str:
    """
    Get the current display refresh rate from xrandr.

    :return: A refresh rate string like "60.00", or "Unknown"
    """
    output = _run_command(["xrandr"])
    for line in output.splitlines():
        if "*" in line:
            parts = line.split()
            for part in parts:
                clean = part.replace("*", "").replace("+", "")
                try:
                    float(clean)
                    return clean
                except ValueError:
                    continue
    return "Unknown"
