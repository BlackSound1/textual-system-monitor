from textual import getters
from textual.app import ComposeResult
from textual.widgets import Static

from src.utilities import get_pallette

from .cpu import CPU_Usage
from .drives import DriveUsage
from .gpu import GPU_Usage
from .memory import MemUsage
from .network import NetInfo


class Stats(Static):
    BORDER_TITLE = "Stats"

    drives = getters.query_one(DriveUsage)
    mem = getters.query_one(MemUsage)
    cpu = getters.query_one(CPU_Usage)
    net = getters.query_one(NetInfo)
    gpu = getters.query_one(GPU_Usage)

    def on_mount(self) -> None:
        """
        Perform initial setup for the Main Screen
        """
        def _on_theme_change() -> None:
            """
            Update the border colors based on the theme
            """
            palette = get_pallette(self.app.theme)

            self.drives.styles.border = ('round', palette['drives'])
            self.mem.styles.border = ('round', palette['mem'])
            self.cpu.styles.border = ('round', palette['cpu'])
            self.net.styles.border = ('round', palette['net'])
            self.gpu.styles.border = ('round', palette['gpu'])

        self.watch(self.app, "theme", _on_theme_change, init=False)

    def compose(self) -> ComposeResult:
        """
        Method to compose and yield DriveUsage, MemUsage, CPU_Usage, and NetInfo objects.

        :return: A ComposeResult object.
        """
        yield DriveUsage(id="drives")
        yield MemUsage(id="mem")
        yield CPU_Usage(id="cpu")
        yield NetInfo(id='network')
        yield GPU_Usage(id="gpu")
