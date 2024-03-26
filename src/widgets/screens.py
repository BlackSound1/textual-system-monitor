from textual.app import ComposeResult
from textual.widgets import Static


class Screens(Static):

    def compose(self) -> ComposeResult:
        for screen in self.app.screen_stack:
            yield Static(f"{screen}")
