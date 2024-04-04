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

        async with self.monitor_app.run_test() as pilot:
            # Make sure we are on the main screen to begin
            assert type(self.monitor_app.screen) is MainScreen

            # Go to the processes screen
            await pilot.press("p")
            assert type(self.monitor_app.screen) is ProcessesScreen
            assert self.monitor_app.screen.BORDER_TITLE == "Processes"

            # Go back to the main screen
            await pilot.press("p")
            assert type(self.monitor_app.screen) is MainScreen
            assert self.monitor_app.screen.BORDER_TITLE == ""

            # Go to the drives screen
            await pilot.press("d")
            assert type(self.monitor_app.screen) is DriveScreen
            assert self.monitor_app.screen.BORDER_TITLE == "Drive Usage"

            # Go back to the main screen
            await pilot.press("d")
            assert type(self.monitor_app.screen) is MainScreen
            assert self.monitor_app.screen.BORDER_TITLE == ""

            # Go to the memory screen
            await pilot.press("m")
            assert type(self.monitor_app.screen) is MemoryScreen
            assert self.monitor_app.screen.BORDER_TITLE == "Memory"

            # Go back to the main screen
            await pilot.press("m")
            assert type(self.monitor_app.screen) is MainScreen
            assert self.monitor_app.screen.BORDER_TITLE == ""

            # Go to the CPU screen
            await pilot.press("c")
            assert type(self.monitor_app.screen) is CPU_Screen
            assert self.monitor_app.screen.BORDER_TITLE == "CPU Usage"

            # Go back to the main screen
            await pilot.press("c")
            assert type(self.monitor_app.screen) is MainScreen
            assert self.monitor_app.screen.BORDER_TITLE == ""

            # Go to the network screen
            await pilot.press("n")
            assert type(self.monitor_app.screen) is NetworkScreen
            assert self.monitor_app.screen.BORDER_TITLE == "Network"

            # Go back to the main screen
            await pilot.press("n")
            assert type(self.monitor_app.screen) is MainScreen
            assert self.monitor_app.screen.BORDER_TITLE == ""

            # Go to the guide screen
            await pilot.press("g")
            assert type(self.monitor_app.screen) is GuideScreen
            assert self.monitor_app.screen.BORDER_TITLE == ""

            # Go back to the main screen
            await pilot.press("g")
            assert type(self.monitor_app.screen) is MainScreen
            assert self.monitor_app.screen.BORDER_TITLE == ""

    @pytest.mark.asyncio
    async def test_keys_relative(self):
        """
        Starting from the Main Screen, test that we can go to each Screen in order
        :return: None
        """

        async with self.monitor_app.run_test() as pilot:

            # Make sure we are on the main screen to begin
            assert type(self.monitor_app.screen) is MainScreen

            # Starting from the Main Screen, test going to each Screen and back
            await pilot.press("p")
            assert type(self.monitor_app.screen) is ProcessesScreen
            await pilot.press("d")
            assert type(self.monitor_app.screen) is DriveScreen
            await pilot.press("m")
            assert type(self.monitor_app.screen) is MemoryScreen
            await pilot.press("c")
            assert type(self.monitor_app.screen) is CPU_Screen
            await pilot.press("n")
            assert type(self.monitor_app.screen) is NetworkScreen
            await pilot.press("n")

            # Make sure we made it back to the Main Screen
            assert type(self.monitor_app.screen) is MainScreen

    @pytest.mark.asyncio
    async def test_keys_relative_reverse(self):
        """
        Starting from the Main Screen, test that we can go to each Screen in order but in reverse
        :return: None
        """

        async with self.monitor_app.run_test() as pilot:

            # Make sure we are on the main screen to begin
            assert type(self.monitor_app.screen) is MainScreen

            await pilot.press("n")
            assert type(self.monitor_app.screen) is NetworkScreen
            await pilot.press("c")
            assert type(self.monitor_app.screen) is CPU_Screen
            await pilot.press("m")
            assert type(self.monitor_app.screen) is MemoryScreen
            await pilot.press("d")
            assert type(self.monitor_app.screen) is DriveScreen
            await pilot.press("p")
            assert type(self.monitor_app.screen) is ProcessesScreen
            await pilot.press("p")

            # Make sure we made it back to the Main Screen
            assert type(self.monitor_app.screen) is MainScreen
