from psutil import disk_partitions, disk_usage
from textual.app import ComposeResult
from textual.containers import VerticalScroll, Container
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Header, DataTable

from src.utilities import compute_percentage_color, bytes2human, RARE_INTERVAL


class DriveScreen(Screen):
    BORDER_TITLE = "Drive Usage"
    BORDER_SUBTITLE = f"Updated every {RARE_INTERVAL} seconds"
    CSS_PATH = "../styles/drive_css.tcss"
    BINDINGS = [
        ("d", "switch_mode('main')", "Main Screen"),
    ]

    # Set the default disks value to an initial call to the function
    disks = reactive(
        (
            {"device": item.device, "mountpoint": item.mountpoint, "fstype": item.fstype,
             "opts": item.opts, "maxfile": item.maxfile, "maxpath": item.maxpath}
            for item in disk_partitions()
        )
    )

    def update_disks(self) -> None:
        """
        Define how to update `self.disks`
        """

        self.disks = (
            {"device": item.device, "mountpoint": item.mountpoint, "fstype": item.fstype,
             "opts": item.opts, "maxfile": item.maxfile, "maxpath": item.maxpath}
            for item in disk_partitions()
        )

    def watch_disks(self, disks: list) -> None:
        """
        Define what happens when `self.disks` changes.

        Update the Drive Usage pane with Statics for each disk
        :param disks: The list of new disks to render
        """

        # First, grab the DataTable Widget
        try:
            table = self.query_one("#drive-screen-table", expect_type=DataTable)
        except NoMatches():
            return

        table.clear(columns=True)
        table.add_columns("Drive", "Options", "Filesystem", "Usage (%)", "Total", "Used", "Free")

        # Next, go through each updated disk, get its info, and add it to the table
        for disk in disks:
            options = disk['opts']
            device = str(disk['device']).replace(":\\", '')
            fs = disk['fstype'] or 'N/A'

            # If the drive is a CD drive, treat it differently
            if options == "cdrom":
                table.add_row(device, options, "N/A", "N/A", "N/A", "N/A", "N/A")
            else:
                usage = disk_usage(disk['mountpoint'])
                pct = compute_percentage_color(usage.percent)
                used = bytes2human(usage.used)
                free = bytes2human(usage.free)
                total = bytes2human(usage.total)

                table.add_row(device, options, fs, pct, total, used, free)

    def on_mount(self) -> None:
        """
        Perform initial setup for the Drive Screen
        :return: None
        """

        self.update_disks = self.set_interval(RARE_INTERVAL, self.update_disks)

        try:
            container = self.query_one("#drive-screen-container", expect_type=Container)
        except NoMatches():
            return

        container.border_title = self.BORDER_TITLE
        container.border_subtitle = self.BORDER_SUBTITLE

    def compose(self) -> ComposeResult:
        """
        Start off with a VerticalScroll Widget with a blank Static inside
        :return: The ComposeResult featuring the VerticalScroll and Static
        """

        yield Header(show_clock=True)
        with Container(id="drive-screen-container"):
            with VerticalScroll():
                yield DataTable(id="drive-screen-table", cell_padding=2)
        yield Footer()
