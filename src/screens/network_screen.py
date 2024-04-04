from textual.app import ComposeResult
from textual.containers import VerticalScroll, Container
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable

from src.utilities import NET_INTERVAL, get_network_stats, bytes2human


class NetworkScreen(Screen):

    BORDER_TITLE = "Network"
    CSS_PATH = "../styles/network_css.tcss"
    BINDINGS = [
        ("n", "switch_mode('main')", "Main Screen"),
    ]

    io = reactive(get_network_stats())

    def update_io(self) -> None:
        """
        Define how to update `self.io`
        """
        self.io = get_network_stats()

    def watch_io(self, old: list, new: list) -> None:
        """
        Define what happens when `self.io` changes.

        Update the Network Screen with new info for each network interface
        :param old: The list of old interface info to use
        :param new: The list of new interface info to use
        """

        # First, grab the DataTable Widget
        try:
            table = self.query_one("#network-screen-table", expect_type=DataTable)
        except NoMatches:
            return

        # Clear the table and add the columns
        table.clear(columns=True)
        table.add_columns("Interface", "Download", "Download Speed (/s)", "Upload", "Upload Speed (/s)")

        # Next, go through each updated network interface, get its info, and update the DataTable
        # with the new info for each interface
        for i, item in enumerate(old):
            interface = item["interface"]
            download = bytes2human(new[i]["bytes_recv"])
            upload = bytes2human(new[i]["bytes_sent"])
            upload_speed = bytes2human(round((new[i]["bytes_sent"] - item["bytes_sent"]) / NET_INTERVAL, 2))
            download_speed = bytes2human(round((new[i]["bytes_recv"] - item["bytes_recv"]) / NET_INTERVAL, 2))

            table.add_row(f"[green]{interface}[/]", download, download_speed, upload, upload_speed)

    def on_mount(self) -> None:
        """
        Perform initial setup for the Network Screen
        :return: None
        """

        self.update_io = self.set_interval(NET_INTERVAL, self.update_io)

        try:
            container = self.query_one("#network-container", expect_type=Container)
        except NoMatches:
            return

        container.border_title = self.BORDER_TITLE

    def compose(self) -> ComposeResult:
        """
        Display the structure of the Network Screen
        :return: The ComposeResult featuring the structure of the Network Screen
        """

        yield Header(show_clock=True)
        with Container(id="network-container"):
            with VerticalScroll():
                yield DataTable(id="network-screen-table", show_cursor=False, zebra_stripes=True)
        yield Footer()
