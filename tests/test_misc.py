from typing import cast
from unittest.mock import patch

from textual.containers import Container
from textual.css.query import NoMatches
from textual.widgets import Static

from src.app import Monitor
from main import run
from src.panes.gpu import GPU_Usage
from src.screens.gpu_screen import GPU_Screen


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


async def test_gpu_pane_linux_gpu_data_nonwindows() -> None:
    """Non-Windows platforms should have no GPU data"""
    with patch('sys.platform', 'linux'):
        gpu_pane = GPU_Usage()
        gpu_pane.update_gpu_data()
        assert gpu_pane.gpu_data == []


@patch('src.panes.gpu.get_gpu_data', return_value=[
    {
        'gpu': 'MY GPU',
        'driver_version': '1',
        'resolution': '1920 x 1080',
        'adapter_ram': '1.0 GB',
        'availability': 'Running',
        'refresh': '1',
        'status': 'OK',
    },
])
async def test_gpu_pane_gpu_data_windows(_: list[dict[str, str]]) -> None:
    """On Windows, GPU data should be populated"""
    with patch('sys.platform', 'win32'):
        app = Monitor()
        app.CONTEXT['kb_size'] = 1000
        async with app.run_test():
            gpu_pane = app.screen.query_one(GPU_Usage)
            gpu_pane.update_gpu_data()
            data = cast(list[dict[str, str]], gpu_pane.gpu_data)
            assert len(data) == 1
            only_item = data[0]
            assert only_item['gpu'] == 'MY GPU'
            assert only_item['driver_version'] == '1'
            assert only_item['resolution'] == '1920 x 1080'
            assert only_item['adapter_ram'] == '1.0 GB'
            assert only_item['availability'] == 'Running'
            assert only_item['refresh'] == '1'
            assert only_item['status'] == 'OK'


async def test_gpu_pane_linux_empty_Static() -> None:
    """Non-Windows platforms should have the empty version of the GPU pane static"""
    with patch('sys.platform', 'linux'):
        app = Monitor()
        async with app.run_test():
            gpu_pane = app.screen.query_one(GPU_Usage)
            static = gpu_pane.query_one("#gpu_pane_empty", expect_type=Static)
            assert static.content == "GPU information not currently supported on non-Windows systems..."


async def test_gpu_screen_linux_empty_Static() -> None:
    """Make sure Linux has an empty Static on the GPU screen"""
    with patch('sys.platform', 'linux'):
        app = Monitor()
        async with app.run_test() as pilot:
            await pilot.press('v')
            await pilot.pause()
            gpu_screen = app.screen
            static = gpu_screen.query_one('#gpu_screen_empty', expect_type=Static)
            assert static.content == "GPU information not currently supported on non-Windows systems..."


@patch('src.screens.gpu_screen.get_gpu_data', return_value=[
    {
        'gpu': 'MY GPU',
        'driver_version': '1',
        'resolution': '1920 x 1080',
        'adapter_ram': '1.0 GB',
        'availability': 'Running',
        'refresh': '1',
        'status': 'OK',
    },
])
async def test_gpu_screen_gpu_data_windows(_: list[dict[str, str]]) -> None:
    """On Windows, GPU data should be populated"""
    with patch('sys.platform', 'win32'):
        app = Monitor()
        app.CONTEXT['kb_size'] = 1000
        async with app.run_test() as pilot:
            await pilot.press('v')
            await pilot.pause()
            gpu_screen = cast(GPU_Screen, app.screen)
            gpu_screen.update_gpu_data()
            data = cast(list[dict[str, str]], gpu_screen.gpu_data)
            assert len(data) == 1
            only_item = data[0]
            assert only_item['gpu'] == 'MY GPU'
            assert only_item['driver_version'] == '1'
            assert only_item['resolution'] == '1920 x 1080'
            assert only_item['adapter_ram'] == '1.0 GB'
            assert only_item['availability'] == 'Running'
            assert only_item['refresh'] == '1'
            assert only_item['status'] == 'OK'


async def test_update_gpu_screen_data_on_linux() -> None:
    """On Linux, after updating GPU data on the GPU Screen, the GPU data should be None"""
    with patch('sys.platform', 'linux'):
        app = Monitor()
        async with app.run_test() as pilot:
            await pilot.press('v')
            await pilot.pause()
            gpu_screen = cast(GPU_Screen, app.screen)
            gpu_screen.update_gpu_data()
            assert gpu_screen.gpu_data is None


async def test_gpu_screen_border_change() -> None:
    """Test that the `_on_theme_change` function works on the GPU Screen"""
    new_pink = '#FF1493'
    app = Monitor()
    async with app.run_test() as pilot:
        await pilot.press('v')
        await pilot.pause()
        app.theme = 'textual-light'
        gpu_screen = cast(GPU_Screen, app.screen)
        container = gpu_screen.query_one("#gpu-container", expect_type=Container)
        for k, v in container.styles.border:
            assert k == 'round'
            assert v.hex6 == new_pink


async def test_gpu_screen_no_container_found() -> None:
    """Make sure that if no `#gpu-container` is loaded, then `on_mount` early returns"""
    app = Monitor()
    async with app.run_test():
        gpu_screen = GPU_Screen()
        with patch.object(gpu_screen.screen, 'query_one', side_effect=NoMatches('', '')):
            with patch.object(gpu_screen, 'watch') as mock_watch:
                gpu_screen.on_mount()
                mock_watch.assert_not_called()
                gpu_screen.on_unmount()  # Force dismounting to kill the timer
