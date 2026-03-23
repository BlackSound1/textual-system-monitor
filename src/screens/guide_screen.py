from textual.app import ComposeResult
from textual.css.query import NoMatches
from textual.containers import Container, VerticalScroll
from textual.reactive import reactive
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Static, Header, Footer

from src.utilities import COMMON_INTERVAL, get_pallette


DESCRIPTION_STRING = """
[bold underline]Textual System Monitor[/]

Created in Python using Textual.

- Fully live-updating monitoring for:
\t- Processes
\t- Drive Usage
\t- Memory Usage
\t- CPU Usage
\t- Network Information
\t- GPU Information
\t- More coming soon?

- Multiple colour themes

- Keyboard and Mouse controls

- Quantities of bytes displayed in human-readable formats

- Color-coded percentages

- Click any pane on the main screen to get a dedicated page for that information

- Clock

- Resizable
"""

MONITORING_STRING = """
[bold underline]Monitoring Descriptions[/]

[{procs}]Processes[/]: An updated list of running processes, sorted by CPU load. Each process has info on:
  - Process ID (PID)
  - CPU load (in %)
  - Application name
  - Username of the user running this process
  - The actual executable file running this process

[{drives}]Drive Usage[/]: An updated list of drives in use by the system. Includes both storage and media drives.
  - If a drive is a storage drive, it will have info on:
    - Disk letter name
    - Options associated with that drive
    - Which file system is associated with that drive
    - Current usage (in %)
    - The capacity of the drive
    - How much of that capacity is used
    - How much of that capacity is free
  - If it's a media drive, info will be displayed about:
    - Disk letter name
    - Options associated with that drive

[{mem}]Memory Usage[/]: Updated info about system memory allocation:
  - Total Memory: How much memory is allocated to the system
  - Available Memory: How much is able to be used by programs/ processes
  - Used: How much is already being used
  - Percentage Used (in %): How much memory is used as a percentage of the total

[{cpu}]CPU Usage[/]: Updated CPU info about:
  - Cores: The total number of cores present on the system
  - Usage (Overall) (in %): A measure of overall CPU usage
  - Usage (per Core) (in %): A measure of each CPU Cores usage

[{net}]Network Info[/]: An updated list of network interfaces. Each interface has info on:
  - Download amount and speed
  - Upload amount and speed

[{gpu}]GPU Info[/]: Updated GPU info about:
  - GPU name: The name of the GPU
  - Driver version: The version of the GPU driver
  - Resolution: The resolution of the GPU
  - Adapter RAM: How much RAM is allocated to the GPU
  - Availability: The availability of the GPU. Can have one of several different statuses
  - Refresh: The refresh rate of the GPU
  - Status: The current status of the GPU
"""


def get_formatted_monitoring_string(theme: str) -> str:
    """
    Returns a formatted string for the monitoring description based on what theme is being used.
    The colors for the headings need to be selected accordingly.

    :param the: The currently-active color theme
    :return: The formatted string with proper Rich color tags based on color theme
    """

    return MONITORING_STRING.format(**{label: color for label, color in get_pallette(theme).items()})


class GuideScreen(Screen[None]):
    CSS_PATH = "../styles/guide_css.tcss"
    BINDINGS = [
        ("q", "app.quit", "Quit"),
        ('g', "app.switch_mode('main')", 'Main Screen'),
        ("/", "", ""),
    ]

    myTheme = reactive("textual-dark")

    update_timer: Timer | None = None

    def update_myTheme(self) -> None:
        self.myTheme = self.app.theme

    def watch_myTheme(self) -> None:
        try:
            static = self.query_one("#monitoring_desc", expect_type=Static)
        except NoMatches:
            return
        static.update(get_formatted_monitoring_string(self.myTheme))

    def on_mount(self) -> None:
        self.update_timer = self.set_interval(COMMON_INTERVAL, self.update_myTheme)

    def on_unmount(self) -> None:
        """
        Kill the timer on unmount to avoid timer-related threading issues
        """
        if self.update_timer:
            self.update_timer.stop()

    def compose(self) -> ComposeResult:
        """
        Generate a ComposeResult by yielding a Header, a Container with statics for the description
        and monitoring guide, and a Footer.

        :return: The ComposeResult of the screen.
        """

        yield Header(show_clock=True)
        with Container(id="guide-container"):
            with VerticalScroll():
                yield Static(DESCRIPTION_STRING, id="description")
            with VerticalScroll():
                yield Static(get_formatted_monitoring_string(self.myTheme), id="monitoring_desc")
        yield Footer()
