from psutil import process_iter
from textual.app import ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable, Button

from src.utilities import UNCOMMON_INTERVAL, compute_percentage_color


class ProcessesScreen(Screen):
    BORDER_TITLE = "Processes"
    BORDER_SUBTITLE = f"Updated every {UNCOMMON_INTERVAL} seconds"
    CSS_PATH = "../styles/processes_css.tcss"
    BINDINGS = [
        ("p", "switch_mode('main')", "Main Screen"),
    ]

    initial = True
    paused = False
    sort = True

    # Set the default processes value to an initial call to the function
    procs = process_iter(['pid', 'name', 'username', 'exe', 'cpu_percent'])
    processes = reactive(
        sorted(
            (p for p in procs),
            key=lambda x: x.info.get('cpu_percent'),
            reverse=True
        )
    )

    def update_processes(self) -> None:
        """
        Define how to update `self.processes`
        """

        if self.paused:
            return

        procs = process_iter(['pid', 'name', 'username', 'exe', 'cpu_percent'])

        self.processes = sorted(
            (p for p in procs),
            key=lambda x: x.info['cpu_percent'],
            reverse=True
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "process-pause-button":
            self.paused = not self.paused

            pause_button = self.query_one("#process-pause-button", expect_type=Button)
            pause_button.label = "Resume" if self.paused else "Pause"
            # pause_button.styles.background = Color.parse("error") if self.paused else Color.parse("success")
        elif button_id == "process-sort-button":
            self.sort = not self.sort

    def watch_processes(self, procs: list) -> None:
        """
        Define what happens when `self.processes` changes.

        Update the Processes pane with Statics for each process
        :param procs: The list of new processes to render
        """

        # First, grab the DataTable Widget
        try:
            table = self.query_one("#process-screen-table", expect_type=DataTable)
        except NoMatches():
            return

        # Then, clear the table and add columns
        table.clear(columns=True)
        table.add_columns("PID", "Name", "Username", "CPU Load (%)", "EXE")

        # Next, go through each updated process, get its info, and update the table widget
        # with the new info for each process
        for proc in procs:
            PID = proc.info['pid']
            name = proc.info['name'] or 'N/A'
            exe = proc.info['exe'] or 'N/A'
            cpu_percent = compute_percentage_color(proc.info['cpu_percent'])
            user_name = proc.info['username'] or 'N/A'

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
        except NoMatches():
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
                yield Button("Sort?", variant="primary", id="process-sort-button")
                yield Button("Pause", variant="primary", id="process-pause-button")
            with Container(id="process-container"):
                yield DataTable(id="process-screen-table", show_cursor=True, cursor_type="row", zebra_stripes=True)
        yield Footer()
