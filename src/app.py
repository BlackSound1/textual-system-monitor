from typing import ClassVar
from collections.abc import Callable

from textual.app import App
from textual.binding import Binding
from textual.screen import Screen

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
    SCREENS: ClassVar[dict[str, Callable[[], Screen[None]]]] = {
        "main": MainScreen,
        "guide": GuideScreen,
        "processes": ProcessesScreen,
        "network": NetworkScreen,
        "cpu": CPU_Screen,
        "drive": DriveScreen,
        "mem": MemoryScreen,
        "gpu": GPU_Screen,
    }

    CONTEXT = {
        "kb_size": 1024
    }

    BINDINGS = [
        Binding(key='/', action='app.switch_base', description='Change KB Size')
    ]

    def on_mount(self) -> None:
        """
        Set the initial MainScreen screen
        """
        self.push_screen("main")

    def action_switch_base(self) -> None:
        """
        Toggles the app-wide KB size between 1000 and 1024.
        """
        self.CONTEXT['kb_size'] = 1000 if self.CONTEXT['kb_size'] == 1024 else 1024
