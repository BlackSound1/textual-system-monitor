from psutil import virtual_memory
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Static

from utilities import compute_percentage_color, bytes2human, INTERVAL


class MemUsage(Static):
    BORDER_TITLE = "Memory Usage"

    total = virtual_memory().total
    available = reactive(0)
    used = reactive(0)
    percent = reactive(0.0)

    def update_available(self) -> None:
        self.available = virtual_memory().available

    def watch_available(self, avail: int) -> None:
        pct = compute_percentage_color(self.percent)
        tot = bytes2human(self.total)
        avail = bytes2human(avail)
        used = bytes2human(self.used)
        self.update(f"Total Memory: {tot}\nAvailable Memory: {avail}\nUsed: {used}\nPercentage Used: {pct}%")

    def update_used(self) -> None:
        self.used = virtual_memory().used

    def watch_used(self, u: int) -> None:
        pct = compute_percentage_color(self.percent)
        tot = bytes2human(self.total)
        avail = bytes2human(self.available)
        used = bytes2human(u)

        try:
            (self.query_one("#mem_static", expect_type=Static)
             .update(f"Total Memory: {tot}\nAvailable Memory: {avail}\nUsed: {used}\nPercentage Used: {pct}%")
             )
        except NoMatches:
            pass

    def update_percent(self) -> None:
        self.percent = virtual_memory().percent

    def watch_percent(self, pct: float) -> None:
        pct = compute_percentage_color(pct)
        tot = bytes2human(self.total)
        avail = bytes2human(self.available)
        used = bytes2human(self.used)

        try:
            (self.query_one("#mem_static", expect_type=Static)
             .update(f"Total Memory: {tot}\nAvailable Memory: {avail}\nUsed: {used}\nPercentage Used: {pct}%")
             )
        except NoMatches:
            pass

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Static(id="mem_static")

    def on_mount(self) -> None:
        self.update_available = self.set_interval(INTERVAL, self.update_available)
        self.update_percent = self.set_interval(INTERVAL, self.update_percent)
        self.update_used = self.set_interval(INTERVAL, self.update_used)
