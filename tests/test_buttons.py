from unittest import IsolatedAsyncioTestCase

import pytest
from textual.widgets import Button

from src.app import Monitor
from src.screens.processes_screen import ProcessesScreen


class TestButtons(IsolatedAsyncioTestCase):

    @classmethod
    async def asyncSetUp(cls):
        cls.monitor_app = Monitor()

    @pytest.mark.asyncio
    async def test_process_screen_buttons(self):
        """
        Go to the Processes Screen and test the Buttons
        :return: None
        """

        async with self.monitor_app.run_test() as pilot:
            await pilot.press("p")

            # Get the Processes Screen
            process_screen: ProcessesScreen = self.monitor_app.screen

            # Get the Buttons
            pause_button = process_screen.query_one("#process-pause-button", expect_type=Button)
            sort_button = process_screen.query_one("#process-sort-button", expect_type=Button)

            self.assertIs(type(process_screen), ProcessesScreen)

            # Ensure initial state is correct
            self.assertIs(process_screen.paused, False)
            self.assertEqual(pause_button.variant, "success")
            self.assertEqual(str(pause_button.label), "Pause")
            self.assertIs(process_screen.sort, True)
            self.assertEqual(sort_button.variant, "success")
            self.assertEqual(str(sort_button.label), "Sorted")

            # Press the pause button and make sure state is correct
            await pilot.click("#process-pause-button")
            self.assertIs(process_screen.paused, True)
            self.assertEqual(pause_button.variant, "error")
            self.assertEqual(str(pause_button.label), "Resume")
            self.assertIs(process_screen.sort, True)
            self.assertEqual(sort_button.variant, "success")
            self.assertEqual(str(sort_button.label), "Sorted")

            # Press the pause button again and make sure state is correct
            await pilot.click("#process-pause-button")
            self.assertIs(process_screen.paused, False)
            self.assertEqual(pause_button.variant, "success")
            self.assertEqual(str(pause_button.label), "Pause")
            self.assertIs(process_screen.sort, True)
            self.assertEqual(sort_button.variant, "success")
            self.assertEqual(str(sort_button.label), "Sorted")

            # Press the sort button and make sure state is correct
            await pilot.click("#process-sort-button")
            self.assertIs(process_screen.paused, False)
            self.assertEqual(pause_button.variant, "success")
            self.assertEqual(str(pause_button.label), "Pause")
            self.assertIs(process_screen.sort, False)
            self.assertEqual(sort_button.variant, "error")
            self.assertEqual(str(sort_button.label), "Unsorted")

            # Press the sort button again and make sure state is correct
            await pilot.click("#process-sort-button")
            self.assertIs(process_screen.paused, False)
            self.assertEqual(pause_button.variant, "success")
            self.assertEqual(str(pause_button.label), "Pause")
            self.assertIs(process_screen.sort, True)
            self.assertEqual(sort_button.variant, "success")
            self.assertEqual(str(sort_button.label), "Sorted")
