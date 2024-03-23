from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Header, Footer

from processes import Processes
from stats import Stats


class MainScreen(Screen):
    CSS_PATH = "styles/main_css.tcss"

    def compose(self) -> ComposeResult:
        """
        Composes and returns a ComposeResult object.

        This function generates the layout for the main screen. It starts by yielding a Header widget with the show_clock parameter set to True. Then, it creates a Container with the id "app-grid" and yields two child widgets: Processes with the id "processes" and Stats with the id "stats". Finally, it yields a Footer widget.

        :return: ComposeResult: The composed result of the application screen.
        """
        yield Header(show_clock=True)

        with Container(id="app-grid"):
            yield Processes(id="processes")
            yield Stats(id="stats")

        yield Footer()
