from typing import Any, ClassVar, cast
from collections.abc import Iterator

from psutil import Process, process_iter
from textual import getters
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Header, Footer, DataTable, Button

from src.utilities import UNCOMMON_INTERVAL, get_color_formatted_string, get_non_zero_procs, get_palette


def _get_procs(sort: bool) -> Iterator[Process] | list[Process]:
    """
    Get the list of processes, depending on the value of `sort`

    :param sort: Whether to sort the processes by CPU load
    :return: The list of processes (possibly sorted)
    """
    procs = process_iter(["pid", "name", "username", "exe", "cpu_percent"])
    if sort:
        procs = sorted(
            get_non_zero_procs(procs),
            key=lambda x: cast(float, x.info.get("cpu_percent")),
            reverse=True,
        )
    return procs


class ProcessesScreen(Screen[None]):
    BORDER_TITLE = f"Processes - Updated every {UNCOMMON_INTERVAL}s"
    CSS_PATH = "../styles/processes_css.tcss"
    BINDINGS: ClassVar = [
        Binding(key="q", action="app.quit", description="Quit"),
        Binding(key="p", action="app.switch_screen('main')", description="Main Screen"),
        Binding(key="c", action="app.switch_screen('cpu')", description="CPU"),
        Binding(key="n", action="app.switch_screen('network')", description="Network"),
        Binding(key="d", action="app.switch_screen('drive')", description="Drives"),
        Binding(key="m", action="app.switch_screen('mem')", description="Memory"),
        Binding(key="v", action="app.switch_screen('gpu')", description="GPU"),
        Binding(key="/", action="", description=""),
    ]

    initial = True
    paused = False
    sort = True

    update_timer: Timer

    # Set the default processes value to an initial call to the function
    processes = reactive(_get_procs(sort=sort))

    table = cast(DataTable[Any], getters.query_one("#process-screen-table", expect_type=DataTable))
    container = getters.query_one("#process-container", expect_type=Container)

    def update_processes(self) -> None:
        """
        Define how to update `self.processes`
        """
        if self.paused:
            return
        self.processes = _get_procs(sort=self.sort)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Define what to do when either the pause or sort Button is pressed

        :param event: The Button Pressed event
        """

        # Get which button was pressed
        button_id = event.button.id

        # If the pause button is pressed, toggle the paused state and update the button
        if button_id == "process-pause-button":
            self.paused = not self.paused

            pause_button = self.screen.query_one("#process-pause-button", expect_type=Button)
            pause_button.label = "Resume" if self.paused else "Pause"
            pause_button.variant = "error" if self.paused else "success"

        # If the sort button is pressed, toggle the sort state and update the button
        elif button_id == "process-sort-button":
            self.sort = not self.sort

            sort_button = self.screen.query_one("#process-sort-button", expect_type=Button)
            sort_button.label = "Sorted" if self.sort else "Unsorted"
            sort_button.variant = "success" if self.sort else "error"

    def watch_processes(self, procs: Iterator[Process] | list[Process]) -> None:
        """
        Define what happens when `self.processes` changes.

        Update the Processes pane with Statics for each process

        :param procs: The list of new processes to render
        """
        palette = get_palette(self.app.theme)

        # Clear the table and add columns
        self.table.clear(columns=True)
        self.table.add_columns("PID", "Name", "Username", "CPU Load (%)", "EXE")

        # Next, go through each updated process, get its info, and update the table widget
        # with the new info for each process
        for proc in procs:
            info = proc.info
            PID = info["pid"]
            name = info["name"] or "N/A"
            exe = info["exe"] or "N/A"
            cpu_percent = get_color_formatted_string(palette, info["cpu_percent"])
            user_name = info["username"] or "N/A"

            # Only colorize the name if it's not "N/A"
            if name != "N/A":
                name = f"[bold {palette['orange']}]{name}[/]"

            self.table.add_row(PID, name, user_name, cpu_percent, exe)

    def on_mount(self) -> None:
        """
        Perform initial setup for the Processes Screen
        """
        self.update_timer = self.set_interval(UNCOMMON_INTERVAL, self.update_processes)
        self.container.border_title = self.BORDER_TITLE
        self.container.styles.border = ("round", get_palette(self.app.theme)["orange"])

        def _on_theme_change() -> None:
            """
            Update the border color based on the theme
            """
            self.container.styles.border = ("round", get_palette(self.app.theme)["orange"])

        self.watch(self.app, "theme", _on_theme_change, init=False)

    def on_unmount(self) -> None:
        """
        Kill the timer on unmount to avoid timer-related threading issues
        """
        if self.update_timer:
            self.update_timer.stop()

    def compose(self) -> ComposeResult:
        """
        Display the structure of the Process Screen

        :return: The ComposeResult featuring the structure of the Screen
        """
        yield Header(show_clock=True)
        with Container(id="process-screen-container"):
            with Horizontal(id="process-options-container"):
                yield Button("Sorted", variant="success", id="process-sort-button")
                yield Button("Pause", variant="success", id="process-pause-button")
            with Container(id="process-container"):
                yield DataTable(id="process-screen-table", show_cursor=True, cursor_type="row", zebra_stripes=True)
        yield Footer()
