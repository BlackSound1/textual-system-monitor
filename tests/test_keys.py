from unittest import IsolatedAsyncioTestCase

import pytest

from src.app import Monitor
from src.screens.cpu_screen import CPU_Screen
from src.screens.drive_screen import DriveScreen
from src.screens.guide_screen import GuideScreen
from src.screens.main_screen import MainScreen
from src.screens.mem_screen import MemoryScreen
from src.screens.network_screen import NetworkScreen
from src.screens.processes_screen import ProcessesScreen
from src.screens.gpu_screen import GPU_Screen


class TestKeys(IsolatedAsyncioTestCase):

    @classmethod
    async def asyncSetUp(cls):
        cls.monitor_app = Monitor()

    @pytest.mark.asyncio
    async def test_keys_main(self):
        """
        Test that we can go to each Screen from the main Screen
        :return: None
        """

        SCREENS = [
            (ProcessesScreen, "p", "Processes"),
            (DriveScreen, "d", "Drive Usage"),
            (MemoryScreen, "m", "Memory"),
            (CPU_Screen, "c", "CPU Usage"),
            (NetworkScreen, "n", "Network"),
            (GPU_Screen, "v", "GPU Info"),
            (GuideScreen, "g", "")
        ]

        async with self.monitor_app.run_test() as pilot:

            # Make sure we are on the main screen to begin
            self.assertIs(type(self.monitor_app.screen), MainScreen)

            # Go through each screen in the SCREENS list
            for screen_class, key, title in SCREENS:

                # Press the key and assert that we are on the correct screen
                await pilot.press(key)
                self.assertIs(type(self.monitor_app.screen), screen_class)
                self.assertEqual(self.monitor_app.screen.BORDER_TITLE, title)

                # Go back to the main screen and assert that we are back there
                await pilot.press(key)
                self.assertIs(type(self.monitor_app.screen), MainScreen)
                self.assertEqual(self.monitor_app.screen.BORDER_TITLE, "")

    @pytest.mark.asyncio
    async def test_keys_relative(self):
        """
        Starting from the Main Screen, test that we can go to each Screen in order
        :return: None
        """

        # Define the screens and their corresponding keys and titles
        SCREENS = [
            (ProcessesScreen, "p", "Processes"),
            (DriveScreen, "d", "Drive Usage"),
            (MemoryScreen, "m", "Memory"),
            (CPU_Screen, "c", "CPU Usage"),
            (NetworkScreen, "n", "Network"),
            (GPU_Screen, "v", "GPU Info"),
            (MainScreen, "v", ""),
        ]

        async with self.monitor_app.run_test() as pilot:

            # Make sure we are on the main screen to begin
            self.assertIs(type(self.monitor_app.screen), MainScreen)

            # Go through each screen in the SCREENS list
            for screen_class, key, title in SCREENS:

                # Press the key and assert that we are on the correct screen
                await pilot.press(key)
                self.assertIs(type(self.monitor_app.screen), screen_class)
                self.assertEqual(self.monitor_app.screen.BORDER_TITLE, title)

    @pytest.mark.asyncio
    async def test_keys_relative_reverse(self):
        """
        Starting from the Main Screen, test that we can go to each Screen in order but in reverse
        :return: None
        """

        # Define the screens and their corresponding keys
        SCREENS = [
            (GPU_Screen, "v"),
            (NetworkScreen, "n"),
            (CPU_Screen, "c"),
            (MemoryScreen, "m"),
            (DriveScreen, "d"),
            (ProcessesScreen, "p"),
            (MainScreen, "p"),
        ]

        async with self.monitor_app.run_test() as pilot:

            # Make sure we are on the main screen to begin
            self.assertIs(type(self.monitor_app.screen), MainScreen)

            # Iterate through the screens and their corresponding keys
            for screen_class, key in SCREENS:

                # Press the key and assert that we are on the correct screen
                await pilot.press(key)
                self.assertIs(type(self.monitor_app.screen), screen_class)
