from textual.app import ComposeResult
from textual.containers import VerticalScroll, Container
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Static, Header, Footer

from ..utilities import COMMON_INTERVAL, get_cpu_data, update_CPU_static


class CPU_Screen(Screen):

    BORDER_TITLE = "CPU Usage"
    CSS_PATH = "../styles/cpu_css.tcss"
    BINDINGS = [("m", "switch_mode('main')", "Main Screen")]

    cpu_data = reactive(get_cpu_data())

    def update_cpu_data(self) -> None:
        """
        Update CPU data
        :return: None
        """
        self.cpu_data = get_cpu_data()

    def watch_cpu_data(self, cpu_data: dict) -> None:
        """
        Watch CPU data and update the Static Widget with the new information

        :param cpu_data: A dictionary containing updated CPU data with keys 'cores', 'overall', and 'individual'.
        :return: None
        """

        # First, grab the Static Widget
        try:
            static = self.query_one("#cpu-screen-static", expect_type=Static)
        except NoMatches():
            return

        # Then, get the updated data
        static_content = update_CPU_static(cpu_data)

        # Update the Static Widget
        static.update(static_content)

    def compose(self) -> ComposeResult:
        """
        Start off with a VerticalScroll Widget with a Static Widget insider
        :return: The ComposeResult featuring the VerticalScroll and Static Widgets
        """

        yield Header(show_clock=True)
        with Container(id="cpu-screen-container"):
            with VerticalScroll():
                yield Static(id="cpu-screen-static")
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
