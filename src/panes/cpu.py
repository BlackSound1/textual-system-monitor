from textual import getters
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.timer import Timer
from textual.widgets import Static

from ..utilities import COMMON_INTERVAL, get_cpu_data, get_palette, update_CPU_static


class CPU_Usage(Static):
    BORDER_TITLE = f"CPU Usage - Updated every {COMMON_INTERVAL}s"

    update_timer: Timer

    cpu_data = reactive(get_cpu_data())

    static = getters.query_one("#cpu_pane_static", expect_type=Static)

    def update_cpu_data(self) -> None:
        """
        Update CPU data
        """
        self.cpu_data = get_cpu_data()

    def watch_cpu_data(self, cpu_data: dict[str, int | float | list[float] | None]) -> None:
        """
        Watch CPU data and update the Static Widget with the new information

        :param cpu_data: A dictionary containing updated CPU data with keys 'cores', 'overall', and 'individual'.
        """
        palette = get_palette(self.app.theme)
        static_content = update_CPU_static(cpu_data, palette)
        self.static.update(static_content)

    def on_click(self) -> None:
        """
        When this pane is clicked, switch to the CPU screen
        """
        self.app.switch_mode("cpu")

    def compose(self) -> ComposeResult:
        """
        Start off with a VerticalScroll Widget with a Static Widget insider

        :return: The ComposeResult featuring the VerticalScroll and Static Widgets
        """
        with VerticalScroll():
            yield Static(id="cpu_pane_static")

    def on_mount(self) -> None:
        """
        Set intervals to update cpu usage
        """
        self.update_timer = self.set_interval(COMMON_INTERVAL, self.update_cpu_data)

    def on_unmount(self) -> None:
        """
        Kill the timer on unmount to avoid timer-related threading issues
        """
        if self.update_timer:
            self.update_timer.stop()
