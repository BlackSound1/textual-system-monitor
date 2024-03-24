from psutil import cpu_count, cpu_percent
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import Static

from ..utilities import compute_percentage_color, COMMON_INTERVAL


def _get_cpu_data() -> dict:
    """
    Return a dictionary containing CPU data with keys 'cores', 'overall', and 'individual'

    :return: The dictionary containing CPU data
    """
    return {
        "cores": cpu_count(),
        "overall": cpu_percent(percpu=False),
        "individual": cpu_percent(percpu=True)
    }


def _display_percentages_CPU(percentages: list) -> str:
    """
    Display the percentages of each core in a string

    :param percentages:
    :return: The string containing the formatted percentages
    """

    string = "\n"

    for i, pct in enumerate(percentages):
        pct = compute_percentage_color(pct)

        separator = " | " if i < len(percentages) - 1 else ""

        string += f"Core {i + 1}: {pct} % {separator}"

    return string


class CPU_Usage(Static):
    BORDER_TITLE = "CPU Usage"

    cpu_data = reactive(_get_cpu_data())

    def update_cpu_data(self) -> None:
        """
        Update CPU data
        :return: None
        """
        self.cpu_data = _get_cpu_data()

    def watch_cpu_data(self, cpu_data: dict) -> None:
        """
        Watch CPU data and update the Static Widget with the new information

        :param cpu_data: A dictionary containing updated CPU data with keys 'cores', 'overall', and 'individual'.
        :return: None
        """

        # First, grab the Static Widget
        static = self.query_one("Static", expect_type=Static)

        # Then, get the updated data
        cores = cpu_data['cores']
        overall = cpu_data['overall']
        individual = _display_percentages_CPU(cpu_data['individual'])  # Colorize the percentages

        # Update the Static Widget
        static_content = (f"Cores: {cores}\n\nOverall: {compute_percentage_color(overall)} %\n\n"
                          f"Per Core: {individual}\n\n")

        static.update(static_content)

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
