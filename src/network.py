from psutil import net_io_counters
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import Static

from utilities import NET_INTERVAL, bytes2human


class NetInfo(Static):
    BORDER_TITLE = "Network Info"

    io = reactive(net_io_counters(pernic=True))

    def update_io(self) -> None:
        self.io = net_io_counters(pernic=True)

    def watch_io(self, io_old: dict, io_new: dict) -> None:
        # First, grab the VerticalScroll Widget and clear it
        scroll = self.query_one("VerticalScroll", expect_type=VerticalScroll)
        scroll.remove_children()

        # Next, go through each updated network interface, get its info, and populate the VerticalScroll
        # Widget with a new Static for each interface
        for interface, interface_io in io_old.items():
            download = bytes2human(io_new[interface].bytes_recv)
            upload = bytes2human(io_new[interface].bytes_sent)

            upload_speed = bytes2human(
                round(
                    (io_new[interface].bytes_sent - interface_io.bytes_sent) / NET_INTERVAL,
                    2
                )
            )
            download_speed = bytes2human(
                round(
                    (io_new[interface].bytes_recv - interface_io.bytes_recv) / NET_INTERVAL,
                    2
                )
            )

            new_static = Static(f"[yellow]{interface}[/yellow]: Download: {download} at "
                                f"{download_speed} \\s | Upload: {upload} at {upload_speed} \\s\n")

            scroll.mount(new_static)

    def on_mount(self) -> None:
        self.update_io = self.set_interval(NET_INTERVAL, self.update_io)

    def compose(self) -> ComposeResult:
        yield VerticalScroll()
