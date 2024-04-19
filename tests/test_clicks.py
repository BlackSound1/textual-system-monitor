from unittest import IsolatedAsyncioTestCase

import pytest

from src.app import Monitor
from src.screens.cpu_screen import CPU_Screen
from src.screens.drive_screen import DriveScreen
from src.screens.main_screen import MainScreen
from src.screens.mem_screen import MemoryScreen
from src.screens.network_screen import NetworkScreen
from src.screens.processes_screen import ProcessesScreen
from src.screens.gpu_screen import GPU_Screen


class TestClicks(IsolatedAsyncioTestCase):
    @classmethod
    async def asyncSetUp(cls):
        cls.monitor_app = Monitor()

    @pytest.mark.asyncio
    async def test_clicks(self):
        """
        Test clicking the different panes in the Main Screen
        :return: None
        """

        async with self.monitor_app.run_test() as pilot:

            # Test clicking the processes pane
            await pilot.click("#processes")
            self.assertIs(type(self.monitor_app.screen), ProcessesScreen)
            self.assertEqual(self.monitor_app.screen.BORDER_TITLE, "Processes")
            await pilot.press("p")
            self.assertIs(type(self.monitor_app.screen), MainScreen)

            # Test clicking the drives pane
            await pilot.click("#drives")
            self.assertIs(type(self.monitor_app.screen), DriveScreen)
            self.assertEqual(self.monitor_app.screen.BORDER_TITLE, "Drive Usage")
            await pilot.press("d")
            self.assertIs(type(self.monitor_app.screen), MainScreen)

            # Test clicking the memory pane
            await pilot.click("#mem")
            self.assertIs(type(self.monitor_app.screen), MemoryScreen)
            self.assertEqual(self.monitor_app.screen.BORDER_TITLE, "Memory")
            await pilot.press("m")
            self.assertIs(type(self.monitor_app.screen), MainScreen)

            # Test clicking the CPU pane
            await pilot.click("#cpu")
            self.assertIs(type(self.monitor_app.screen), CPU_Screen)
            self.assertEqual(self.monitor_app.screen.BORDER_TITLE, "CPU Usage")
            await pilot.press("c")
            self.assertIs(type(self.monitor_app.screen), MainScreen)

            # Test clicking the network pane
            await pilot.click("#network")
            self.assertIs(type(self.monitor_app.screen), NetworkScreen)
            self.assertEqual(self.monitor_app.screen.BORDER_TITLE, "Network")
            await pilot.press("n")
            self.assertIs(type(self.monitor_app.screen), MainScreen)

            # Test clicking the GPU pane
            await pilot.click("#gpu")
            self.assertIs(type(self.monitor_app.screen), GPU_Screen)
            self.assertEqual(self.monitor_app.screen.BORDER_TITLE, "GPU Info")
