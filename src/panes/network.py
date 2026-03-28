from typing import cast

from textual import getters
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.timer import Timer
from textual.widgets import Static

from ..utilities import NET_INTERVAL, get_network_stats, get_palette, update_network_static

type NetworkStatsType = list[dict[str, str | int]]


class NetInfo(Static):
    BORDER_TITLE = f"Network Info - Updated every {NET_INTERVAL}s"

    update_timer: Timer

    io = reactive(get_network_stats())

    static = getters.query_one("#network_pane_static", expect_type=Static)

    def update_io(self) -> None:
        """
        Define how to update `self.io`
        """
        self.io = get_network_stats()

    def watch_io(self, old: NetworkStatsType, new: NetworkStatsType) -> None:
        """
        Define what happens when `self.io` changes.

        Update the Network pane with new info for each network interface

        :param old: The list of old interface info to use
        :param new: The list of new interface info to use
        """

        from src.app import Monitor  # Need to import here to avoid circular import

        kb_size = cast(Monitor, self.app).CONTEXT['kb_size']

        palette = get_palette(self.app.theme)

        # Go through each updated network interface, get its info, and update the Static widget
        # with the new info for each interface
        static_content = update_network_static(new, old, kb_size, palette)

        # Update the content of the Static widget with the new info for all interfaces
        self.static.update(static_content)

    def on_mount(self) -> None:
        """
        Hook up the `update_io` function, set to an interval of 1 second
        """
        self.update_timer = self.set_interval(NET_INTERVAL, self.update_io)

    def on_unmount(self) -> None:
        """
        Kill the timer on unmount to avoid timer-related threading issues
        """
        if self.update_timer:
            self.update_timer.stop()

    def on_click(self) -> None:
        """
        When this pane is clicked, switch to the Network screen
        """
        self.app.switch_screen("network")

    def compose(self) -> ComposeResult:
        """
        Start off with a simple VerticalScroll Widget with a Static attached

        :return: The ComposeResult featuring the VerticalScroll and Static
        """
        with VerticalScroll():
            yield Static("", id="network_pane_static")
