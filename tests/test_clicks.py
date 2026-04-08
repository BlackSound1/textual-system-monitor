from textual.screen import Screen

from src.app import Monitor
from src.screens.cpu_screen import CPU_Screen
from src.screens.drive_screen import DriveScreen
from src.screens.gpu_screen import GPU_Screen
from src.screens.main_screen import MainScreen
from src.screens.mem_screen import MemoryScreen
from src.screens.network_screen import NetworkScreen
from src.screens.processes_screen import ProcessesScreen


async def test_clicks() -> None:
    """
    From the Main Screen, click on each pane to go to its Screen. Then,
    hit the corresponding key to go back to the Main Screen
    """

    SCREENS: list[tuple[str, type[Screen[None]], str]] = [
        ("#processes", ProcessesScreen, "p"),
        ("#drives", DriveScreen, "d"),
        ("#mem", MemoryScreen, "m"),
        ("#cpu", CPU_Screen, "c"),
        ("#network", NetworkScreen, "n"),
        ("#gpu", GPU_Screen, "v"),
    ]

    app = Monitor()

    async with app.run_test() as pilot:
        # Iterate over each screen
        for screen_class, screen_type, screen_key in SCREENS:
            # Click on the screen and assert that we are on the correct screen
            await pilot.click(screen_class)
            assert type(app.screen) is screen_type

            # Press the key to go back to the main screen and assert that we are on the main screen
            await pilot.press(screen_key)
            assert type(app.screen) is MainScreen
