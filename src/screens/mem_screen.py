from textual.app import ComposeResult
from textual.containers import Container
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
            total = self.query_one("#total-static", Static)
            avail = self.query_one("#avail-static", Static)
            used = self.query_one("#used-static", Static)
            perc = self.query_one("#perc-static", Static)
        except NoMatches:
            return

        total.update(f"Total Memory: {bytes2human(data['total'])}")
        avail.update(f"Available Memory: {bytes2human(data['available'])}")
        used.update(f"Used: {bytes2human(data['used'])}")
        perc.update(f"Percentage Used: {compute_percentage_color(data['percent'])} %")

    def compose(self) -> ComposeResult:
        """
        Display the structure of the Memory Screen

        :return: The ComposeResult
        """

        yield Header(show_clock=True)
        with Container(id="mem-container"):
            yield Static(id="total-static", classes="mem-static")
            yield Static(id="avail-static", classes="mem-static")
            yield Static(id="used-static", classes="mem-static")
            yield Static(id="perc-static", classes="mem-static")
        yield Footer()

    def on_mount(self) -> None:
        """
        Perform initial setup for the Memory Screen
        :return: None
        """

        self.update_mem_data = self.set_interval(COMMON_INTERVAL, self.update_mem_data)

        try:
            container = self.query_one("#mem-container", expect_type=Container)
        except NoMatches:
            return

        container.border_title = self.BORDER_TITLE
