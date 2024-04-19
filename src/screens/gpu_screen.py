import platform

from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable, Static

from src.utilities import RARE_INTERVAL, get_gpu_data

WINDOWS = platform.system() == "Windows"


class GPU_Screen(Screen):
    BORDER_TITLE = "GPU Info"
    BORDER_SUBTITLE = f"Updated every {RARE_INTERVAL} seconds"
    CSS_PATH = "../styles/gpu_css.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("t", "toggle_dark", "Toggle dark mode"),
        ("p", "switch_mode('processes')", "Processes"),
        ("c", "switch_mode('cpu')", "CPU"),
        ("n", "switch_mode('network')", "Network"),
        ("d", "switch_mode('drive')", "Drives"),
        ("m", "switch_mode('mem')", "Memory"),
        ("v", "switch_mode('main')", "Main Screen"),
    ]

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
            table = self.query_one("#gpu-screen-table", expect_type=DataTable)
        except NoMatches:
            return

        # Clear the table and add the columns
        table.clear(columns=True)
        table.add_columns("GPU", "Driver Version", "Resolution", "Adapter RAM",
                          "Availability", "Refresh", "Status")

        # Then, for each video controller, update the Static Widget with its new information
        for gpu in gpu_data:
            name = gpu['gpu']
            version = gpu['driver_version']
            resolution = gpu['resolution']
            ram = gpu['adapter_ram']
            availability = gpu['availability']
            refresh = gpu['refresh']
            status = gpu['status']

            table.add_row(name, version, resolution, ram, availability, refresh, status)

    def on_mount(self) -> None:
        """
        Perform initial setup for the GPU Screen
        :return: None
        """

        self.update_gpu_data = self.set_interval(RARE_INTERVAL, self.update_gpu_data)

        try:
            container = self.query_one("#gpu-container", expect_type=Container)
        except NoMatches:
            return

        container.border_title = self.BORDER_TITLE
        container.border_subtitle = self.BORDER_SUBTITLE

    def compose(self) -> ComposeResult:
        """
        Display the structure of the GPU Screen
        :return: The ComposeResult featuring the structure of the GPU Screen
        """

        yield Header(show_clock=True)
        with Container(id="gpu-container"):
            with VerticalScroll():
                if WINDOWS:
                    yield DataTable(id="gpu-screen-table", show_cursor=False, zebra_stripes=True)
                else:
                    yield Static("GPU information not currently supported on non-Windows systems...")
        yield Footer()
