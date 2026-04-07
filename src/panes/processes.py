from typing import cast
from collections.abc import Iterator

from psutil import Process, process_iter
from textual import getters
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.timer import Timer
from textual.widgets import Static

from ..utilities import UNCOMMON_INTERVAL, get_color_formatted_string, get_non_zero_procs, get_palette


class Processes(Static):
    BORDER_TITLE = f"Processes - Updated every {UNCOMMON_INTERVAL}s"
    BORDER_SUBTITLE = "Top 10 by CPU Load"

    update_timer: Timer

    initial = True  # When app starts, want to wait a tick before displaying processes. This variable helps with that

    # Set the default processes value to an initial call to the function
    procs = process_iter(['pid', 'name', 'username', 'exe', 'cpu_percent'])
    processes = reactive(
        sorted(
            get_non_zero_procs(procs),
            key=lambda x: cast(float, x.info.get('cpu_percent')),
            reverse=True,
        )[:10],
    )

    static = getters.query_one("#procs_pane_static", expect_type=Static)

    def update_processes(self) -> None:
        """
        Update the list of processes with the top 10 by CPU load.
        """
        procs = process_iter(['pid', 'name', 'username', 'exe', 'cpu_percent'])
        self.processes = sorted(
            get_non_zero_procs(procs),
            key=lambda x: x.info['cpu_percent'],
            reverse=True,
        )[:10]

    def watch_processes(self, procs: Iterator[Process]) -> None:
        """
        Define what happens when `self.processes` changes.

        Update the Processes pane with Statics for each process

        :param procs: The list of new processes to render
        """

        palette = get_palette(self.app.theme)

        # Don't bother if this is the first tick of the update function
        if self.initial:
            self.initial = False
            return

        static_content = ""

        # Go through each updated process, get its info, and update the Static widget
        # with the new info for each process
        for proc in procs:
            PID = proc.info['pid']
            name = proc.info['name'] or 'N/A'
            exe = proc.info['exe'] or 'N/A'
            cpu_percent = get_color_formatted_string(palette, proc.info['cpu_percent'])
            user_name = proc.info['username'] or 'N/A'

            # Add the new info for this process to the content of the Static widget
            static_content += (f"PID: {PID} | CPU Load: {cpu_percent} % | Name: [bold {palette['orange']}]{name}[/] | "
                               f"Username: {user_name} | EXE: {exe}\n\n")

        # Update the content of the Static widget with the new info for all processes
        self.static.update(static_content)

    def on_mount(self) -> None:
        """
        Hook up the `update_processes` function, set to a long interval
        """
        self.update_timer = self.set_interval(UNCOMMON_INTERVAL, self.update_processes)

    def on_unmount(self) -> None:
        """
        Kill the timer on unmount to avoid timer-related threading issues
        """
        if self.update_timer:
            self.update_timer.stop()

    def on_click(self) -> None:
        """
        When this pane is clicked, switch to the Processes screen
        """
        self.app.switch_screen("processes")

    def compose(self) -> ComposeResult:
        """
        Start off with a simple VerticalScroll Widget with some initial text

        :return: The ComposeResult featuring the VerticalScroll
        """
        with VerticalScroll():
            yield Static("[blink]Populating...[/]", id="procs_pane_static")
