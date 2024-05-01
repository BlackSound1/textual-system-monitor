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

        # Define the screens to be tested
        SCREENS = [
            ("#processes", ProcessesScreen, "Processes", 'p'),
            ("#drives", DriveScreen, "Drive Usage", 'd'),
            ("#mem", MemoryScreen, "Memory", 'm'),
            ("#cpu", CPU_Screen, "CPU Usage", 'c'),
            ("#network", NetworkScreen, "Network", 'n'),
            ("#gpu", GPU_Screen, "GPU Info", 'v')
        ]

        async with self.monitor_app.run_test() as pilot:

            # Iterate over each screen
            for screen_class, screen_type, screen_title, screen_key in SCREENS:

                # Click on the screen and assert that we are on the correct screen
                await pilot.click(screen_class)
                self.assertIs(type(self.monitor_app.screen), screen_type)
                self.assertEqual(self.monitor_app.screen.BORDER_TITLE, screen_title)

                # Press the key to go back to the main screen and assert that we are on the main screen
                await pilot.press(screen_key)
                self.assertIs(type(self.monitor_app.screen), MainScreen)
