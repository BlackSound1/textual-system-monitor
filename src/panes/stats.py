from textual.app import ComposeResult
from textual.widgets import Static

from .cpu import CPU_Usage
from .drives import DriveUsage
from .gpu import GPU_Usage
from .memory import MemUsage
from .network import NetInfo


class Stats(Static):
    BORDER_TITLE = "Stats"

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
