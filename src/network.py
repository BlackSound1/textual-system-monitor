from typing import List

from psutil import net_io_counters
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import Static

from utilities import NET_INTERVAL, bytes2human


def get_network_stats() -> List[dict]:
    """
    Utility function to get network statistics, per interface.

    :return: A list of dicts, each one containing the network statistics for a single interface. Sorted
             by highest download amount
    """

    stats = []

    # Go through each interface and its accompanying stats. Get the interface name and upload/ download info.
    # Append this as a dict to the stats list
    for interface, interface_io in net_io_counters(pernic=True).items():
        interface_dict = {
            "interface": interface,
            "bytes_sent": interface_io.bytes_sent,
            "bytes_recv": interface_io.bytes_recv
        }

        stats.append(interface_dict)

    # Sort by highest download amount
    stats = sorted(stats, key=lambda x: x['bytes_recv'], reverse=True)

    return stats


class NetInfo(Static):
    BORDER_TITLE = "Network Info"

    io = reactive(get_network_stats())

    def update_io(self) -> None:
        """
        Define how to update `self.io`
        """
        self.io = get_network_stats()

    def watch_io(self, old: list, new: list) -> None:
        """
        Define what happens when `self.io` changes.

        Update the Network pane with Statics for each network interface
        :param old: The list of old interface info to use
        :param new: The list of new interface info to use
        """

        # First, grab the VerticalScroll Widget and clear it
        scroll = self.query_one("VerticalScroll", expect_type=VerticalScroll)
        scroll.remove_children()

        # Next, go through each updated network interface, get its info, and populate the VerticalScroll
        # Widget with a new Static for each interface
        for i, item in enumerate(old):
            interface = item.get("interface")
            download = bytes2human(new[i]["bytes_recv"])
            upload = bytes2human(new[i]["bytes_sent"])
            upload_speed = bytes2human(
                round(
                    (new[i]["bytes_sent"] - item.get("bytes_sent")) / NET_INTERVAL,
                    2
                )
            )
            download_speed = bytes2human(
                round(
                    (new[i]["bytes_recv"] - item.get("bytes_recv")) / NET_INTERVAL,
                    2
                )
            )

            new_static = Static(f"[#F9F070]{interface}[/]: [#508CFC]Download[/]: {download} at "
                                f"{download_speed} /s | [#508CFC]Upload[/]: {upload} at {upload_speed} /s\n")

            scroll.mount(new_static)

    def on_mount(self) -> None:
        """
        Hook up the `update_io` function, set to an interval of 1 second
        :return: None
        """
        self.update_io = self.set_interval(NET_INTERVAL, self.update_io)

    def compose(self) -> ComposeResult:
        """
        Start off with a simple VerticalScroll Widget
        :return: The ComposeResult featuring the VerticalScroll
        """
        yield VerticalScroll()
