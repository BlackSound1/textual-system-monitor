from textual.app import App

from .screens.guide_screen import Guide
from .screens.main_screen import MainScreen
from .screens.processes_screen import ProcessesScreen


class Monitor(App[str]):
    TITLE = "Textual System Monitor"
    SUB_TITLE = "Written in Python using Textual"
    SCREENS = {'guide': Guide(), 'processes': ProcessesScreen()}
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ('g', "push_screen('guide')", 'Guide')
    ]

    def on_mount(self) -> None:
        """
        Set the initial MainScreen screen

        :return: None
        """
        self.main = MainScreen()
        self.push_screen(self.main)
