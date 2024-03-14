from psutil import process_iter
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static


class Processes(Static):
    BORDER_TITLE = "Processes"

    processes = process_iter(['pid', 'name', 'username', 'exe'])

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            for process in self.processes:
                name = 'N/A' if process.info.get('name') == '' else process.info.get('name')
                exe = 'N/A' if process.info.get('exe') == '' else process.info.get('exe')

                yield Static(f"PID: {process.info.get('pid')} | Name: {name} | "
                             f"Username: {process.info.get('username')} | EXE: [green]{exe}[/green]\n")
