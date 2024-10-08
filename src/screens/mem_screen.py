from textual.app import ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Static, Header, Footer, Digits

from src.utilities import get_mem_data, bytes_to_human, compute_percentage_color, COMMON_INTERVAL


def reset_percentage_color(digits: Digits) -> Digits:
    """
    Reset the color classes of the Digits widget

    :param digits: The Digits widget to reset color classes for
    :return: The updated Digits widget
    """

    digits.remove_class("green")
    digits.remove_class("yellow")
    digits.remove_class("red")

    return digits


class MemoryScreen(Screen):
    BORDER_TITLE = f"Memory - Updated every {COMMON_INTERVAL}s"
    CSS_PATH = "../styles/mem_css.tcss"
    BINDINGS = [
        ("q", "app.quit", "Quit"),
        ("t", "app.toggle_dark", "Toggle dark mode"),
        ("p", "app.switch_mode('processes')", "Processes"),
        ("c", "app.switch_mode('cpu')", "CPU"),
        ("n", "app.switch_mode('network')", "Network"),
        ("d", "app.switch_mode('drive')", "Drives"),
        ("m", "app.switch_mode('main')", "Main Screen"),
        ("v", "app.switch_mode('gpu')", "GPU"),
        ('/', 'app.switch_base', 'Change KB Size')
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
        Watch for changes in the memory data and update the Widgets accordingly

        :param data: The new memory data
        :return: None
        """

        try:
            total_digits = self.query_one("#total-digits", Digits)
            total_label = self.query_one("#total-static-label", Static)
            avail_digits = self.query_one("#avail-digits", Digits)
            avail_label = self.query_one("#avail-static-label", Static)
            used_digits = self.query_one("#used-digits", Digits)
            used_label = self.query_one("#used-static-label", Static)
            perc_digits = self.query_one("#perc-digits", Digits)
        except NoMatches:
            return

        # Get KB size
        kb_size = self.app.CONTEXT['kb_size']

        # Update total information
        value, denom = bytes_to_human(data['total'], kb_size).split(' ')
        total_label.update(f"Total Memory ({denom}):\t")
        total_digits.update(f"{value}")

        # Update available information
        value, denom = bytes_to_human(data['available'], kb_size).split(' ')
        avail_label.update(f"Available Memory ({denom}):\t")
        avail_digits.update(f"{value}")

        # Update used information
        value, denom = bytes_to_human(data['used'], kb_size).split(' ')
        used_label.update(f"Used Memory ({denom}):\t")
        used_digits.update(f"{value}")

        # Update percentage information
        pct, color = compute_percentage_color(data['percent'], combine_output=False)
        perc_digits = reset_percentage_color(perc_digits)
        perc_digits.add_class(color)
        perc_digits.update(f"{pct}")

    def compose(self) -> ComposeResult:
        """
        Display the structure of the Memory Screen

        :return: The ComposeResult
        """

        yield Header(show_clock=True)

        with Container(id="mem-container"):
            with Container(classes="mem-static"):
                yield Static("", id="total-static-label", classes="label")
                yield Digits(id="total-digits", classes="digits")

            with Container(classes="mem-static"):
                yield Static("", id="avail-static-label", classes="label")
                yield Digits(id="avail-digits", classes="digits")

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
