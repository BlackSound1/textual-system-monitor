import logging

from textual import getters
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Header, Footer
from textual.logging import TextualHandler

from src.utilities import get_palette

from ..panes.processes import Processes
from ..panes.stats import Stats

logging.basicConfig(handlers=[TextualHandler()], level=logging.WARNING)


class MainScreen(Screen[None]):
    CSS_PATH = "../styles/main_css.tcss"
    BINDINGS = [
        ("q", "app.quit", "Quit"),
        ("p", "app.switch_screen('processes')", "Processes"),
        ("c", "app.switch_screen('cpu')", "CPU"),
        ("n", "app.switch_screen('network')", "Network"),
        ("d", "app.switch_screen('drive')", "Drives"),
        ("m", "app.switch_screen('mem')", "Memory"),
        ("v", "app.switch_screen('gpu')", "GPU"),
        ('g', "app.switch_screen('guide')", 'Guide'),
    ]

    processes = getters.query_one("#processes", expect_type=Processes)

    def on_mount(self) -> None:
        """
        Perform initial setup for the Main Screen
        """
        self.processes.styles.border = ('round', get_palette(self.app.theme)['orange'])

        def _on_theme_change() -> None:
            """
            Update the border color based on the theme
            """
            self.processes.styles.border = ('round', get_palette(self.app.theme)['orange'])

        self.watch(self.app, "theme", _on_theme_change, init=False)

    def compose(self) -> ComposeResult:
        """
        Generates the layout for the main screen.

        :return: ComposeResult: The composed result of the application screen.
        """
        yield Header(show_clock=True)
        with Container(id="app-grid"):
            yield Processes(id="processes")
            yield Stats(id="stats")
        yield Footer()
