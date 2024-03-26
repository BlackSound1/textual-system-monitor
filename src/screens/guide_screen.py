from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.screen import Screen
from textual.widgets import Static, Header, Footer


DESCRIPTION_STRING = """
[bold underline]Textual System Monitor[/]

Created in Python using Textual.

- Fully live-updating monitoring for:
\t- Processes
\t- Drive Usage
\t- Memory Usage
\t- CPU Usage
\t- Network Information
\t- More coming soon?

- Dark and Light modes

- Keyboard and Mouse controls

- Quantities of bytes displayed in human-readable formats

- Color-coded percentages

- Clock

- Resizable
"""

MONITORING_STRING = """
[bold underline]Monitoring Descriptions[/]

[#FEA62B]Processes[/]: An updated list of running processes, sorted by CPU load. Each process has info on:
  - Process ID (PID)
  - CPU load (in %)
  - Application name
  - Username of the user running this process
  - The actual executable file running this process

[#FF0000]Drive Usage[/]: An updated list of drives in use by the system. Includes both storage and media drives. 
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

[#FFFF00]Memory Usage[/]: Updated info about system memory allocation:
  - Total Memory: How much memory is allocated to the system
  - Available Memory: How much is able to be used by programs/ processes
  - Used: How much is already being used
  - Percentage Used (in %): How much memory is used as a percentage of the total 

[#ADD8E6]CPU Usage[/]: Updated CPU info about:
  - Cores: The total number of cores present on the system
  - Usage (Overall) (in %): A measure of overall CPU usage
  - Usage (per Core) (in %): A measure of each CPU Cores usage

[#90EE90]Network Info[/]: An updated list of network interfaces. Each interface has info on:
  - Download amount and speed
  - Upload amount and speed
"""


class Guide(Screen):
    CSS_PATH = "../styles/guide_css.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ('g', "switch_mode('main')", 'Main Screen'),
    ]

    def compose(self) -> ComposeResult:
        """
        Generate a ComposeResult by yielding a Header, a Container with statics for the description and monitoring guide,
        and a Footer

        :return: The ComposeResult of the screen
        """

        yield Header(show_clock=True)
        with Container(id="guide-container"):
            with VerticalScroll():
                yield Static(DESCRIPTION_STRING, id="description")
            with VerticalScroll():
                yield Static(MONITORING_STRING, id="monitoring-desc")
        yield Footer()
