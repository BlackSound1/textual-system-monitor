from typing import List

from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Header, Footer, Static, ListView, ListItem
from psutil import cpu_count, cpu_percent, virtual_memory, disk_partitions, disk_usage, process_iter, net_connections

from utilities import compute_percentage_color, INTERVAL, bytes2human


class Processes(Static):
    BORDER_TITLE = "Processes"

    processes = process_iter(['pid', 'name', 'username', 'exe'])

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            for process in self.processes:
                name = 'N/A' if process.info.get('name') == '' else process.info.get('name')
                exe = 'N/A' if process.info.get('exe') == '' else process.info.get('exe')

                yield Static(f"PID: {process.info.get('pid')} | Name: {name} | "
                             f"Username: {process.info.get('username')} | EXE: [green]{exe}[/green]\n")


class MemUsage(Static):
    BORDER_TITLE = "Memory Usage"

    total = virtual_memory().total
    available = reactive(0)
    used = reactive(0)
    percent = reactive(0.0)

    def update_available(self) -> None:
        self.available = virtual_memory().available

    def watch_available(self, avail: int) -> None:
        pct = compute_percentage_color(self.percent)
        tot = bytes2human(self.total)
        avail = bytes2human(avail)
        used = bytes2human(self.used)
        self.update(f"Total Memory: {tot}\nAvailable Memory: {avail}\nUsed: {used}\nPercentage Used: {pct}%")

    def update_used(self) -> None:
        self.used = virtual_memory().used

    def watch_used(self, u: int) -> None:
        pct = compute_percentage_color(self.percent)
        tot = bytes2human(self.total)
        avail = bytes2human(self.available)
        used = bytes2human(u)
        self.update(f"Total Memory: {tot}\nAvailable Memory: {avail}\nUsed: {used}\nPercentage Used: {pct}%")

    def update_percent(self) -> None:
        self.percent = virtual_memory().percent

    def watch_percent(self, pct: float) -> None:
        pct = compute_percentage_color(pct)
        tot = bytes2human(self.total)
        avail = bytes2human(self.available)
        used = bytes2human(self.used)
        self.update(f"Total Memory: {tot}\nAvailable Memory: {avail}\nUsed: {used}\nPercentage Used: {pct}%")

    def on_mount(self) -> None:
        self.update_available = self.set_interval(INTERVAL, self.update_available)
        self.update_percent = self.set_interval(INTERVAL, self.update_percent)
        self.update_used = self.set_interval(INTERVAL, self.update_used)


class CPU_Usage(Static):
    BORDER_TITLE = "CPU Usage"

    cores = cpu_count()
    percents_indiv = reactive([0.0])
    percent_overall = reactive(0.0)

    def update_cpu_tot(self) -> None:
        self.percent_overall: float = cpu_percent(percpu=False)

    def update_cpu_indiv(self) -> None:
        self.percents_indiv: list = cpu_percent(percpu=True)

    def _display_percentages_CPU(self, percentages: list) -> str:
        string = "\n"

        for i, pct in enumerate(percentages):
            pct = compute_percentage_color(pct)

            string += f"Core {i + 1}: {pct} % |" if i == 0 else f" Core {i + 1}: {pct} % | "

        return string

    def watch_percents_indiv(self, percentages: list) -> None:
        """
        Watch what happens when the percents_indiv variable is changed and react accordingly.

        :param percentages: The list of percentages
        :return: None
        """

        percentage_string = self._display_percentages_CPU(percentages)
        pct = compute_percentage_color(self.percent_overall)
        self.update(f"Cores: {self.cores}\n\nUsage (Overall): {pct} %\n\nUsage (per Core): {percentage_string}")

    def watch_percents_overall(self, percentage: float) -> None:
        percentage_string = self._display_percentages_CPU(self.percents_indiv)
        pct = compute_percentage_color(percentage)
        self.update(f"Cores: {self.cores}\n\nUsage (Overall): {pct} %\n\nUsage (per Core): {percentage_string}")

    def on_mount(self) -> None:
        self.update_cpu = self.set_interval(INTERVAL, self.update_cpu_indiv)
        self.update_cpu_tot = self.set_interval(INTERVAL, self.update_cpu_tot)


class NetInfo(Static):
    BORDER_TITLE = "Network Info"

    connections = net_connections(kind='all')

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            # Get each network connection discovered
            for net in self.connections:

                # Get the info for this connection
                family = net.family.name
                type = net.type.name
                laddr_ip, laddr_port = net.laddr
                status = net.status
                pid = net.pid

                # raddr info can be an empty tuple
                try:
                    raddr_ip, raddr_port = net.raddr
                except ValueError:
                    raddr_ip, raddr_port = None, None

                # Display it
                yield Static(f"PID: {pid} | Status: {status} | Family: {family} | Type: {type} | "
                             f"Local Address: {laddr_ip}/{laddr_port} | "
                             f"Remote Address: "
                             f"{'N/A' if raddr_ip is None and raddr_port is None else f'{raddr_ip}/{raddr_port}'}\n")


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
                    pct = compute_percentage_color(usage.percent)
                    used = bytes2human(usage.used)
                    free = bytes2human(usage.free)
                    total = bytes2human(usage.total)
                except PermissionError:
                    pct = "N/A"
                    used = "N/A"
                    free = "N/A"
                    total = "N/A"

                fs = "N/A" if item.get('fstype') == '' else item.get('fstype')
                device = str(item.get('device')).replace(":\\", '')
                options = item.get('opts')

                yield Static(f"Disk: {device} | Options: {options} |"
                             f" Filesystem: {fs} | Usage: {pct} {'' if options == 'cdrom' else '%'} | Total: {total} | "
                             f"Used: {used} | Free: {free}\n")


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
