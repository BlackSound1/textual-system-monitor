from psutil import net_connections
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static


class NetInfo(Static):
    BORDER_TITLE = "Network Info"

    connections = net_connections(kind='all')

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            # Get each network connection discovered
            for net in self.connections:

                # Get the info for this connection
                family = net.family.name
                type = net.type.name
                laddr_ip, laddr_port = net.laddr
                status = net.status
                pid = net.pid

                # raddr info can be an empty tuple
                try:
                    raddr_ip, raddr_port = net.raddr
                except ValueError:
                    raddr_ip, raddr_port = None, None

                # Display it
                yield Static(f"PID: {pid} | Status: {status} | Family: {family} | Type: {type} | "
                             f"Local Address: {laddr_ip}/{laddr_port} | "
                             f"Remote Address: "
                             f"{'N/A' if raddr_ip is None and raddr_port is None else f'{raddr_ip}/{raddr_port}'}\n")
