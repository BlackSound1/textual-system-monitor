from typing import List

from psutil import disk_partitions, disk_usage
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import Static

from utilities import compute_percentage_color, bytes2human, RARE_INTERVAL


class DriveUsage(Static):
    BORDER_TITLE = "Drive Usage"

    # Set the default disks value to an initial call to the function
    disks: List[dict] = reactive(
        [
            {"device": item.device, "mountpoint": item.mountpoint, "fstype": item.fstype,
             "opts": item.opts, "maxfile": item.maxfile, "maxpath": item.maxpath}
            for item in disk_partitions()
        ]
    )

    def update_disks(self) -> None:
        """
        Define how to update `self.disks`.
        """

        self.disks = [
            {"device": item.device, "mountpoint": item.mountpoint, "fstype": item.fstype,
             "opts": item.opts, "maxfile": item.maxfile, "maxpath": item.maxpath}
            for item in disk_partitions()
        ]

    def watch_disks(self, disks: list) -> None:
        """
        Define what happens when `self.disks` changes.

        Update the Drive Usage pane with Statics for each disk
        :param disks: The list of new disks to render
        """

        # First, grab the VerticalScroll Widget and clear it
        scroll = self.query_one("VerticalScroll", expect_type=VerticalScroll)
        scroll.remove_children()

        # Next, go through each updated disk, get its info, and populate the VerticalScroll
        # Widget with a new Static for each disk
        for disk in disks:
            options = disk.get('opts')
            device = str(disk.get('device')).replace(":\\", '')
            fs = "N/A" if disk.get('fstype') == '' else disk.get('fstype')

            # If the drive is a CD drive, treat it differently
            if options == "cdrom":
                new_static = Static(f"Disk: {device} | Options: {options}")
            else:
                usage = disk_usage(disk.get('mountpoint'))
                pct = compute_percentage_color(usage.percent)
                used = bytes2human(usage.used)
                free = bytes2human(usage.free)
                total = bytes2human(usage.total)

                new_static = Static(f"Disk: {device} | Options: {options} | Filesystem: {fs} | Usage: {pct} % | "
                                    f"Total: {total} | Used: {used} | Free: {free}\n")

            scroll.mount(new_static)

    def on_mount(self) -> None:
        """
        Hook up the `update_disks` function, set to a long interval
        """
        self.update_disks = self.set_interval(RARE_INTERVAL, self.update_disks)

    def compose(self) -> ComposeResult:
        """
        Start off with a simple blank VerticalScroll Widget
        :return: The ComposeResult featuring the VerticalScroll
        """
        yield VerticalScroll()
