from typing import cast
from unittest.mock import patch

from textual.containers import Container
from textual.css.query import NoMatches
from textual.widgets import DataTable, Static

from textual_system_monitor.app import Monitor
from textual_system_monitor.panes.gpu import GPU_Usage
from textual_system_monitor.screens.gpu_screen import GPU_Screen


async def test_change_KB_base() -> None:
    """
    Test that changing the KB size works
    """
    app = Monitor()
    assert app.CONTEXT["kb_size"] == 1024
    app.action_switch_base()
    assert app.CONTEXT["kb_size"] == 1000
    app.action_switch_base()
    assert app.CONTEXT["kb_size"] == 1024


async def test_gpu_pane_gpu_data() -> None:
    """Linux platforms should have GPU data when available"""
    with patch(
        "textual_system_monitor.panes.gpu.get_gpu_data",
        return_value=[
            {
                "gpu": "MY GPU",
                "driver_version": "1",
                "resolution": "1920 x 1080",
                "adapter_ram": "1.0 GB",
                "availability": "Available",
                "refresh": "60",
                "status": "OK",
            },
        ],
    ):
        app = Monitor()
        app.CONTEXT["kb_size"] = 1000
        async with app.run_test():
            gpu_pane = app.screen.query_one(GPU_Usage)
            gpu_pane.update_gpu_data()
            assert len(gpu_pane.gpu_data) == 1
            only_item = gpu_pane.gpu_data[0]
            assert only_item["gpu"] == "MY GPU"
            assert only_item["driver_version"] == "1"
            assert only_item["resolution"] == "1920 x 1080"
            assert only_item["adapter_ram"] == "1.0 GB"
            assert only_item["availability"] == "Available"
            assert only_item["refresh"] == "60"
            assert only_item["status"] == "OK"


async def test_gpu_pane_no_gpu_data() -> None:
    """GPU pane with no GPU data has an empty list"""
    app = Monitor()
    async with app.run_test():
        with patch(
            "textual_system_monitor.panes.gpu.get_gpu_data",
            return_value=[],
        ):
            gpu_pane = app.screen.query_one(GPU_Usage)
            gpu_pane.update_gpu_data()
            assert gpu_pane.gpu_data == []
            static = gpu_pane.query_one("#gpu_pane_static", expect_type=Static)
            assert static.content == "GPU information not currently supported..."


async def test_gpu_pane_gpu_data_windows() -> None:
    """On Windows, GPU data should be populated"""

    with (
        patch(
            "textual_system_monitor.panes.gpu.get_gpu_data",
            return_value=[
                {
                    "gpu": "MY GPU",
                    "driver_version": "1",
                    "resolution": "1920 x 1080",
                    "adapter_ram": "1.0 GB",
                    "availability": "Running",
                    "refresh": "1",
                    "status": "OK",
                },
            ],
        ),
        patch("sys.platform", "win32"),
    ):
        app = Monitor()
        app.CONTEXT["kb_size"] = 1000
        async with app.run_test():
            gpu_pane = app.screen.query_one(GPU_Usage)
            gpu_pane.update_gpu_data()
            data = cast(list[dict[str, str]], gpu_pane.gpu_data)
            assert len(data) == 1
            only_item = data[0]
            assert only_item["gpu"] == "MY GPU"
            assert only_item["driver_version"] == "1"
            assert only_item["resolution"] == "1920 x 1080"
            assert only_item["adapter_ram"] == "1.0 GB"
            assert only_item["availability"] == "Running"
            assert only_item["refresh"] == "1"
            assert only_item["status"] == "OK"


async def test_gpu_pane_static_exists() -> None:
    """GPU pane static widget always exists"""
    app = Monitor()
    async with app.run_test():
        gpu_pane = app.screen.query_one(GPU_Usage)
        static = gpu_pane.query_one("#gpu_pane_static", expect_type=Static)
        assert static is not None


