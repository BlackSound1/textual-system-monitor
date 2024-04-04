from unittest import IsolatedAsyncioTestCase

import pytest
import pytest_asyncio

from src.app import Monitor
from src.screens.cpu_screen import CPU_Screen
from src.screens.drive_screen import DriveScreen
from src.screens.main_screen import MainScreen
from src.screens.mem_screen import MemoryScreen
from src.screens.network_screen import NetworkScreen
from src.screens.processes_screen import ProcessesScreen


# @pytest_asyncio.fixture()
# def monitor_app_fixture():
#     monitor_app = Monitor()
#     yield monitor_app


class TestKeys(IsolatedAsyncioTestCase):

    # @classmethod
    # async def asyncSetUp(cls):
    #     monitor_app = Monitor()
    #     cls

    @pytest.mark.asyncio
    async def test_process_screen(self):
        monitor_app = Monitor()

        async with monitor_app.run_test() as pilot:
            await pilot.press("p")

            assert type(monitor_app.screen) is ProcessesScreen

            assert monitor_app.screen.BORDER_TITLE == "Processes"

            await pilot.press("p")

            assert type(monitor_app.screen) is MainScreen

            assert monitor_app.screen.BORDER_TITLE == ""

    @pytest.mark.asyncio
    async def test_drives_screen(self):
        monitor_app = Monitor()

        async with monitor_app.run_test() as pilot:
            await pilot.press("d")

            assert type(monitor_app.screen) is DriveScreen

            assert monitor_app.screen.BORDER_TITLE == "Drive Usage"

            await pilot.press("d")

            assert type(monitor_app.screen) is MainScreen

            assert monitor_app.screen.BORDER_TITLE == ""

    @pytest.mark.asyncio
    async def test_memory_screen(self):
        monitor_app = Monitor()

        async with monitor_app.run_test() as pilot:
            await pilot.press("m")

            assert type(monitor_app.screen) is MemoryScreen

            assert monitor_app.screen.BORDER_TITLE == "Memory"

            await pilot.press("m")

            assert type(monitor_app.screen) is MainScreen

            assert monitor_app.screen.BORDER_TITLE == ""

    @pytest.mark.asyncio
    async def test_cpu_screen(self):
        monitor_app = Monitor()

        async with monitor_app.run_test() as pilot:
            await pilot.press("c")

            assert type(monitor_app.screen) is CPU_Screen

            assert monitor_app.screen.BORDER_TITLE == "CPU Usage"

            await pilot.press("c")

            assert type(monitor_app.screen) is MainScreen

            assert monitor_app.screen.BORDER_TITLE == ""

    @pytest.mark.asyncio
    async def test_network_screen(self):
        monitor_app = Monitor()

        async with monitor_app.run_test() as pilot:
            await pilot.press("n")

            assert type(monitor_app.screen) is NetworkScreen

            assert monitor_app.screen.BORDER_TITLE == "Network"

            await pilot.press("n")

            assert type(monitor_app.screen) is MainScreen

            assert monitor_app.screen.BORDER_TITLE == ""
