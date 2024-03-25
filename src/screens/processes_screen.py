from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Header, Footer


class ProcessesScreen(Screen):

    BINDINGS = [
        ("b", "app.switch_screen('main')", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("Processes Screen")
        yield Footer()
