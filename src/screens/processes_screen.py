from psutil import process_iter
from textual.app import ComposeResult
from textual.containers import VerticalScroll, Container
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Static, Header, Footer

from src.utilities import UNCOMMON_INTERVAL, compute_percentage_color


class ProcessesScreen(Screen):
    BORDER_TITLE = "Processes"
    BORDER_SUBTITLE = f"Updated every {UNCOMMON_INTERVAL} seconds"
    CSS_PATH = "../styles/processes_css.tcss"
    BINDINGS = [
        ("m", "switch_mode('main')", "Main Screen"),
    ]

    initial = True

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

        procs = process_iter(['pid', 'name', 'username', 'exe', 'cpu_percent'])

        self.processes = sorted(
            (p for p in procs),
            key=lambda x: x.info['cpu_percent'],
            reverse=True
        )

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

        # First, grab the Static Widget
        try:
            static = self.query_one("#process-screen-procs", expect_type=Static)
        except NoMatches():
            return

        static_content = ""

        # Next, go through each updated process, get its info, and update the Static widget
        # with the new info for each process
        for proc in procs:
            PID = proc.info['pid']
            name = proc.info['name'] or 'N/A'
            exe = proc.info['exe'] or 'N/A'
            cpu_percent = compute_percentage_color(proc.info['cpu_percent'])
            user_name = proc.info['username'] or 'N/A'

            # Add the new info for this process to the content of the Static widget
            static_content += (f"PID: {PID} | CPU Load: {cpu_percent} % | Name: {name} | "
                               f"Username: {user_name} | EXE: [#F9F070]{exe}[/]\n\n")

        # Update the content of the Static widget with the new info for all processes
        static.update(static_content)

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
        with Container(id="process-container"):
            with VerticalScroll():
                yield Static("[blink]Populating...[/]", id="process-screen-procs")
        yield Footer()
