from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Static
import wmi

from src.utilities import AVAILABILITY_MAP, bytes2human, RARE_INTERVAL


def get_gpu_data():
    wmi_object = wmi.WMI()
    gpus = wmi_object.Win32_VideoController()

    gpu_data_list = []

    for gpu in gpus:
        gpu_data_list.append({
            "GPU": gpu.Name,
            "Driver Version": gpu.DriverVersion,
            "Resolution": f"{gpu.CurrentHorizontalResolution} x {gpu.CurrentVerticalResolution}",
            "Adapter RAM": bytes2human(gpu.AdapterRAM),
            "Availability": AVAILABILITY_MAP.get(gpu.Availability),
            "Refresh": gpu.CurrentRefreshRate,
            "Status": gpu.Status,
        })

    return gpu_data_list


class GPU_Usage(Static):
    BORDER_TITLE = "GPU Info"
    BORDER_SUBTITLE = f"Updated every {RARE_INTERVAL} seconds"

    gpu_data = reactive(get_gpu_data())

    def update_gpu_data(self) -> None:
        self.gpu_data = get_gpu_data()

    def watch_gpu_data(self, gpu_data: list) -> None:

        try:
            static = self.query_one("#gpu-static", Static)
        except NoMatches:
            return

        static_content = ""

        for gpu in gpu_data:
            static_content += (
                f"GPU: {gpu['GPU']}\n"
                f"Driver Version: {gpu['Driver Version']}\n"
                f"Resolution: {gpu['Resolution']}\n"
                f"Adapter RAM: {gpu['Adapter RAM']}\n"
                f"Availability: {gpu['Availability']}\n"
                f"Refresh: {gpu['Refresh']} Hz\n"
                f"Status: {gpu['Status']}\n"
            )

        static.update(static_content)

    def on_mount(self):
        self.update_gpu_data = self.set_interval(RARE_INTERVAL, self.update_gpu_data)

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Static(id="gpu-static")
