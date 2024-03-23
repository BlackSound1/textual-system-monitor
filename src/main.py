from textual.app import App

from guide_screen import Guide
from main_screen import MainScreen


class Monitor(App[str]):
    TITLE = "Textual System Monitor"
    SUB_TITLE = "Written in Python using Textual"
    SCREENS = {'guide': Guide()}
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ('g', "push_screen('guide')", 'Guide')
    ]

    def on_mount(self) -> None:
        """
        Set the initial MainScreen screen

        :return: None
        """
        self.main = MainScreen()
        self.push_screen(self.main)


def run() -> None:
    """
    Run the Monitor.

    :return: None
    """
    Monitor().run()


if __name__ == '__main__':
    run()
