from textual.app import ComposeResult
from textual.containers import VerticalScroll, Container
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Static, Header, Footer

from src.utilities import NET_INTERVAL, get_network_stats, update_network_static


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

        Update the Network pane with new info for each network interface
        :param old: The list of old interface info to use
        :param new: The list of new interface info to use
        """

        # First, grab the Static Widget
        try:
            static = self.query_one("#network-screen-static", expect_type=Static)
        except NoMatches():
            return

        # Next, go through each updated network interface, get its info, and update the Static widget
        # with the new info for each interface
        static_content = update_network_static(new, old)

        # Update the content of the Static widget with the new info for all interfaces
        static.update(static_content)

    def on_mount(self) -> None:
        """
        Perform initial setup for the Network Screen
        :return: None
        """

        self.update_io = self.set_interval(NET_INTERVAL, self.update_io)

        try:
            container = self.query_one("#network-container", expect_type=Container)
        except NoMatches():
            return

        container.border_title = self.BORDER_TITLE

    def compose(self) -> ComposeResult:
        """
        Display the structure of the Network Screen
        :return: The ComposeResult featuring the structure of the Screen
        """

        yield Header(show_clock=True)
        with Container(id="network-container"):
            with VerticalScroll():
                yield Static("", id="network-screen-static")
        yield Footer()
