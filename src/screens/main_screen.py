import logging

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Header, Footer
from textual.logging import TextualHandler

from ..panes.processes import Processes
from ..panes.stats import Stats

logging.basicConfig(handlers=[TextualHandler()], level=logging.WARNING)


class MainScreen(Screen):
    CSS_PATH = "../styles/main_css.tcss"
    BINDINGS = [
        ('g', "switch_mode('guide')", 'Guide')
    ]

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
