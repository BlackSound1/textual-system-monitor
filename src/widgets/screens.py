from textual.app import ComposeResult
from textual.widgets import Static


class Screens(Static):

    def compose(self) -> ComposeResult:
        """
        Generates the layout for the Screens stack.

        Yields a dedicated Static widget for each Screen in the stack.
        :return: ComposeResult: The composed result of the application screen.
        """

        for screen in self.app.screen_stack:
            yield Static(f"{screen}")
