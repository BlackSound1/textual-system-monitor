from unittest.mock import patch

from src.app import Monitor
from main import run


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
