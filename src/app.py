from textual.app import App

from .screens.guide_screen import Guide
from .screens.main_screen import MainScreen
from .screens.processes_screen import ProcessesScreen
from .screens.network_screen import NetworkScreen


class Monitor(App[str]):
    TITLE = "Textual System Monitor"
    SUB_TITLE = "Written in Python using Textual"
    # SCREENS = {'main': MainScreen(), 'guide': Guide(), 'processes': ProcessesScreen()}
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]
    MODES = {
        "main": MainScreen,
        "guide": Guide,
        "processes": ProcessesScreen,
        "network": NetworkScreen
    }

    def on_mount(self) -> None:
        """
        Set the initial MainScreen screen

        :return: None
        """
        self.switch_mode("main")
        # self.main = self.SCREENS['main']
        # self.push_screen(self.main)
