from unittest import IsolatedAsyncioTestCase

import pytest

from src.app import Monitor
from src.screens.cpu_screen import CPU_Screen
from src.screens.drive_screen import DriveScreen
from src.screens.main_screen import MainScreen
from src.screens.mem_screen import MemoryScreen
from src.screens.network_screen import NetworkScreen
from src.screens.processes_screen import ProcessesScreen


class TestClicks(IsolatedAsyncioTestCase):
    @classmethod
    async def asyncSetUp(cls):
        cls.monitor_app = Monitor()

    @pytest.mark.asyncio
    async def test_clicks(self):

        async with self.monitor_app.run_test() as pilot:
            # Test clicking the processes pane
            await pilot.click("#processes")
            assert type(self.monitor_app.screen) is ProcessesScreen
            assert self.monitor_app.screen.BORDER_TITLE == "Processes"
            await pilot.press("p")
            assert type(self.monitor_app.screen) is MainScreen

            # Test clicking the drives pane
            await pilot.click("#drives")
            assert type(self.monitor_app.screen) is DriveScreen
            assert self.monitor_app.screen.BORDER_TITLE == "Drive Usage"
            await pilot.press("d")
            assert type(self.monitor_app.screen) is MainScreen

            # Test clicking the memory pane
            await pilot.click("#mem")
            assert type(self.monitor_app.screen) is MemoryScreen
            assert self.monitor_app.screen.BORDER_TITLE == "Memory"
            await pilot.press("m")
            assert type(self.monitor_app.screen) is MainScreen

            # Test clicking the CPU pane
            await pilot.click("#cpu")
            assert type(self.monitor_app.screen) is CPU_Screen
            assert self.monitor_app.screen.BORDER_TITLE == "CPU Usage"
            await pilot.press("c")
            assert type(self.monitor_app.screen) is MainScreen

            # Test clicking the network pane
            await pilot.click("#network")
            assert type(self.monitor_app.screen) is NetworkScreen
            assert self.monitor_app.screen.BORDER_TITLE == "Network"
