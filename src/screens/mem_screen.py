from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Static, Header, Footer, Digits

from src.utilities import get_mem_data, bytes2human, compute_percentage_color, COMMON_INTERVAL


def reset_percentage_color(digits: Digits) -> Digits:
    """
    Reset the percentage color

    :param digits: The Digits widget
    :return: None
    """

    digits.remove_class("green")
    digits.remove_class("yellow")
    digits.remove_class("red")

    return digits


class MemoryScreen(Screen):
    BORDER_TITLE = "Memory"
    CSS_PATH = "../styles/mem_css.tcss"
    BINDINGS = [
        Binding("m", "switch_mode('main')", "Main Screen", priority=True),
    ]

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
            used = self.query_one("#used-digits", Digits)
            used_label = self.query_one("#used-static-label", Static)
            perc = self.query_one("#perc-digits", Digits)
        except NoMatches:
            return

        pct, color = compute_percentage_color(data['percent'], combine_output=False)

        total.update(f"Total Memory: {bytes2human(data['total'])}")
        avail.update(f"Available Memory: {bytes2human(data['available'])}")

        # Update used information
        value, denom = bytes2human(data['total']).split(' ')
        used_label.update(f"Used ({denom}):\t")
        used.update(f"{value}")

        # Update percentage information
        perc = reset_percentage_color(perc)
        perc.add_class(color)
        perc.update(f"{pct}")

    def compose(self) -> ComposeResult:
        """
        Display the structure of the Memory Screen

        :return: The ComposeResult
        """

        yield Header(show_clock=True)
        with Container(id="mem-container"):
            yield Static(id="total-static", classes="mem-static")
            yield Static(id="avail-static", classes="mem-static")
            with Container(classes="mem-static"):
                yield Static("", id="used-static-label", classes="label")
                yield Digits(id="used-digits", classes="digits")
            with Container(classes="mem-static"):
                yield Static("Percentage Used (%):\t", classes="label")
                yield Digits(id="perc-digits", classes="digits")
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
