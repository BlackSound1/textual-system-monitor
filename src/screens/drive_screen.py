from typing import cast

from psutil import disk_partitions, disk_usage
from textual import getters
from textual.app import ComposeResult
from textual.containers import VerticalScroll, Container
from textual.reactive import reactive
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Footer, Header, DataTable

from src.utilities import compute_percentage_color, bytes_to_human, RARE_INTERVAL, get_pallette


class DriveScreen(Screen[None]):
    BORDER_TITLE = f"Drive Usage - Updated every {RARE_INTERVAL}s"
    CSS_PATH = "../styles/drive_css.tcss"
    BINDINGS = [
        ("q", "app.quit", "Quit"),
        ("p", "app.switch_mode('processes')", "Processes"),
        ("c", "app.switch_mode('cpu')", "CPU"),
        ("n", "app.switch_mode('network')", "Network"),
        ("d", "app.switch_mode('main')", "Main Screen"),
        ("m", "app.switch_mode('mem')", "Memory"),
        ("v", "app.switch_mode('gpu')", "GPU"),
    ]

    update_timer: Timer | None = None

    # Set the default disks value to an initial call to the function
    disks = reactive(
        {
            "device": item.device,
            "mountpoint": item.mountpoint,
            "fstype": item.fstype,
            "opts": item.opts,
        }
        for item in disk_partitions()
    )

    table = getters.query_one("#drive-screen-table", expect_type=DataTable)
    container = getters.query_one("#drive-screen-container", expect_type=Container)

    def update_disks(self) -> None:
        """
        Define how to update `self.disks`
        """
        self.disks = (
            {
                "device": item.device,
                "mountpoint": item.mountpoint,
                "fstype": item.fstype,
                "opts": item.opts,
            }
            for item in disk_partitions()
        )

    def watch_disks(self, disks: list[dict[str, str]]) -> None:
        """
        Define what happens when `self.disks` changes.

        Update the Drive Usage pane with Statics for each disk

        :param disks: The list of new disks to render
        """

        from src.app import Monitor

        kb_size = cast(Monitor, self.app).CONTEXT['kb_size']

        self.table.clear(columns=True)
        self.table.add_columns("Drive", "Options", "Filesystem", "Usage (%)", "Total", "Used", "Free")

        # Next, go through each updated disk, get its info, and add it to the table
        for disk in disks:
            options = disk['opts']
            device = disk['device']
            fs = disk['fstype'] or 'N/A'

            # If the drive is a CD drive, treat it differently
            if options == "cdrom":
                self.table.add_row(device, options, "N/A", "N/A", "N/A", "N/A", "N/A")
            else:
                usage = disk_usage(disk['mountpoint'])
                pct = compute_percentage_color(usage.percent)
                used = bytes_to_human(usage.used, kb_size)
                free = bytes_to_human(usage.free, kb_size)
                total = bytes_to_human(usage.total, kb_size)

                self.table.add_row(device, options, fs, pct, total, used, free)

    def on_mount(self) -> None:
        """
        Perform initial setup for the Drive Screen
        """
        self.update_timer = self.set_interval(RARE_INTERVAL, self.update_disks)
        self.container.border_title = self.BORDER_TITLE
        self.container.styles.border = ('round', get_pallette(self.app.theme)['drives'])

        def _on_theme_change() -> None:
            """
            Update the border color based on the theme
            """
            self.container.styles.border = ('round', get_pallette(self.app.theme)['drives'])

        self.watch(self.app, "theme", _on_theme_change, init=False)

    def on_unmount(self) -> None:
        """
        Kill the timer on unmount to avoid timer-related threading issues
        """
        if self.update_timer:
            self.update_timer.stop()

    def compose(self) -> ComposeResult:
        """
        Create the structure of the Drive Screen

        :return: The ComposeResult featuring the Drive Screen structure
        """
        yield Header(show_clock=True)
        with Container(id="drive-screen-container"):
            with VerticalScroll():
                yield DataTable(id="drive-screen-table", cell_padding=2, show_cursor=False, zebra_stripes=True)
        yield Footer()
