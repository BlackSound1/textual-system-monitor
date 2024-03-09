from typing import List

from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Header, Footer, Static, ListView, ListItem
from psutil import cpu_count, cpu_percent, virtual_memory, disk_partitions, disk_usage, process_iter

from utilities import compute_percentage_color, INTERVAL


class Processes(Static):
    BORDER_TITLE = "Processes"

    processes = process_iter(['pid', 'name', 'username', 'exe'])

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            for process in self.processes:
                name = 'N/A' if process.info.get('name') == '' else process.info.get('name')
                exe = 'N/A' if process.info.get('exe') == '' else process.info.get('exe')

                yield Static(f"PID: {process.info.get('pid')}, Name: {name},"
                             f" Username: {process.info.get('username')}, EXE: {exe}\n")


    # def on_mount(self) -> None:
    #     self.update("This will display current processes")


class MemUsage(Static):
    BORDER_TITLE = "Memory Usage"

    total = virtual_memory().total
    available = reactive(0)
    percent = reactive(0.0)

    def update_available(self) -> None:
        self.available = virtual_memory().available

    def watch_available(self, avail: float) -> None:
        pct = compute_percentage_color(self.percent)
        self.update(f"Total memory: {self.total} B\nAvailable memory: {avail} B\nPercentage: {pct}%")

    def update_percent(self) -> None:
        self.percent = virtual_memory().percent

    def watch_percent(self, pct: float) -> None:
        pct = compute_percentage_color(pct)
        self.update(f"Total memory: {self.total} B\nAvailable memory: {self.available} B\nPercentage: {pct}%")

    def on_mount(self) -> None:
        self.update_available = self.set_interval(INTERVAL, self.update_available)
        self.update_percent = self.set_interval(INTERVAL, self.update_percent)


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
        Watch what happens when the percents variable is changed and react accordingly.

        :param percentages: The list of percentages
        :return: None
        """

        percentage_string = self._display_percentages_CPU(percentages)
        self.update(f"Cores: {self.cores},\nPercents: {percentage_string}")

    def on_mount(self) -> None:
        self.update_cpu = self.set_interval(INTERVAL, self.update_cpu_stats)


class GPU_Usage(Static):
    BORDER_TITLE = "GPU Usage"

    def on_mount(self) -> None:
        self.update("This will display current GPU usage")


class DriveUsage(Static):
    BORDER_TITLE = "Drive Usage"

    disks: List[dict] = [{"device": item.device, "mountpoint": item.mountpoint, "fstype": item.fstype,
                          "opts": item.opts, "maxfile": item.maxfile, "maxpath": item.maxpath}
                         for item in disk_partitions()]

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            for item in self.disks:
                try:
                    usage = disk_usage(item.get('mountpoint'))
                    pct = usage.percent
                    used = usage.used
                    free = usage.free
                    total = usage.total
                except PermissionError:
                    pct = "N/A"
                    used = "N/A"
                    free = "N/A"
                    total = "N/A"

                fs = "N/A" if item.get('fstype') == '' else item.get('fstype')

                yield Static(f"Disk: {item.get('device')} | Options: {item.get('opts')} |"
                             f" Filesystem: {fs} | Usage: {pct}% | Total: {total} | "
                             f"Used: {used} | Free: {free}\n")

    # def on_mount(self) -> None:
    #
    #     self.update(f"{self.stuff[0]}")
    #     # for part in self.stuff:
    #     #     self.update(f"{part}")


class Stats(Static):
    BORDER_TITLE = "Stats"

    def compose(self) -> ComposeResult:
        yield DriveUsage(id="drives")
        yield MemUsage(id="mem")
        yield CPU_Usage(id="cpu")
        yield GPU_Usage(id="gpu")

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
