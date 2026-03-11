from typing import Any, cast

from textual.app import ComposeResult
from textual.containers import VerticalScroll, Container
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Static, Header, Footer, DataTable

from ..utilities import COMMON_INTERVAL, get_cpu_data, compute_percentage_color


class CPU_Screen(Screen[None]):

    BORDER_TITLE = f"CPU Usage - Updated every {COMMON_INTERVAL}s"
    CSS_PATH = "../styles/cpu_css.tcss"
    BINDINGS = [
        ("q", "app.quit", "Quit"),
        ("p", "app.switch_mode('processes')", "Processes"),
        ("c", "app.switch_mode('main')", "Main Screen"),
        ("n", "app.switch_mode('network')", "Network"),
        ("d", "app.switch_mode('drive')", "Drives"),
        ("m", "app.switch_mode('mem')", "Memory"),
        ("v", "app.switch_mode('gpu')", "GPU"),
    ]

    update_timer: Timer | None = None

    cpu_data = reactive(get_cpu_data())

    def update_cpu_data(self) -> None:
        """
        Update CPU data
        :return: None
        """
        self.cpu_data = get_cpu_data()

    def watch_cpu_data(self, cpu_data: dict[str, int | float | list[float] | None]) -> None:
        """
        Watch CPU data and update the CPU Screen with the new information

        :param cpu_data: A dictionary containing updated CPU data with keys 'cores', 'overall', and 'individual'.
        :return: None
        """

        # First, grab the Static and DataTable Widgets
        try:
            static = self.query_one("#cpu-screen-static", expect_type=Static)
            table = cast(DataTable[Any], self.query_one("#cpu-screen-table", expect_type=DataTable))
        except NoMatches:
            return

        # Then, get the updated overall data
        cores = cpu_data['cores']
        overall = cpu_data['overall']
        indiv_list = cast(list[float], cpu_data['individual'])  # To please static analyzer
        individual = [compute_percentage_color(core) for core in indiv_list]

        # Update the Static Widget
        static_content = f"Cores: {cores}\n\nOverall: {compute_percentage_color(cast(float, overall))} %\n\n"
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

        self.update_timer = self.set_interval(COMMON_INTERVAL, self.update_cpu_data)

        try:
            container = self.query_one("#cpu-screen-container", expect_type=Container)
        except NoMatches:
            return

        container.border_title = self.BORDER_TITLE

    def on_unmount(self) -> None:
        if self.update_timer:
            self.update_timer.stop()
