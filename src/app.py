from textual.app import App

from .screens.guide_screen import GuideScreen
from .screens.main_screen import MainScreen
from .screens.processes_screen import ProcessesScreen
from .screens.network_screen import NetworkScreen
from .screens.cpu_screen import CPU_Screen
from .screens.drive_screen import DriveScreen
from .screens.mem_screen import MemoryScreen
from .screens.gpu_screen import GPU_Screen


class Monitor(App[str]):
    TITLE = "Textual System Monitor"
    SUB_TITLE = "Written in Python using Textual"
    # SCREENS = {'main': MainScreen(), 'guide': Guide(), 'processes': ProcessesScreen()}
    MODES = {
        "main": MainScreen,
        "guide": GuideScreen,
        "processes": ProcessesScreen,
        "network": NetworkScreen,
        "cpu": CPU_Screen,
        "drive": DriveScreen,
        "mem": MemoryScreen,
        "gpu": GPU_Screen,
    }

    def on_mount(self) -> None:
        """
        Set the initial MainScreen screen

        :return: None
        """
        self.switch_mode("main")
