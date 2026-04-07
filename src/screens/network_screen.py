from typing import Any, cast

from textual import getters
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll, Container
from textual.reactive import reactive
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Header, Footer, DataTable

from src.utilities import NET_INTERVAL, get_network_stats, bytes_to_human, get_palette


type NetworkStatsType = list[dict[str, str | int]]


class NetworkScreen(Screen[None]):

    BORDER_TITLE = f"Network - Updated every {NET_INTERVAL}s"
    CSS_PATH = "../styles/network_css.tcss"
    BINDINGS = [
        Binding(key="q", action="app.quit", description="Quit"),
        Binding(key="p", action="app.switch_screen('processes')", description="Processes"),
        Binding(key="c", action="app.switch_screen('cpu')", description="CPU"),
        Binding(key="n", action="app.switch_screen('main')", description="Main Screen"),
        Binding(key="d", action="app.switch_screen('drive')", description="Drives"),
        Binding(key="m", action="app.switch_screen('mem')", description="Memory"),
        Binding(key="v", action="app.switch_screen('gpu')", description="GPU"),
    ]

    update_timer: Timer

    io = reactive(get_network_stats())

    container = getters.query_one("#network-container", expect_type=Container)
    table = cast(DataTable[Any], getters.query_one("#network-screen-table", expect_type=DataTable))

    def update_io(self) -> None:
        """
        Define how to update `self.io`
        """
        self.io = get_network_stats()

    def watch_io(self, old_stats: NetworkStatsType, new_stats: NetworkStatsType) -> None:
        """
        Define what happens when `self.io` changes.

        Update the Network Screen with new info for each network interface

        :param old_stats: The list of old interface info to use
        :param new_stats: The list of new interface info to use
        """

        from src.app import Monitor

        kb_size = cast(Monitor, self.app).CONTEXT['kb_size']

        # Clear the table and add the columns
        self.table.clear(columns=True)
        self.table.add_columns("Interface", "Download", "Download Speed (/s)", "Upload", "Upload Speed (/s)")

        # Next, go through each updated network interface, get its info, and update the DataTable
        # with the new info for each interface
        for old_stat, new_stat in zip(old_stats, new_stats, strict=True):
            interface = old_stat["interface"]
            new_bytes_sent = cast(int, new_stat["bytes_sent"])
            old_bytes_sent = cast(int, old_stat["bytes_sent"])
            new_bytes_recv = cast(int, new_stat["bytes_recv"])
            old_bytes_recv = cast(int, old_stat["bytes_recv"])

            download = bytes_to_human(new_bytes_recv, kb_size)
            upload = bytes_to_human(new_bytes_sent, kb_size)
            upload_speed = bytes_to_human(
                round((new_bytes_sent - old_bytes_sent) / NET_INTERVAL, 2),
                kb_size,
            )
            download_speed = bytes_to_human(
                round((new_bytes_recv - old_bytes_recv) / NET_INTERVAL, 2),
                kb_size,
            )

            self.table.add_row(f"[green]{interface}[/]", download, download_speed, upload, upload_speed)

    def on_mount(self) -> None:
        """
        Perform initial setup for the Network Screen
        """
        self.update_timer = self.set_interval(NET_INTERVAL, self.update_io)
        self.container.border_title = self.BORDER_TITLE
        self.container.styles.border = ('round', get_palette(self.app.theme)['green'])

        def _on_theme_change() -> None:
            """
            Update the border color based on the theme
            """
            self.container.styles.border = ('round', get_palette(self.app.theme)['green'])

        self.watch(self.app, "theme", _on_theme_change, init=False)

    def on_unmount(self) -> None:
        """
        Kill the timer on unmount to avoid timer-related threading issues
        """
        if self.update_timer:
            self.update_timer.stop()

    def compose(self) -> ComposeResult:
        """
        Display the structure of the Network Screen

        :return: The ComposeResult featuring the structure of the Network Screen
        """
        # ruff: disable[SIM117]
        yield Header(show_clock=True)
        with Container(id="network-container"):
            with VerticalScroll():
                yield DataTable(id="network-screen-table", show_cursor=False, zebra_stripes=True)
        yield Footer()
