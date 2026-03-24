from typing import cast

from textual import getters
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Label, Header, Footer, Digits

from src.utilities import get_mem_data, get_pallette, bytes_to_human, compute_percentage_color, COMMON_INTERVAL


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


class MemoryScreen(Screen[None]):
    BORDER_TITLE = f"Memory - Updated every {COMMON_INTERVAL}s"
    CSS_PATH = "../styles/mem_css.tcss"
    BINDINGS = [
        ("q", "app.quit", "Quit"),
        ("p", "app.switch_mode('processes')", "Processes"),
        ("c", "app.switch_mode('cpu')", "CPU"),
        ("n", "app.switch_mode('network')", "Network"),
        ("d", "app.switch_mode('drive')", "Drives"),
        ("m", "app.switch_mode('main')", "Main Screen"),
        ("v", "app.switch_mode('gpu')", "GPU"),
    ]

    update_timer: Timer | None = None

    mem_data = reactive(get_mem_data())

    container = getters.query_one("#mem-container", expect_type=Container)
    total_digits = getters.query_one("#total-digits", Digits)
    total_label = getters.query_one("#total-static-label", Label)
    avail_digits = getters.query_one("#avail-digits", Digits)
    avail_label = getters.query_one("#avail-static-label", Label)
    used_digits = getters.query_one("#used-digits", Digits)
    used_label = getters.query_one("#used-static-label", Label)
    perc_digits = getters.query_one("#perc-digits", Digits)

    def update_mem_data(self) -> None:
        """
        Update the memory information by calling `_get_mem_data`
        """
        self.mem_data = get_mem_data()

    def watch_mem_data(self, data: dict[str, int | float]) -> None:
        """
        Watch for changes in the memory data and update the Widgets accordingly

        :param data: The new memory data
        :return: None
        """

        from src.app import Monitor

        # Get KB size
        kb_size = cast(Monitor, self.app).CONTEXT['kb_size']

        # Update total information
        value, denom = bytes_to_human(data['total'], kb_size).split(' ')
        self.total_label.update(f"Total Memory ({denom}):  ")
        self.total_digits.update(f"{value}")

        # Update available information
        value, denom = bytes_to_human(data['available'], kb_size).split(' ')
        self.avail_label.update(f"Available Memory ({denom}):  ")
        self.avail_digits.update(f"{value}")

        # Update used information
        value, denom = bytes_to_human(data['used'], kb_size).split(' ')
        self.used_label.update(f"Used Memory ({denom}):  ")
        self.used_digits.update(f"{value}")

        # Update percentage information
        pct, color = compute_percentage_color(data['percent'], combine_output=False)
        perc_digits = reset_percentage_color(self.perc_digits)
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
                yield Label("", id="total-static-label", classes="label")
                yield Digits(id="total-digits", classes="digits")

            with Container(classes="mem-static"):
                yield Label("", id="avail-static-label", classes="label")
                yield Digits(id="avail-digits", classes="digits")

            with Container(classes="mem-static"):
                yield Label("", id="used-static-label", classes="label")
                yield Digits(id="used-digits", classes="digits")

            with Container(classes="mem-static"):
                yield Label("Percentage Used (%):  ", classes="label")
                yield Digits(id="perc-digits", classes="digits")

        yield Footer()

    def on_mount(self) -> None:
        """
        Perform initial setup for the Memory Screen
        """
        self.update_timer = self.set_interval(COMMON_INTERVAL, self.update_mem_data)
        self.container.border_title = self.BORDER_TITLE
        self.container.styles.border = ('round', get_pallette(self.app.theme)['yellow'])

        def _on_theme_change() -> None:
            """
            Update the border color based on the theme
            """
            self.container.styles.border = ('round', get_pallette(self.app.theme)['yellow'])

        self.watch(self.app, "theme", _on_theme_change, init=False)

    def on_unmount(self) -> None:
        """
        Kill the timer on unmount to avoid timer-related threading issues
        """
        if self.update_timer:
            self.update_timer.stop()
