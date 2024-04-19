import platform

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Static

from src.utilities import get_gpu_data, RARE_INTERVAL

WINDOWS = platform.system() == "Windows"


class GPU_Usage(Static):
    BORDER_TITLE = "GPU Info"
    BORDER_SUBTITLE = f"Updated every {RARE_INTERVAL} seconds"

    gpu_data = reactive(get_gpu_data()) if WINDOWS else None

    def update_gpu_data(self) -> None:
        """
        Update GPU data

        :return: None
        """

        if WINDOWS:
            self.gpu_data = get_gpu_data()

    def watch_gpu_data(self, gpu_data: list) -> None:
        """
        Watch `gpu_data` and update the Static Widget with the new information

        :param gpu_data: The list of new GPU data
        :return: None
        """

        # First, grab the Static Widget
        try:
            static = self.query_one("#gpu-static", Static)
        except NoMatches:
            return

        static_content = ""

        # Then, for each video controller, update the Static Widget with its new information
        for gpu in gpu_data:
            static_content += (
                f"[green]GPU[/]: {gpu['gpu']}\n"
                f"[green]Driver Version[/]: {gpu['driver_version']}\n"
                f"[green]Resolution[/]: {gpu['resolution']}\n"
                f"[green]Adapter RAM[/]: {gpu['adapter_ram']}\n"
                f"[green]Availability[/]: {gpu['availability']}\n"
                f"[green]Refresh[/]: {gpu['refresh']} Hz\n"
                f"[green]Status[/]: {gpu['status']}\n"
            )

        static.update(static_content)

    def on_mount(self) -> None:
        """
        Set interval to update the memory information.
        :return: None
        """
        self.update_gpu_data = self.set_interval(RARE_INTERVAL, self.update_gpu_data)

    def on_click(self) -> None:
        """
        When this pane is clicked, switch to the GPU screen
        :return: None
        """
        self.app.switch_mode("gpu")

    def compose(self) -> ComposeResult:
        """
        Generate a ComposeResult by yielding a vertically-scrolling Static widget with the GPU information.
        :return: The ComposeResult
        """

        with VerticalScroll():
            if WINDOWS:
                yield Static(id="gpu-static")
            else:
                yield Static("GPU information not currently supported on non-Windows systems...")
