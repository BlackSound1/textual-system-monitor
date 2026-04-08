import sys
from typing import Any, ClassVar, cast

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, VerticalScroll
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import DataTable, Footer, Header, Static

from src.utilities import RARE_INTERVAL, convert_adapter_ram, get_gpu_data, get_palette


class GPU_Screen(Screen[None]):
    BORDER_TITLE = f"GPU Info - Updated every {RARE_INTERVAL}s"
    CSS_PATH = "../styles/gpu_css.tcss"
    BINDINGS: ClassVar = [
        Binding(key="q", action="app.quit", description="Quit"),
        Binding(key="p", action="app.switch_screen('processes')", description="Processes"),
        Binding(key="c", action="app.switch_screen('cpu')", description="CPU"),
        Binding(key="n", action="app.switch_screen('network')", description="Network"),
        Binding(key="d", action="app.switch_screen('drive')", description="Drives"),
        Binding(key="m", action="app.switch_screen('mem')", description="Memory"),
        Binding(key="v", action="app.switch_screen('main')", description="Main Screen"),
    ]

    update_timer: Timer

    gpu_data = reactive(get_gpu_data())

    def adapter_ram_wrapper(self, adapter_ram: str) -> str:
        """
        Adapter RAM info is given as a string like '1.0 GiB'. Need to separate this to convert the number
        to a human-readable value of Bytes.

        :param adapter_ram: The string corresponding to the adapter RAM for this GPU
        :return: The `bytes_to_human` representation of the adapter RAM
        """

        from src.app import Monitor

        kb_size = cast(Monitor, self.app).CONTEXT["kb_size"]
        return convert_adapter_ram(adapter_ram, kb_size)

    def update_gpu_data(self) -> None:
        """
        Update GPU data
        """
        if sys.platform == "win32":
            self.gpu_data = [
                {
                    "gpu": gpu_info["gpu"],
                    "driver_version": gpu_info["driver_version"],
                    "resolution": gpu_info["resolution"],
                    "adapter_ram": self.adapter_ram_wrapper(cast(str, gpu_info["adapter_ram"])),
                    "availability": gpu_info["availability"],
                    "refresh": gpu_info["refresh"],
                    "status": gpu_info["status"],
                }
                for gpu_info in get_gpu_data()
                if gpu_info
            ]
        else:
            self.gpu_data = None

    def watch_gpu_data(self, gpu_data: list[dict[str, str | int]]) -> None:
        """
        Watch `gpu_data` and update the Static Widget with the new information

        :param gpu_data: The list of new GPU data
        """

        # First, grab the Static Widget
        try:
            table = cast(DataTable[Any], self.screen.query_one("#gpu-screen-table", expect_type=DataTable))
        except NoMatches:
            return

        # Clear the table and add the columns
        table.clear(columns=True)
        table.add_columns("GPU", "Driver Version", "Resolution", "Adapter RAM", "Availability", "Refresh", "Status")

        # Then, for each video controller, update the Static Widget with its new information
        for gpu_info in gpu_data:
            name = gpu_info["gpu"]
            version = gpu_info["driver_version"]
            resolution = gpu_info["resolution"]
            ram = gpu_info["adapter_ram"]
            availability = gpu_info["availability"]
            refresh = gpu_info["refresh"]
            status = gpu_info["status"]

            table.add_row(name, version, resolution, ram, availability, refresh, status)

    def on_mount(self) -> None:
        """
        Perform initial setup for the GPU Screen
        """
        self.update_timer = self.set_interval(RARE_INTERVAL, self.update_gpu_data)

        try:
            container = self.screen.query_one("#gpu-container", expect_type=Container)
        except NoMatches:
            return

        container.border_title = self.BORDER_TITLE
        container.styles.border = ("round", get_palette(self.app.theme)["pink"])

        def _on_theme_change() -> None:
            """
            Update the border color based on the theme
            """
            container.styles.border = ("round", get_palette(self.app.theme)["pink"])

        self.watch(self.app, "theme", _on_theme_change, init=False)

    def on_unmount(self) -> None:
        """
        Kill the timer on unmount to avoid timer-related threading issues
        """
        if self.update_timer:
            self.update_timer.stop()

    def compose(self) -> ComposeResult:
        """
        Display the structure of the GPU Screen

        :return: The ComposeResult featuring the structure of the GPU Screen
        """
        yield Header(show_clock=True)
        with Container(id="gpu-container"):  # noqa: SIM117
            with VerticalScroll():
                if sys.platform == "win32":
                    yield DataTable(id="gpu-screen-table", show_cursor=False, zebra_stripes=True)
                else:
                    yield Static(
                        "GPU information not currently supported on non-Windows systems...",
                        id="gpu_screen_empty",
                    )
        yield Footer()
