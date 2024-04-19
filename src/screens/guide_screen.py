from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.css.query import NoMatches
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
\t- GPU Information
\t- More coming soon?

- Dark and Light modes

- Keyboard and Mouse controls

- Quantities of bytes displayed in human-readable formats

- Color-coded percentages

- Click any pane on the main screen to get a dedicated page for that information

- Clock

- Resizable
"""

COLOR_MAP = {
    "proc_color": {"dark": "#FEA62B", "light": "#FF8C00"},
    "drive_color": {"dark": "#FF0000", "light": "#FF0000"},
    "mem_color": {"dark": "#FFFF00", "light": "#F3CD00"},
    "cpu_color": {"dark": "#ADD8E6", "light": "#7272f6"},
    "net_color": {"dark": "#90EE90", "light": "#008000"},
    "gpu_color": {"dark": "#FFC0CB", "light": "#FF1493"},
}

MONITORING_STRING = """
[bold underline]Monitoring Descriptions[/]

[{proc_color}]Processes[/]: An updated list of running processes, sorted by CPU load. Each process has info on:
  - Process ID (PID)
  - CPU load (in %)
  - Application name
  - Username of the user running this process
  - The actual executable file running this process

[{drive_color}]Drive Usage[/]: An updated list of drives in use by the system. Includes both storage and media drives. 
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

[{mem_color}]Memory Usage[/]: Updated info about system memory allocation:
  - Total Memory: How much memory is allocated to the system
  - Available Memory: How much is able to be used by programs/ processes
  - Used: How much is already being used
  - Percentage Used (in %): How much memory is used as a percentage of the total 

[{cpu_color}]CPU Usage[/]: Updated CPU info about:
  - Cores: The total number of cores present on the system
  - Usage (Overall) (in %): A measure of overall CPU usage
  - Usage (per Core) (in %): A measure of each CPU Cores usage

[{net_color}]Network Info[/]: An updated list of network interfaces. Each interface has info on:
  - Download amount and speed
  - Upload amount and speed
  
[{gpu_color}]GPU Info[/]: Updated GPU info about:
  - GPU name: The name of the GPU
  - Driver version: The version of the GPU driver
  - Resolution: The resolution of the GPU
  - Adapter RAM: How much RAM is allocated to the GPU
  - Availability: The availability of the GPU. Can have one of several different statuses
  - Refresh: The refresh rate of the GPU
  - Status: The current status of the GPU
"""


def get_formatted_monitoring_string(mode: str = "dark") -> str:
    """
    Returns a formatted string for the monitoring description based on whether light mode or dark mode is being used.
    The colors for the headings need to be selected accordingly.

    :param mode: "dark" or "light"
    :return: The formatted string with proper Rich color tags based on dark/ light mode
    """

    return MONITORING_STRING.format(**{label: color_dict[mode] for label, color_dict in COLOR_MAP.items()})


class GuideScreen(Screen):
    CSS_PATH = "../styles/guide_css.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ('t', "toggle_dark", 'Toggle dark mode'),
        ('p', "", ''),
        ('c', "", ''),
        ('n', "", ''),
        ('d', "", ''),
        ('m', "", ''),
        ('v', "", ''),
        ('g', "switch_mode('main')", 'Main Screen'),
    ]

    def action_toggle_dark(self) -> None:
        """
        Need to override this method to allow for toggling the colors appropriately

        :return: None
        """

        self.app.dark = not self.app.dark

        try:
            monitoring_static = self.query_one("#monitoring-desc", Static)
        except NoMatches:
            return

        monitoring_static.update(get_formatted_monitoring_string("dark" if self.app.dark else "light"))

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
                yield Static(get_formatted_monitoring_string("dark"), id="monitoring-desc")
        yield Footer()
