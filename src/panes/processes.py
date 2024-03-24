from psutil import process_iter
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import Static

from ..utilities import compute_percentage_color, UNCOMMON_INTERVAL


class Processes(Static):
    BORDER_TITLE = "Processes"
    BORDER_SUBTITLE = f"Top 10 by CPU Load - Updated every {UNCOMMON_INTERVAL} seconds"

    initial = True  # When app starts, want to wait a tick before displaying processes. This variable helps with that

    # Set the default processes value to an initial call to the function
    processes = reactive(
        sorted(
            process_iter(['pid', 'name', 'username', 'exe', 'cpu_percent']),
            key=lambda x: x.info.get('cpu_percent'),
            reverse=True
        )[:10]
    )

    def update_processes(self) -> None:
        """
        Define how to update `self.processes`
        """

        self.processes = sorted(
            process_iter(['pid', 'name', 'username', 'exe', 'cpu_percent']),
            key=lambda x: x.info.get('cpu_percent'),
            reverse=True
        )[:10]

    def watch_processes(self, procs: list) -> None:
        """
        Define what happens when `self.processes` changes.

        Update the Processes pane with Statics for each process
        :param procs: The list of new processes to render
        """

        # Don't bother if this is the first tick of the update function
        if self.initial:
            self.initial = False
            return

        # First, grab the VerticalScroll Widget and clear it
        scroll = self.query_one("VerticalScroll", expect_type=VerticalScroll)
        scroll.remove_children()

        # Next, go through each updated process, get its info, and populate the VerticalScroll
        # Widget with a new Static for each processes
        for proc in procs:
            PID = proc.info.get('pid')
            name = 'N/A' if proc.info.get('name') == '' else proc.info.get('name')
            exe = 'N/A' if proc.info.get('exe') == '' else proc.info.get('exe')
            cpu_percent = compute_percentage_color(proc.info.get('cpu_percent'))
            user_name = "N/A" if proc.info.get('username') is None else proc.info.get('username')

            new_static = Static(f"PID: {PID} | CPU Load: {cpu_percent} % | Name: {name} | "
                                f"Username: {user_name} | EXE: [#F9F070]{exe}[/]\n", classes="proc")

            scroll.mount(new_static)

    def on_mount(self) -> None:
        """
        Hook up the `update_processes` function, set to a long interval
        """
        self.update_processes = self.set_interval(UNCOMMON_INTERVAL, self.update_processes)

    def compose(self) -> ComposeResult:
        """
        Start off with a simple VerticalScroll Widget with some initial text
        :return: The ComposeResult featuring the VerticalScroll
        """
        with VerticalScroll():
            yield Static("[blink]Populating...[/]")
