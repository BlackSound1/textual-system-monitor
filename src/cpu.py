from psutil import cpu_count, cpu_percent
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Static

from utilities import compute_percentage_color, COMMON_INTERVAL


class CPU_Usage(Static):
    BORDER_TITLE = "CPU Usage"

    cores = cpu_count()
    percents_indiv = reactive([0.0])
    percent_overall = reactive(0.0)

    def update_cpu_tot(self) -> None:
        self.percent_overall: float = cpu_percent(percpu=False)

    def update_cpu_indiv(self) -> None:
        self.percents_indiv: list = cpu_percent(percpu=True)

    def _display_percentages_CPU(self, percentages: list) -> str:
        string = "\n"

        for i, pct in enumerate(percentages):
            pct = compute_percentage_color(pct)

            string += f"Core {i + 1}: {pct} % |" if i == 0 else f" Core {i + 1}: {pct} % | "

        return string

    def watch_percents_indiv(self, percentages: list) -> None:
        """
        Watch what happens when the percents_indiv variable is changed and react accordingly.

        :param percentages: The list of percentages
        :return: None
        """

        percentage_string = self._display_percentages_CPU(percentages)
        pct = compute_percentage_color(self.percent_overall)

        try:
            (self.query_one("#cpu_static", expect_type=Static)
             .update(f"Cores: {self.cores}\n\nUsage (Overall): {pct} %\n\nUsage (per Core): {percentage_string}")
             )
        except NoMatches:
            pass

    def watch_percents_overall(self, percentage: float) -> None:
        percentage_string = self._display_percentages_CPU(self.percents_indiv)
        pct = compute_percentage_color(percentage)

        try:
            (self.query_one("#cpu_static", expect_type=Static)
             .update(f"Cores: {self.cores}\n\nUsage (Overall): {pct} %\n\nUsage (per Core): {percentage_string}")
             )
        except NoMatches:
            pass

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Static(id="cpu_static")

    def on_mount(self) -> None:
        self.update_cpu = self.set_interval(COMMON_INTERVAL, self.update_cpu_indiv)
        self.update_cpu_tot = self.set_interval(COMMON_INTERVAL, self.update_cpu_tot)
