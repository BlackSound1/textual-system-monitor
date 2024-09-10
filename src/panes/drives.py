from psutil import disk_partitions, disk_usage
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Static

from ..utilities import compute_percentage_color, bytes_to_human, RARE_INTERVAL


class DriveUsage(Static):
    BORDER_TITLE = f"Drive Usage - Updated every {RARE_INTERVAL}s"

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

    def watch_disks(self, disks: list) -> None:
        """
        Define what happens when `self.disks` changes.

        Update the Drive Usage pane with Statics for each disk
        :param disks: The list of new disks to render
        """

        # First, grab the Static Widget
        try:
            static = self.query_one("Static", expect_type=Static)
        except NoMatches:
            return

        # Get KB size
        kb_size = self.app.CONTEXT['kb_size']

        static_content = ""

        # Next, go through each updated disk, get its info, and update the content of the Static with
        # the updated info for each drive
        for disk in disks:
            options = disk['opts']
            device = str(disk['device']).replace(":\\", '')
            fs = disk['fstype'] or 'N/A'

            # If the drive is a CD drive, treat it differently
            if options == "cdrom":
                static_content += f"Disk: {device} | Options: {options}\n\n"
            else:
                usage = disk_usage(disk['mountpoint'])
                pct = compute_percentage_color(usage.percent)
                used = bytes_to_human(usage.used, kb_size)
                free = bytes_to_human(usage.free, kb_size)
                total = bytes_to_human(usage.total, kb_size)

                # Add the new info for this drive to the content of the Static widget
                static_content += (f"Disk: {device} | Options: {options} | Filesystem: {fs} | Usage: {pct} % | "
                                   f"Total: {total} | Used: {used} | Free: {free}\n\n")

        # Update the content of the Static widget with the new info for all drives
        static.update(static_content)

    def on_mount(self) -> None:
        """
        Hook up the `update_disks` function, set to a long interval
        """
        self.update_disks = self.set_interval(RARE_INTERVAL, self.update_disks)

    def on_click(self) -> None:
        """
        When this pane is clicked, switch to the Network screen
        :return: None
        """
        self.app.switch_mode("drive")

    def compose(self) -> ComposeResult:
        """
        Start off with a VerticalScroll Widget with a blank Static inside
        :return: The ComposeResult featuring the VerticalScroll and Static
        """
        with VerticalScroll():
            yield Static()
