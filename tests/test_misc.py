from unittest.mock import patch

from textual.widgets import Static

from src.app import Monitor
from main import run
from src.panes.gpu import GPU_Usage


async def test_change_KB_base() -> None:
    """
    Test that changing the KB size works
    """
    app = Monitor()
    assert app.CONTEXT['kb_size'] == 1024
    app.action_switch_base()
    assert app.CONTEXT['kb_size'] == 1000
    app.action_switch_base()
    assert app.CONTEXT['kb_size'] == 1024


async def test_run_calls_monitor_run() -> None:
    """
    Test that when the app starts, the `run()` method calls `Monitor.run()`
    """
    with patch('src.app.Monitor.run') as mock_monitor_run:
        run()
        mock_monitor_run.assert_called_once()


async def test_gpu_pane_linux_gpu_data_empty() -> None:
    """Non-Windows platforms should have no GPU data"""
    with patch('sys.platform', 'linux'):
        gpu_pane = GPU_Usage()
        gpu_pane.update_gpu_data()
        assert gpu_pane.gpu_data == []


async def test_gpu_pane_linux_empty_Static() -> None:
    """Non-Windows platforms should have the empty version of the GPU pane static"""
    with patch('sys.platform', 'linux'):
        app = Monitor()
        async with app.run_test():
            gpu_pane = app.screen.query_one(GPU_Usage)
            static = gpu_pane.query_one("#gpu_pane_empty", expect_type=Static)
            assert static.content == "GPU information not currently supported on non-Windows systems..."
