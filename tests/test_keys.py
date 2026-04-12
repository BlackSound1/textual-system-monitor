from textual.screen import Screen

from textual_system_monitor.app import Monitor
from textual_system_monitor.screens.cpu_screen import CPU_Screen
from textual_system_monitor.screens.drive_screen import DriveScreen
from textual_system_monitor.screens.gpu_screen import GPU_Screen
from textual_system_monitor.screens.guide_screen import GuideScreen
from textual_system_monitor.screens.main_screen import MainScreen
from textual_system_monitor.screens.mem_screen import MemoryScreen
from textual_system_monitor.screens.network_screen import NetworkScreen
from textual_system_monitor.screens.processes_screen import ProcessesScreen

type ScreenListType = list[tuple[type[Screen[None]], str]]


async def test_keys_main() -> None:
    """
    Starting from the Main Screen, go to each Screen in turn and try to
    return to the Main Screen from the other Screen
    """

    SCREENS: ScreenListType = [
        (ProcessesScreen, "p"),
        (DriveScreen, "d"),
        (MemoryScreen, "m"),
        (CPU_Screen, "c"),
        (NetworkScreen, "n"),
        (GPU_Screen, "v"),
        (GuideScreen, "g"),
    ]

    app = Monitor()

    async with app.run_test() as pilot:
        # Make sure we are on the main screen to begin
        assert type(app.screen) is MainScreen

        # Go through each screen in the SCREENS list
        for screen_class, key in SCREENS:
            # Press the key and assert that we are on the correct screen
            await pilot.press(key)
            await pilot.pause()
            assert type(app.screen) is screen_class

            # Go back to the main screen and assert that we are back there
            await pilot.press(key)
            await pilot.pause()
            assert type(app.screen) is MainScreen


async def test_keys_relative() -> None:
    """
    Starting from the Main Screen, test that we can go to each Screen in order
    """

    # Define the screens and their corresponding keys and titles
    SCREENS: ScreenListType = [
        (ProcessesScreen, "p"),
        (DriveScreen, "d"),
        (MemoryScreen, "m"),
        (CPU_Screen, "c"),
        (NetworkScreen, "n"),
        (GPU_Screen, "v"),
        (MainScreen, "v"),
    ]

    app = Monitor()

    async with app.run_test() as pilot:
        # Make sure we are on the main screen to begin
        assert type(app.screen) is MainScreen

        # Go through each screen in the SCREENS list
        for screen_class, key in SCREENS:
            # Press the key and assert that we are on the correct screen
            await pilot.press(key)
            await pilot.pause()
            assert type(app.screen) is screen_class


async def test_keys_relative_reverse() -> None:
    """
    Starting from the Main Screen, test that we can go to each Screen in order but in reverse
    """

    # Define the screens and their corresponding keys
    SCREENS: ScreenListType = [
        (GPU_Screen, "v"),
        (NetworkScreen, "n"),
        (CPU_Screen, "c"),
        (MemoryScreen, "m"),
        (DriveScreen, "d"),
        (ProcessesScreen, "p"),
        (MainScreen, "p"),
    ]

    app = Monitor()

    async with app.run_test() as pilot:
        # Make sure we are on the main screen to begin
        assert type(app.screen) is MainScreen

        # Iterate through the screens and their corresponding keys
        for screen_class, key in SCREENS:
            # Press the key and assert that we are on the correct screen
            await pilot.press(key)
            await pilot.pause()
            assert type(app.screen) is screen_class
