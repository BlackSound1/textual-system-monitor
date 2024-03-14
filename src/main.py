from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static

from cpu import CPU_Usage
from drives import DriveUsage
from memory import MemUsage
from network import NetInfo
from processes import Processes


class Stats(Static):
    BORDER_TITLE = "Stats"

    def compose(self) -> ComposeResult:
        yield DriveUsage(id="drives")
        yield MemUsage(id="mem")
        yield CPU_Usage(id="cpu")
        yield NetInfo(id='network')
        # yield GPU_Usage(id="gpu")

    def on_mount(self) -> None:
        self.update("This will display all current usage stats")


class Monitor(App[str]):
    CSS_PATH = "css.tcss"
    TITLE = "Textual System Monitor"
    SUB_TITLE = "Written in Python using Textual"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    # TEST
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Container(id="app-grid"):
            yield Processes(id="processes")
            yield Stats(id="stats")

        yield Footer()


def run() -> None:
    Monitor().run()


if __name__ == '__main__':
    run()
