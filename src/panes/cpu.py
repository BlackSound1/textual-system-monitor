from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Static

from ..utilities import COMMON_INTERVAL, get_cpu_data, update_CPU_static


class CPU_Usage(Static):
    BORDER_TITLE = "CPU Usage"

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
            static = self.query_one("Static", expect_type=Static)
        except NoMatches():
            return

        # Then, get the updated data
        static_content = update_CPU_static(cpu_data)

        # Update the Static Widget
        static.update(static_content)

    def on_click(self) -> None:
        """
        When this pane is clicked, switch to the CPU screen
        :return: None
        """
        self.app.switch_mode("cpu")

    def compose(self) -> ComposeResult:
        """
        Start off with a VerticalScroll Widget with a Static Widget insider
        :return: The ComposeResult featuring the VerticalScroll and Static Widgets
        """
        with VerticalScroll():
            yield Static()

    def on_mount(self) -> None:
        """
        Set intervals to update cpu usage
        :return: None
        """
        self.update_cpu_data = self.set_interval(COMMON_INTERVAL, self.update_cpu_data)
