from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Header, Footer, Static, Label


class Processes(Static):
    BORDER_TITLE = "Processes"

    def on_mount(self) -> None:
        self.update("This will display current processes")


class Temp(Static):
    BORDER_TITLE = "Temperature"

    def on_mount(self) -> None:
        self.update("This will display current system temperatures")


class MemUsage(Static):
    BORDER_TITLE = "Memory Usage"

    def on_mount(self) -> None:
        self.update("This will display current memory usage")


class CPU_Usage(Static):
    BORDER_TITLE = "CPU Usage"

    def on_mount(self) -> None:
        self.update("This will display current CPU usage")


class GPU_Usage(Static):
    BORDER_TITLE = "GPU Usage"

    def on_mount(self) -> None:
        self.update("This will display current GPU usage")


class Stats(Static):
    BORDER_TITLE = "Stats"

    def compose(self) -> ComposeResult:
        yield Temp(id="temp")
        yield DriveUsage(id="drives")
        yield MemUsage(id="mem")
        yield CPU_Usage(id="cpu")
        yield GPU_Usage(id="gpu")

    def on_mount(self) -> None:
        self.update("This will display all current usage stats")


class DriveUsage(Static):
    BORDER_TITLE = "Drive Usage"

    def on_mount(self) -> None:
        self.update("This will display current drive usage")


class Monitor(App[str]):
    CSS_PATH = "css.tcss"
    TITLE = "Textual System Monitor"
    SUB_TITLE = "Written in Python using Textual"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Container(id="app-grid"):
            yield Processes(id="processes")

            yield Stats(id="stats")
            # with Container(id="right"):
            #     yield Temp(id="temps")
            #     yield Stats(id="stats")
            # yield Usage(id="usages")

        yield Footer()


def run() -> None:
    Monitor().run()


if __name__ == '__main__':
    run()