async def test_gpu_screen_table_exists() -> None:
    """GPU screen table widget always exists"""
    app = Monitor()
    async with app.run_test() as pilot:
        await pilot.press("v")
        await pilot.pause()
        gpu_screen = app.screen
        table = gpu_screen.query_one("#gpu-screen-table", expect_type=DataTable)
        assert table is not None


async def test_gpu_screen_no_gpu_data_message() -> None:
    """Linux platforms with no GPU data should show a not supported message in the table"""
    app = Monitor()
    async with app.run_test() as pilot:
        with patch(
            "textual_system_monitor.screens.gpu_screen.get_gpu_data",
            return_value=[],
        ):
            await pilot.press("v")
            await pilot.pause()
            gpu_screen = cast(GPU_Screen, app.screen)
            gpu_screen.update_gpu_data()
            table = gpu_screen.query_one("#gpu-screen-table", expect_type=DataTable)
            row_count = table.row_count
            assert row_count == 1
            # First cell of the first row should contain the not supported message
            first_cell = table.get_cell_at((0, 0))
            assert "not currently supported" in first_cell


async def test_gpu_screen_gpu_data_windows() -> None:
    """On Windows, GPU data should be populated"""

    with (
        patch(
            "textual_system_monitor.screens.gpu_screen.get_gpu_data",
            return_value=[
                {
                    "gpu": "MY GPU",
                    "driver_version": "1",
                    "resolution": "1920 x 1080",
                    "adapter_ram": "1.0 GB",
                    "availability": "Running",
                    "refresh": "1",
                    "status": "OK",
                },
            ],
        ),
        patch("sys.platform", "win32"),
    ):
        app = Monitor()
        app.CONTEXT["kb_size"] = 1000
        async with app.run_test() as pilot:
            await pilot.press("v")
            await pilot.pause()
            gpu_screen = cast(GPU_Screen, app.screen)
            gpu_screen.update_gpu_data()
            data = cast(list[dict[str, str]], gpu_screen.gpu_data)
            assert len(data) == 1
            only_item = data[0]
            assert only_item["gpu"] == "MY GPU"
            assert only_item["driver_version"] == "1"
            assert only_item["resolution"] == "1920 x 1080"
            assert only_item["adapter_ram"] == "1.0 GB"
            assert only_item["availability"] == "Running"
            assert only_item["refresh"] == "1"
            assert only_item["status"] == "OK"


async def test_update_gpu_screen_data() -> None:
    """On Linux, after updating GPU data on the GPU Screen, the GPU data should be a list"""
    with patch(
        "textual_system_monitor.screens.gpu_screen.get_gpu_data",
        return_value=[],
    ):
        app = Monitor()
        async with app.run_test() as pilot:
            await pilot.press("v")
            await pilot.pause()
            gpu_screen = cast(GPU_Screen, app.screen)
            gpu_screen.update_gpu_data()
            assert gpu_screen.gpu_data == []


async def test_gpu_screen_border_change() -> None:
    """Test that the `_on_theme_change` function works on the GPU Screen"""
    new_pink = "#FF1493"
    app = Monitor()
    async with app.run_test() as pilot:
        await pilot.press("v")
        await pilot.pause()
        app.theme = "textual-light"
        gpu_screen = cast(GPU_Screen, app.screen)
        container = gpu_screen.query_one("#gpu-container", expect_type=Container)
        for k, v in container.styles.border:
            assert k == "round"
            assert v.hex6 == new_pink


async def test_gpu_screen_no_container_found() -> None:
    """Make sure that if no `#gpu-container` is loaded, then `on_mount` early returns"""
    app = Monitor()
    async with app.run_test():
        gpu_screen = GPU_Screen()
        with (
            patch.object(
                gpu_screen.screen,
                "query_one",
                side_effect=NoMatches("", ""),
            ),
            patch.object(gpu_screen, "watch") as mock_watch,
        ):
            gpu_screen.on_mount()
            mock_watch.assert_not_called()
            gpu_screen.on_unmount()  # Force dismounting to kill the timer
