from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Static

from ..utilities import NET_INTERVAL, bytes2human, get_network_stats


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

        Update the Network pane with new info for each network interface
        :param old: The list of old interface info to use
        :param new: The list of new interface info to use
        """

        # First, grab the Static Widget
        try:
            static = self.query_one("Static", expect_type=Static)
        except NoMatches():
            return

        static_content = ""

        # Next, go through each updated network interface, get its info, and update the Static widget
        # with the new info for each interface
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
            static_content += (f"[#F9F070]{interface}[/]: [#508CFC]Download[/]: {download} at "
                               f"{download_speed} /s | [#508CFC]Upload[/]: {upload} at {upload_speed} /s\n\n")

        # Update the content of the Static widget with the new info for all interfaces
        static.update(static_content)

    def on_mount(self) -> None:
        """
        Hook up the `update_io` function, set to an interval of 1 second
        :return: None
        """
        self.update_io = self.set_interval(NET_INTERVAL, self.update_io)

    def on_click(self) -> None:
        """
        When this pane is clicked, switch to the Network screen

        :return: None
        """

        self.app.switch_mode("network")

    def compose(self) -> ComposeResult:
        """
        Start off with a simple VerticalScroll Widget with a Static attached
        :return: The ComposeResult featuring the VerticalScroll and Static
        """
        with VerticalScroll():
            yield Static("")
