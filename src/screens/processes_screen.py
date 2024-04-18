from psutil import process_iter
from textual.app import ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable, Button

from src.utilities import UNCOMMON_INTERVAL, compute_percentage_color


def get_procs(sort: bool) -> list:
    """
    Get the list of processes, depending on the value of `sort`
    :param sort: Whether to sort the processes by CPU load
    :return: The list of processes (possibly sorted)
    """

    procs = process_iter(['pid', 'name', 'username', 'exe', 'cpu_percent'])

    if sort:
        procs = sorted(
            (p for p in procs),
            key=lambda x: x.info.get('cpu_percent'),
            reverse=True
        )

    return procs


class ProcessesScreen(Screen):
    BORDER_TITLE = "Processes"
    BORDER_SUBTITLE = f"Updated every {UNCOMMON_INTERVAL} seconds"
    CSS_PATH = "../styles/processes_css.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("t", "toggle_dark", "Toggle dark mode"),
        ("p", "switch_mode('main')", "Main Screen"),
        ("c", "switch_mode('cpu')", "CPU"),
        ("n", "switch_mode('network')", "Network"),
        ("d", "switch_mode('drive')", "Drives"),
        ("m", "switch_mode('mem')", "Memory"),
    ]

    initial = True
    paused = False
    sort = True

    # Set the default processes value to an initial call to the function
    processes = reactive(get_procs(sort=sort))

    def update_processes(self) -> None:
        """
        Define how to update `self.processes`
        """

        if self.paused:
            return

        self.processes = get_procs(sort=self.sort)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Define what to do when either the pause or sort Button is pressed
        :param event: The Button Pressed event
        :return: None
        """

        # Get which button was pressed
        button_id = event.button.id

        # If the pause button is pressed, toggle the paused state and update the button
        if button_id == "process-pause-button":
            self.paused = not self.paused

            pause_button = self.query_one("#process-pause-button", expect_type=Button)
            pause_button.label = "Resume" if self.paused else "Pause"
            pause_button.variant = "error" if self.paused else "success"

        # If the sort button is pressed, toggle the sort state and update the button
        elif button_id == "process-sort-button":
            self.sort = not self.sort

            sort_button = self.query_one("#process-sort-button", expect_type=Button)
            sort_button.label = "Sorted" if self.sort else "Unsorted"
            sort_button.variant = "success" if self.sort else "error"

    def watch_processes(self, procs: list) -> None:
        """
        Define what happens when `self.processes` changes.

        Update the Processes pane with Statics for each process
        :param procs: The list of new processes to render
        """

        # First, grab the DataTable Widget
        try:
            table = self.query_one("#process-screen-table", expect_type=DataTable)
        except NoMatches:
            return

        # Then, clear the table and add columns
        table.clear(columns=True)
        table.add_columns("PID", "Name", "Username", "CPU Load (%)", "EXE")

        # Next, go through each updated process, get its info, and update the table widget
        # with the new info for each process
        for proc in procs:
            info = proc.info
            PID = info['pid']
            name = info['name'] or 'N/A'
            exe = info['exe'] or 'N/A'
            cpu_percent = compute_percentage_color(info['cpu_percent'])
            user_name = info['username'] or 'N/A'

            # Only colorize the name if it's not "N/A"
            if name != "N/A":
                name = f"[blue]{name}[/]"

            table.add_row(PID, name, user_name, cpu_percent, exe)

    def on_mount(self) -> None:
        """
        Perform initial setup for the Processes Screen
        :return: None
        """

        self.update_processes = self.set_interval(UNCOMMON_INTERVAL, self.update_processes)

        try:
            container = self.query_one("#process-container", expect_type=Container)
        except NoMatches:
            return

        container.border_title = self.BORDER_TITLE
        container.border_subtitle = self.BORDER_SUBTITLE

    def compose(self) -> ComposeResult:
        """
        Display the structure of the Process Screen
        :return: The ComposeResult featuring the structure of the Screen
        """

        yield Header(show_clock=True)

        with Container(id="process-screen-container"):
            with Container(id="process-options-container"):
                yield Button("Sorted", variant="success", id="process-sort-button")
                yield Button("Pause", variant="success", id="process-pause-button")

            with Container(id="process-container"):
                yield DataTable(id="process-screen-table", show_cursor=True, cursor_type="row", zebra_stripes=True)

        yield Footer()
