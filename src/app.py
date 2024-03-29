from textual.app import App

from .screens.guide_screen import Guide
from .screens.main_screen import MainScreen
from .screens.processes_screen import ProcessesScreen
from .screens.network_screen import NetworkScreen
from .screens.cpu_screen import CPU_Screen
from .screens.drive_screen import DriveScreen


class Monitor(App[str]):
    TITLE = "Textual System Monitor"
    SUB_TITLE = "Written in Python using Textual"
    # SCREENS = {'main': MainScreen(), 'guide': Guide(), 'processes': ProcessesScreen()}
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("t", "toggle_dark", "Toggle dark mode"),
        ("p", "switch_mode('processes')", "Processes"),
        ("c", "switch_mode('cpu')", "CPU"),
        ("n", "switch_mode('network')", "Network"),
        ("d", "switch_mode('drive')", "Drives"),
    ]
    MODES = {
        "main": MainScreen,
        "guide": Guide,
        "processes": ProcessesScreen,
        "network": NetworkScreen,
        "cpu": CPU_Screen,
        "drive": DriveScreen,
    }

    def on_mount(self) -> None:
        """
        Set the initial MainScreen screen

        :return: None
        """
        self.switch_mode("main")
