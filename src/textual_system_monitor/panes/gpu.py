import sys
from typing import cast

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.timer import Timer
from textual.widgets import Static

from textual_system_monitor.utilities import RARE_INTERVAL, convert_adapter_ram, get_gpu_data, get_palette


class GPU_Usage(Static):
    BORDER_TITLE = f"GPU Info - Updated every {RARE_INTERVAL}s"

    update_timer: Timer

    # Get initial GPU data. Different from approach in `update_gpu_data` because
    # we can't use `self` (to get the kb_size context) outside a function
    gpu_data = reactive(get_gpu_data())

    def _adapter_ram_wrapper(self, adapter_ram: str) -> str:
        """
        Adapter RAM info is given as a string like '1.0 GiB'. Need to separate this to convert the number
        to a human-readable value of Bytes.

        :param adapter_ram: The string corresponding to the adapter RAM for this GPU
        :return: The `bytes_to_human` representation of the adapter RAM
        """

        from textual_system_monitor.app import Monitor  # Need to import here to avoid circular import

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
                    "adapter_ram": self._adapter_ram_wrapper(cast(str, gpu_info["adapter_ram"])),
                    "availability": gpu_info["availability"],
                    "refresh": gpu_info["refresh"],
                    "status": gpu_info["status"],
                }
                for gpu_info in get_gpu_data()
                if gpu_info
            ]
        else:
            self.gpu_data = []

    def watch_gpu_data(self, gpu_data: list[dict[str, str | int]]) -> None:
        """
        Watch `gpu_data` and update the Static Widget with the new information

        :param gpu_data: The list of new GPU data
        """

        # First, grab the Static Widget
        try:
            static = self.query_one("#gpu_pane_static", Static)
        except NoMatches:
            return

        green = get_palette(self.app.theme)["green"]

        static_content = ""

        # Then, for each video controller, update the Static Widget with its new information
        for gpu in gpu_data:
            static_content += (
                f"[bold {green}]GPU[/]: {gpu['gpu']}\n"
                f"[bold {green}]Driver Version[/]: {gpu['driver_version']}\n"
                f"[bold {green}]Resolution[/]: {gpu['resolution']}\n"
                f"[bold {green}]Adapter RAM[/]: {gpu['adapter_ram']}\n"
                f"[bold {green}]Availability[/]: {gpu['availability']}\n"
                f"[bold {green}]Refresh[/]: {gpu['refresh']} Hz\n"
                f"[bold {green}]Status[/]: {gpu['status']}\n"
            )

        static.update(static_content)

    def on_mount(self) -> None:
        """
        Set interval to update the memory information.
        """
        self.update_timer = self.set_interval(RARE_INTERVAL, self.update_gpu_data)

        def _on_theme_change() -> None:
            """
            Callback to cause immediate update when the theme changes
            """
            self.update_timer.reset()

        self.watch(self.app, "theme", _on_theme_change, init=False)

    def on_unmount(self) -> None:
        """
        Kill the timer on unmount to avoid timer-related threading issues
        """
        if self.update_timer:
            self.update_timer.stop()

    def on_click(self) -> None:
        """
        When this pane is clicked, switch to the GPU screen
        """
        self.app.switch_screen("gpu")

    def compose(self) -> ComposeResult:
        """
        Generate a ComposeResult by yielding a vertically-scrolling Static widget with the GPU information.

        :return: The ComposeResult
        """
        with VerticalScroll():
            if sys.platform == "win32":
                yield Static(id="gpu_pane_static")
            else:
                yield Static("GPU information not currently supported on non-Windows systems...", id="gpu_pane_empty")
