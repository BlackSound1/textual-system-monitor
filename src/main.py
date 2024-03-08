from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Header, Footer, Static
from psutil import cpu_count, cpu_percent

from utilities import compute_percentage_color


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

    cores = cpu_count()
    percents = reactive([0.0])
    percent_overall = reactive(0.0)  # TODO: Add overall CPU percentage display functionality

    def update_cpu_stats(self) -> None:
        # self.percents = cpu_percent()
        self.percents: list = cpu_percent(percpu=True)
        self.percents_overall: float = cpu_percent()

    def _display_percentages_CPU(self, percentages: list) -> str:
        string = "\n"

        for i, pct in enumerate(percentages):
            pct = compute_percentage_color(pct)

            string += f"Core {i + 1}: {pct}" if i == 0 else f" Core {i + 1}: {pct}"

        return string

    def watch_percents(self, percentages: list) -> None:
        """
        Watch what heppens when the percents variable is changed and react accordingly.

        :param percentages: The list of percentages
        :return: None
        """

        percentage_string = self._display_percentages_CPU(percentages)
        self.update(f"Cores: {self.cores},\nPercents: {percentage_string}")

    def on_mount(self) -> None:
        self.update_cpu = self.set_interval(1 / 5, self.update_cpu_stats, pause=False)


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
