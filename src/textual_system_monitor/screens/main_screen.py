import logging
from typing import ClassVar

from textual import getters
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.logging import TextualHandler
from textual.screen import Screen
from textual.widgets import Footer, Header

from textual_system_monitor.utilities import get_palette

from ..panes.processes import Processes
from ..panes.stats import Stats

logging.basicConfig(handlers=[TextualHandler()], level=logging.WARNING)


class MainScreen(Screen[None]):
    CSS_PATH = "../styles/main_css.tcss"
    BINDINGS: ClassVar = [
        Binding(key="q", action="app.quit", description="Quit"),
        Binding(key="p", action="app.switch_screen('processes')", description="Processes"),
        Binding(key="c", action="app.switch_screen('cpu')", description="CPU"),
        Binding(key="n", action="app.switch_screen('network')", description="Network"),
        Binding(key="d", action="app.switch_screen('drive')", description="Drives"),
        Binding(key="m", action="app.switch_screen('mem')", description="Memory"),
        Binding(key="v", action="app.switch_screen('gpu')", description="GPU"),
        Binding(key="g", action="app.switch_screen('guide')", description="Guide"),
    ]

    processes = getters.query_one("#processes", expect_type=Processes)

    def on_mount(self) -> None:
        """
        Perform initial setup for the Main Screen
        """
        self.processes.styles.border = ("round", get_palette(self.app.theme)["orange"])

        def _on_theme_change() -> None:
            """
            Update the border color based on the theme
            """
            self.processes.styles.border = ("round", get_palette(self.app.theme)["orange"])

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
