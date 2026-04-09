from textual.widgets import Button

from src.app import Monitor
from src.screens.processes_screen import ProcessesScreen


async def test_process_screen_buttons():
    """
    Go to the Processes Screen and test the Buttons
    """

    app = Monitor()

    DELAY = 0.2

    async with app.run_test() as pilot:
        # Get the Processes Screen
        await pilot.press("p")
        process_screen = app.screen

        # Get the Buttons
        pause_button = process_screen.screen.query_one("#process-pause-button", expect_type=Button)
        sort_button = process_screen.screen.query_one("#process-sort-button", expect_type=Button)

        assert type(process_screen) is ProcessesScreen

        # Ensure initial state is correct
        assert not process_screen.paused
        assert pause_button.variant == "success"
        assert pause_button.label == "Pause"
        assert process_screen.sort
        assert sort_button.variant == "success"
        assert sort_button.label == "Sorted"

        # Press the pause button and make sure state is correct
        await pilot.click(pause_button)
        await pilot.pause(DELAY)

        assert process_screen.paused
        assert pause_button.variant == "error"
        assert pause_button.label == "Resume"
        assert process_screen.sort
        assert sort_button.variant == "success"
        assert sort_button.label == "Sorted"

        # Press the pause button again and make sure state is correct
        await pilot.click(pause_button)
        await pilot.pause(DELAY)

        assert not process_screen.paused
        assert pause_button.variant == "success"
        assert pause_button.label == "Pause"
        assert process_screen.sort
        assert sort_button.variant == "success"
        assert sort_button.label == "Sorted"

        # Press the sort button and make sure state is correct
        await pilot.click(sort_button)
        await pilot.pause(DELAY)

        assert not process_screen.paused
        assert pause_button.variant == "success"
        assert pause_button.label == "Pause"
        assert not process_screen.sort
        assert sort_button.variant == "error"
        assert sort_button.label == "Unsorted"

        # Press the sort button again and make sure state is correct
        await pilot.click(sort_button)
        await pilot.pause(DELAY)

        assert not process_screen.paused
        assert pause_button.variant == "success"
        assert pause_button.label == "Pause"
        assert process_screen.sort
        assert sort_button.variant == "success"
        assert sort_button.label == "Sorted"
