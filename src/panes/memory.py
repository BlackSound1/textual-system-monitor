from typing import cast

from textual import getters
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.timer import Timer
from textual.widgets import Static

from ..utilities import bytes_to_human, COMMON_INTERVAL, get_color_formatted_string, get_mem_data, get_pallette


class MemUsage(Static):
    BORDER_TITLE = f"Memory Usage - Updated every {COMMON_INTERVAL}s"

    update_timer: Timer | None = None

    mem_data = reactive(get_mem_data())

    static = getters.query_one("#mem_pane_static", expect_type=Static)

    def update_mem_data(self) -> None:
        """
        Update the memory information by calling `get_mem_data()`

        :return: None
        """
        self.mem_data = get_mem_data()

    def watch_mem_data(self, data: dict[str, int | float]) -> None:
        """
        Watch for changes in the memory data and update the Static widget accordingly

        :param data: The new memory data
        :return: None
        """

        from src.app import Monitor

        kb_size = cast(Monitor, self.app).CONTEXT['kb_size']

        palette = get_pallette(self.app.theme)

        self.static.update(
            f"Total Memory: {bytes_to_human(data['total'], kb_size)}\n\n"
            f"Available Memory: {bytes_to_human(data['available'], kb_size)}\n\n"
            f"Used: {bytes_to_human(data['used'], kb_size)}\n\n"
            f"Percentage Used: {get_color_formatted_string(palette, data['percent'])} %"
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
            yield Static(id="mem_pane_static")

    def on_mount(self) -> None:
        """
        Set intervals to update the memory information.
        :return: None
        """
        self.update_timer = self.set_interval(COMMON_INTERVAL, self.update_mem_data)

    def on_unmount(self) -> None:
        """
        Kill the timer on unmount to avoid timer-related threading issues
        """
        if self.update_timer:
            self.update_timer.stop()
