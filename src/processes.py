from psutil import process_iter
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import Static

from utilities import compute_percentage_color


class Processes(Static):
    BORDER_TITLE = "Processes"
    BORDER_SUBTITLE = "Top 10 by CPU Load"

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
        Define how to update `self.processes`.
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

            new_static = Static(f"PID: {PID} | CPU Load: {cpu_percent} | Name: {name} | "
                                f"Username: {user_name} | EXE: [blue]{exe}[/blue]\n", classes="hey")

            scroll.mount(new_static)

    def on_mount(self) -> None:
        """
        Hook up the `update_processes` function, set to a long interval
        """
        self.update_processes = self.set_interval(3, self.update_processes)

    def compose(self) -> ComposeResult:
        """
        Start off with a simple blank VerticalScroll Widget
        :return: The ComposeResult featuring the VerticalScroll
        """
        yield VerticalScroll()
