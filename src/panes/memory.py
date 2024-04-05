from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Static

from ..utilities import compute_percentage_color, bytes2human, COMMON_INTERVAL, get_mem_data


class MemUsage(Static):
    BORDER_TITLE = "Memory Usage"

    mem_data = reactive(get_mem_data())

    def update_mem_data(self) -> None:
        """
        Update the memory information by calling `_get_mem_data`

        :return: None
        """
        self.mem_data = get_mem_data()

    def watch_mem_data(self, data: dict) -> None:
        """
        Watch for changes in the memory data and update the Static widget accordingly

        :param data: The new memory data
        :return: None
        """

        try:
            static = self.query_one("Static", Static)
        except NoMatches:
            return

        static.update(f"Total Memory: {bytes2human(data['total'])}\n\n"
                      f"Available Memory: {bytes2human(data['available'])}\n\n"
                      f"Used: {bytes2human(data['used'])}\n\n"
                      f"Percentage Used: {compute_percentage_color(data['percent'])}%")

    def on_click(self) -> None:
        """
        Switch to the Memory screen when clicked
        :return: None
        """
        self.app.switch_mode("mem")

    def compose(self) -> ComposeResult:
        """
        Generate a ComposeResult by yielding a vertically-scrolling Static widget with the memory information.

        :return: The ComposeResult
        """
        with VerticalScroll():
            yield Static(id="mem-static")

    def on_mount(self) -> None:
        """
        Set intervals to update the memory information.
        :return: None
        """
        self.update_mem_data = self.set_interval(COMMON_INTERVAL, self.update_mem_data)
