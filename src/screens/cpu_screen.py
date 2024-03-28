from textual.app import ComposeResult
from textual.containers import VerticalScroll, Container
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Static, Header, Footer, DataTable

from ..utilities import COMMON_INTERVAL, get_cpu_data, compute_percentage_color


class CPU_Screen(Screen):

    BORDER_TITLE = "CPU Usage"
    CSS_PATH = "../styles/cpu_css.tcss"
    BINDINGS = [
        ("c", "switch_mode('main')", "Main Screen"),
    ]

    cpu_data = reactive(get_cpu_data())

    def update_cpu_data(self) -> None:
        """
        Update CPU data
        :return: None
        """
        self.cpu_data = get_cpu_data()

    def watch_cpu_data(self, cpu_data: dict) -> None:
        """
        Watch CPU data and update the CPU Screen with the new information

        :param cpu_data: A dictionary containing updated CPU data with keys 'cores', 'overall', and 'individual'.
        :return: None
        """

        # First, grab the Static Widget
        try:
            static = self.query_one("#cpu-screen-static", expect_type=Static)
        except NoMatches():
            return

        # Then, get the updated overall data
        cores = cpu_data['cores']
        overall = cpu_data['overall']
        individual = [compute_percentage_color(core) for core in cpu_data['individual']]

        static_content = f"Cores: {cores}\n\nOverall: {compute_percentage_color(overall)} %\n\n"

        # Update the Static Widget
        static.update(static_content)

        # Then, get the DataTable
        try:
            table = self.query_one("#cpu-screen-table", expect_type=DataTable)
        except NoMatches():
            return

        # Clear the table and add the columns
        table.clear(columns=True)
        table.add_columns("Core", "Percentage (%)")

        # Update the table
        for core_num, core_pct in enumerate(individual):
            table.add_row(core_num + 1, core_pct)

    def compose(self) -> ComposeResult:
        """
        Start off with a VerticalScroll Widget with a Static Widget insider
        :return: The ComposeResult featuring the VerticalScroll and Static Widgets
        """

        yield Header(show_clock=True)
        with Container(id="cpu-screen-container"):
            with VerticalScroll():
                yield Static(id="cpu-screen-static")
            with VerticalScroll():
                yield DataTable(id="cpu-screen-table", show_cursor=False)
        yield Footer()

    def on_mount(self) -> None:
        """
        Perform initial setup for the CPU Screen
        :return: None
        """

        self.update_cpu_data = self.set_interval(COMMON_INTERVAL, self.update_cpu_data)

        try:
            container = self.query_one("#cpu-screen-container", expect_type=Container)
        except NoMatches():
            return

        container.border_title = self.BORDER_TITLE
