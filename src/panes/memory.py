from psutil import virtual_memory
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Static

from ..utilities import compute_percentage_color, bytes2human, COMMON_INTERVAL


class MemUsage(Static):
    BORDER_TITLE = "Memory Usage"

    total = virtual_memory().total
    available = reactive(0)
    used = reactive(0)
    percent = reactive(0.0)

    def update_available(self) -> None:
        """
        Update the available memory by assigning the value of virtual_memory().available to self.available.
        """
        self.available = virtual_memory().available

    def watch_available(self, avail: int) -> None:
        """
        Update memory information with the total, available, used memory, and percentage used.

        :param avail: The updated amount of available memory in Bytes
        :return: None
        """

        pct = compute_percentage_color(self.percent)
        tot = bytes2human(self.total)
        avail = bytes2human(avail)
        used = bytes2human(self.used)
        self.update(f"Total Memory: {tot}\nAvailable Memory: {avail}\nUsed: {used}\nPercentage Used: {pct}%")

    def update_used(self) -> None:
        """
        Update the used memory by assigning the value of virtual_memory().used to self.used.

        :return: None
        """
        self.used = virtual_memory().used

    def watch_used(self, u: int) -> None:
        """
        Update memory information with the total, available, used memory, and percentage used.

        :param u: The updated amount of used memory in Bytes
        :return: None
        """

        # Compute the percentage used and format the memory values
        pct = compute_percentage_color(self.percent)

        # Convert memory sizes to human-readable format
        tot = bytes2human(self.total)
        avail = bytes2human(self.available)
        used = bytes2human(u)

        # Update the memory information in the UI
        try:
            (
                self.query_one("#mem_static", expect_type=Static)
                .update(f"Total Memory: {tot}\nAvailable Memory: {avail}\nUsed: {used}\nPercentage Used: {pct}%")
            )
        except NoMatches:
            pass

    def update_percent(self) -> None:
        """
        Update the percentage used by assigning the value of virtual_memory().percent to self.percent

        :return: None
        """
        self.percent = virtual_memory().percent

    def watch_percent(self, pct: float) -> None:
        """
        Updates the memory information with the total, available, used memory, and percentage used

        :param pct: The updated percentage used
        :return: None
        """

        # Compute the color based on the percentage
        pct = compute_percentage_color(pct)

        # Convert memory sizes to human-readable format
        tot = bytes2human(self.total)
        avail = bytes2human(self.available)
        used = bytes2human(self.used)

        # Update the memory information in the UI
        try:
            (
                self.query_one("#mem_static", expect_type=Static)
                .update(f"Total Memory: {tot}\nAvailable Memory: {avail}\nUsed: {used}\nPercentage Used: {pct}%")
            )
        except NoMatches:
            pass

    def compose(self) -> ComposeResult:
        """
        Generate a ComposeResult by yielding a Static widget with the memory information.

        :return: The ComposeResult
        """
        with VerticalScroll():
            yield Static(id="mem_static")

    def on_mount(self) -> None:
        """
        Set intervals to update the memory information.

        :return: None
        """
        self.update_available = self.set_interval(COMMON_INTERVAL, self.update_available)
        self.update_percent = self.set_interval(COMMON_INTERVAL, self.update_percent)
        self.update_used = self.set_interval(COMMON_INTERVAL, self.update_used)
