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
        ("q", "app.quit", "Quit"),
        ("t", "app.toggle_dark", "Toggle dark mode"),
        ("p", "app.switch_mode('processes')", "Processes"),
        ("c", "app.switch_mode('main')", "Main Screen"),
        ("n", "app.switch_mode('network')", "Network"),
        ("d", "app.switch_mode('drive')", "Drives"),
        ("m", "app.switch_mode('mem')", "Memory"),
        ("v", "app.switch_mode('gpu')", "GPU"),
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

        # First, grab the Static and DataTable Widgets
        try:
            static = self.query_one("#cpu-screen-static", expect_type=Static)
            table = self.query_one("#cpu-screen-table", expect_type=DataTable)
        except NoMatches:
            return

        # Then, get the updated overall data
        cores = cpu_data['cores']
        overall = cpu_data['overall']
        individual = [compute_percentage_color(core) for core in cpu_data['individual']]

        # Update the Static Widget
        static_content = f"Cores: {cores}\n\nOverall: {compute_percentage_color(overall)} %\n\n"
        static.update(static_content)

        # Clear the table and add the columns
        table.clear(columns=True)
        table.add_columns("Core", "Percentage (%)")

        # Update the table
        table.add_rows([(core_num + 1, core_pct) for core_num, core_pct in enumerate(individual)])

    def compose(self) -> ComposeResult:
        """
        Create the structure of the CPU Screen
        :return: The ComposeResult featuring the CPU Screen structure
        """

        yield Header(show_clock=True)
        with Container(id="cpu-screen-container"):
            with VerticalScroll():
                yield Static(id="cpu-screen-static")
            with VerticalScroll():
                yield DataTable(id="cpu-screen-table", show_cursor=False, zebra_stripes=True)
        yield Footer()

    def on_mount(self) -> None:
        """
        Perform initial setup for the CPU Screen
        :return: None
        """

        self.update_cpu_data = self.set_interval(COMMON_INTERVAL, self.update_cpu_data)

        try:
            container = self.query_one("#cpu-screen-container", expect_type=Container)
        except NoMatches:
            return

        container.border_title = self.BORDER_TITLE
