from textual.app import ComposeResult
from textual.containers import VerticalScroll, Container
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable

from src.utilities import NET_INTERVAL, get_network_stats, bytes_to_human


class NetworkScreen(Screen):

    BORDER_TITLE = f"Network - Updated every {NET_INTERVAL}s"
    CSS_PATH = "../styles/network_css.tcss"
    BINDINGS = [
        ("q", "app.quit", "Quit"),
        ("t", "app.toggle_dark", "Toggle dark mode"),
        ("p", "app.switch_mode('processes')", "Processes"),
        ("c", "app.switch_mode('cpu')", "CPU"),
        ("n", "app.switch_mode('main')", "Main Screen"),
        ("d", "app.switch_mode('drive')", "Drives"),
        ("m", "app.switch_mode('mem')", "Memory"),
        ("v", "app.switch_mode('gpu')", "GPU"),
        ('/', 'app.switch_base', 'Change KB Size')
    ]

    io = reactive(get_network_stats())

    def update_io(self) -> None:
        """
        Define how to update `self.io`
        """
        self.io = get_network_stats()

    def watch_io(self, old_stats: list, new_stats: list) -> None:
        """
        Define what happens when `self.io` changes.

        Update the Network Screen with new info for each network interface
        :param old_stats: The list of old interface info to use
        :param new_stats: The list of new interface info to use
        """

        # First, grab the DataTable Widget
        try:
            table = self.query_one("#network-screen-table", expect_type=DataTable)
        except NoMatches:
            return

        # Get KB size
        kb_size = self.app.CONTEXT['kb_size']

        # Clear the table and add the columns
        table.clear(columns=True)
        table.add_columns("Interface", "Download", "Download Speed (/s)", "Upload", "Upload Speed (/s)")

        # Next, go through each updated network interface, get its info, and update the DataTable
        # with the new info for each interface
        for old_stat, new_stat in zip(old_stats, new_stats):
            interface = old_stat["interface"]
            download = bytes_to_human(new_stat["bytes_recv"], kb_size)
            upload = bytes_to_human(new_stat["bytes_sent"], kb_size)
            upload_speed = bytes_to_human(
                round((new_stat["bytes_sent"] - old_stat["bytes_sent"]) / NET_INTERVAL, 2),
                kb_size
            )
            download_speed = bytes_to_human(
                round((new_stat["bytes_recv"] - old_stat["bytes_recv"]) / NET_INTERVAL, 2),
                kb_size
            )

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
