from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Static

from ..utilities import compute_percentage_color, bytes_to_human, COMMON_INTERVAL, get_mem_data


class MemUsage(Static):
    BORDER_TITLE = f"Memory Usage - Updated every {COMMON_INTERVAL}s"

    mem_data = reactive(get_mem_data())

    def update_mem_data(self) -> None:
        """
        Update the memory information by calling `get_mem_data()`

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

        # Get KB size
        kb_size = self.app.CONTEXT['kb_size']

        static.update(
            f"Total Memory: {bytes_to_human(data['total'], kb_size)}\n\n"
            f"Available Memory: {bytes_to_human(data['available'], kb_size)}\n\n"
            f"Used: {bytes_to_human(data['used'], kb_size)}\n\n"
            f"Percentage Used: {compute_percentage_color(data['percent'])} %"
        )

    def on_click(self) -> None:
        """
        Switch to the Memory screen when clicked
        :return: None
        """
        self.app.switch_mode("mem")

    def compose(self) -> ComposeResult:
        """
        Generate a ComposeResult by yielding a vertically scrolling Static widget with the memory information.

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
