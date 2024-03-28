from textual.app import ComposeResult
from textual.containers import VerticalScroll, Container
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Static, Header, Footer

from src.utilities import get_mem_data, bytes2human, compute_percentage_color, COMMON_INTERVAL


class MemoryScreen(Screen):
    BORDER_TITLE = "Memory"
    CSS_PATH = "../styles/mem_css.tcss"
    BINDINGS = [("m", "switch_mode('main')", "Main Screen")]

    mem_data = reactive(get_mem_data())

    def update_mem_data(self) -> None:
        """
        Update the memory information by calling `_get_mem_data`

        :return: None
        """
        self.mem_data = get_mem_data()

    def watch_mem_data(self, data: dict) -> None:
        """
        Watch for changes in the memory data and update the Static widget accordingly

        :param data: The new memory data
        :return: None
        """

        try:
            static = self.query_one("Static", Static)
        except NoMatches():
            return

        static.update(f"Total Memory: {bytes2human(data['total'])}\n\n"
                      f"Available Memory: {bytes2human(data['available'])}\n\n"
                      f"Used: {bytes2human(data['used'])}\n\n"
                      f"Percentage Used: {compute_percentage_color(data['percent'])}%")

    def compose(self) -> ComposeResult:
        """
        Display the structure of the Memory Screen

        :return: The ComposeResult
        """

        yield Header(show_clock=True)
        with Container(id="mem-container"):
            with VerticalScroll():
                yield Static(id="mem-static")
        yield Footer()

    def on_mount(self) -> None:
        """
        Perform initial setup for the Memory Screen
        :return: None
        """

        self.update_mem_data = self.set_interval(COMMON_INTERVAL, self.update_mem_data)

        try:
            container = self.query_one("#mem-container", expect_type=Container)
        except NoMatches():
            return

        container.border_title = self.BORDER_TITLE
