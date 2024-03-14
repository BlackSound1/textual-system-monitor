from typing import List

from psutil import disk_partitions, disk_usage
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static

from utilities import compute_percentage_color, bytes2human


class DriveUsage(Static):
    BORDER_TITLE = "Drive Usage"

    disks: List[dict] = [{"device": item.device, "mountpoint": item.mountpoint, "fstype": item.fstype,
                          "opts": item.opts, "maxfile": item.maxfile, "maxpath": item.maxpath}
                         for item in disk_partitions()]

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            for item in self.disks:
                try:
                    usage = disk_usage(item.get('mountpoint'))
                    pct = compute_percentage_color(usage.percent)
                    used = bytes2human(usage.used)
                    free = bytes2human(usage.free)
                    total = bytes2human(usage.total)
                except PermissionError:
                    pct = "N/A"
                    used = "N/A"
                    free = "N/A"
                    total = "N/A"

                fs = "N/A" if item.get('fstype') == '' else item.get('fstype')
                device = str(item.get('device')).replace(":\\", '')
                options = item.get('opts')

                yield Static(f"Disk: {device} | Options: {options} |"
                             f" Filesystem: {fs} | Usage: {pct} {'' if options == 'cdrom' else '%'} | Total: {total} | "
                             f"Used: {used} | Free: {free}\n")
