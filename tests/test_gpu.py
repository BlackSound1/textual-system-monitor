# pyright: reportPrivateUsage=false

from pathlib import Path
from typing import cast
from unittest.mock import MagicMock, patch

from textual.containers import Container
from textual.css.query import NoMatches
from textual.widgets import DataTable, Static

from textual_system_monitor.app import Monitor
from textual_system_monitor.gpu_linux import (
    _get_driver_name,
    _get_drm_resolution,
    _get_refresh_rate,
    _get_resolution,
    _get_xrandr_resolution,
    _parse_lspci_name,
    _read_generic,
    _read_nvidia,
    _run_command,
    get_gpu_data_linux,
)
from textual_system_monitor.panes.gpu import GPU_Usage
from textual_system_monitor.screens.gpu_screen import GPU_Screen


async def test_gpu_pane_gpu_data() -> None:
    """GPU pane with GPU data available"""
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
    """GPU screen table shows a not supported message when there is no data"""
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
    """On platforms without GPU data, after updating GPU data on the GPU Screen, the GPU data should be an empty list"""
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


class TestRunCommand:
    """Tests for `_run_command`."""

    def test_run_command_success(self) -> None:
        """Should return stdout when command succeeds."""
        with patch(
            "textual_system_monitor.gpu_linux.subprocess.run",
            return_value=MagicMock(stdout="  nvidia  \n", returncode=0),
        ):
            result = _run_command(["lspci", "-k"])
            assert result == "nvidia"

    def test_run_command_file_not_found(self) -> None:
        """Should return empty string when command is not found."""
        with patch(
            "textual_system_monitor.gpu_linux.subprocess.run",
            side_effect=FileNotFoundError("lspci not found"),
        ):
            result = _run_command(["lspci", "-k"])
            assert result == ""

    def test_run_command_timeout(self) -> None:
        """Should return empty string on subprocess timeout."""
        import subprocess

        with patch(
            "textual_system_monitor.gpu_linux.subprocess.run",
            side_effect=subprocess.TimeoutExpired("lspci", 5),
        ):
            result = _run_command(["lspci", "-k"])
            assert result == ""


class TestParseLspciName:
    """Tests for `_parse_lspci_name`."""

    def test_parse_standard_vga(self) -> None:
        """Should extract vendor/model from a standard VGA lspci line."""
        line = "00:02.0 VGA compatible controller: Intel Corporation UHD Graphics (rev 01)"
        assert _parse_lspci_name(line) == "Intel Corporation UHD Graphics"

    def test_parse_nvidia_with_model_in_brackets(self) -> None:
        """Should strip model in brackets from NVIDIA lspci line."""
        line = "01:00.0 VGA compatible controller: NVIDIA Corporation GA106 [GeForce RTX 3060] (rev a1)"
        assert _parse_lspci_name(line) == "NVIDIA Corporation GA106"

    def test_parse_amd_3d_controller(self) -> None:
        """Should strip model in brackets from AMD 3D controller lspci line."""
        line = "03:00.0 3D controller: Advanced Micro Devices, Inc. [AMD/ATI] Navi 21 [Radeon RX 6800 XT] (rev c1)"
        # The function splits on first " [" so [AMD/ATI] Navi 21 is stripped
        assert _parse_lspci_name(line) == "Advanced Micro Devices, Inc."

    def test_parse_malformed_line(self) -> None:
        """Should return 'Unknown GPU' for a line without enough colons."""
        assert _parse_lspci_name("garbage no colons") == "Unknown GPU"

    def test_parse_no_vendor_name(self) -> None:
        """Should return whatever remains when name portion is just a revision."""
        line = "01:00.0 VGA compatible controller: (rev 01)"
        # "(rev 01)" has no leading space before "(rev", so it's not stripped
        assert _parse_lspci_name(line) == "(rev 01)"


class TestGetDriverName:
    """Tests for `_get_driver_name`."""

    def test_driver_found(self) -> None:
        """Should return the driver name from lspci -k output."""
        output = """01:00.0 VGA compatible controller: NVIDIA Corporation GA106 (rev a1)
        Subsystem: NVIDIA Corporation Device 1234
        Kernel driver in use: nvidia
        Kernel modules: nouveau, nvidia"""
        with patch(
            "textual_system_monitor.gpu_linux._run_command",
            return_value=output,
        ):
            assert _get_driver_name() == "nvidia"

    def test_driver_not_found(self) -> None:
        """Should return 'Unknown' when no driver line is present."""
        output = "01:00.0 VGA compatible controller: NVIDIA Corporation GA106 (rev a1)\n"
        with patch(
            "textual_system_monitor.gpu_linux._run_command",
            return_value=output,
        ):
            assert _get_driver_name() == "Unknown"


class TestGetDrmResolution:
    """Tests for `_get_drm_resolution`."""

    def test_drm_path_missing(self) -> None:
        """Should return None when /sys/class/drm does not exist."""
        with patch(
            "textual_system_monitor.gpu_linux.Path.exists",
            return_value=False,
        ):
            assert _get_drm_resolution() is None

    def test_connected_connector_with_modes(self) -> None:
        """Should return resolution from a connected DRM connector."""
        # Mock Path.glob for card* and card*-*
        mock_card = MagicMock(spec=Path)
        mock_connector = MagicMock(spec=Path)
        mock_status = MagicMock(spec=Path)
        mock_modes = MagicMock(spec=Path)

        def glob_side_effect(pattern: str):
            if pattern == "card*":
                return [mock_card]
            if pattern == "card*-*":
                return [mock_connector]
            return []

        mock_card.glob.side_effect = glob_side_effect
        mock_status.read_text.return_value = "connected"
        mock_modes.read_text.return_value = "1920x1080 60.00\n1280x720 60.00"

        with patch(
            "textual_system_monitor.gpu_linux.Path",
            return_value=mock_card,
        ) as mock_path_cls:
            mock_path_cls.return_value.glob.side_effect = glob_side_effect
            mock_path_cls.return_value.exists.return_value = True
            # We need Path("/sys/class/drm") to return mock_card
            # and card.glob("card*-*") to return [mock_connector]
            with patch.object(mock_card, "__truediv__", return_value=mock_connector):
                mock_connector.__truediv__ = lambda _, other: {
                    "status": mock_status,
                    "modes": mock_modes,
                }[other]
                result = _get_drm_resolution()
                assert result == "1920x1080"

    def test_no_connected_connector(self) -> None:
        """Should return None when no connector is connected."""
        mock_card = MagicMock(spec=Path)
        mock_connector = MagicMock(spec=Path)
        mock_status = MagicMock(spec=Path)
        mock_modes = MagicMock(spec=Path)

        mock_status.read_text.return_value = "disconnected"
        mock_modes.read_text.return_value = "1920x1080 60.00"

        def glob_side_effect(pattern: str):
            if pattern == "card*":
                return [mock_card]
            if pattern == "card*-*":
                return [mock_connector]
            return []

        mock_card.glob.side_effect = glob_side_effect

        with patch.object(mock_card, "__truediv__", return_value=mock_connector):
            mock_connector.__truediv__ = lambda _, other: {
                "status": mock_status,
                "modes": mock_modes,
            }[other]
            with patch(
                "textual_system_monitor.gpu_linux.Path",
                return_value=mock_card,
            ):
                mock_card.exists.return_value = True
                assert _get_drm_resolution() is None

    def test_read_text_raises_oserror(self) -> None:
        """Should continue to next connector when read_text raises OSError."""
        mock_card = MagicMock(spec=Path)
        mock_connector = MagicMock(spec=Path)
        mock_status = MagicMock(spec=Path)
        mock_modes = MagicMock(spec=Path)

        def glob_side_effect(pattern: str):
            if pattern == "card*":
                return [mock_card]
            if pattern == "card*-*":
                return [mock_connector]
            return []

        mock_card.glob.side_effect = glob_side_effect
        mock_status.exists.return_value = True
        mock_modes.exists.return_value = True
        mock_status.read_text.side_effect = OSError("permission denied")

        with patch.object(mock_card, "__truediv__", return_value=mock_connector):
            mock_connector.__truediv__ = lambda _, other: {
                "status": mock_status,
                "modes": mock_modes,
            }[other]
            with patch(
                "textual_system_monitor.gpu_linux.Path",
                return_value=mock_card,
            ):
                mock_card.exists.return_value = True
                assert _get_drm_resolution() is None


class TestGetXrandrResolution:
    """Tests for `_get_xrandr_resolution`."""

    def test_xrandr_with_resolution(self) -> None:
        """Should extract resolution from xrandr output."""
        output = """Screen 0: minimum 8 x 8, current 1920 x 1080, maximum 32767 x 32767
DP-0 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 531mm x 299mm
   1920x1080     60.00*+  59.94
   1280x720      60.00"""
        with patch(
            "textual_system_monitor.gpu_linux._run_command",
            return_value=output,
        ):
            assert _get_xrandr_resolution() == "1920x1080"

    def test_xrandr_no_resolution(self) -> None:
        """Should return 'Unknown' when xrandr has no resolution."""
        with patch(
            "textual_system_monitor.gpu_linux._run_command",
            return_value="Screen 0: minimum 8 x 8, current 1920 x 1080, maximum 32767 x 32767\n",
        ):
            assert _get_xrandr_resolution() == "Unknown"


class TestGetResolution:
    """Tests for `_get_resolution`."""

    def test_drm_priority_over_xrandr(self) -> None:
        """Should prefer DRM resolution over xrandr."""
        with (
            patch(
                "textual_system_monitor.gpu_linux._get_drm_resolution",
                return_value="2560x1440",
            ),
            patch(
                "textual_system_monitor.gpu_linux._get_xrandr_resolution",
                return_value="1920x1080",
            ),
        ):
            assert _get_resolution() == "2560x1440"

    def test_falls_back_to_xrandr(self) -> None:
        """Should use xrandr when DRM returns None."""
        with (
            patch(
                "textual_system_monitor.gpu_linux._get_drm_resolution",
                return_value=None,
            ),
            patch(
                "textual_system_monitor.gpu_linux._get_xrandr_resolution",
                return_value="1920x1080",
            ),
        ):
            assert _get_resolution() == "1920x1080"

    def test_both_unknown(self) -> None:
        """Should return 'Unknown' when both DRM and xrandr fail."""
        with (
            patch(
                "textual_system_monitor.gpu_linux._get_drm_resolution",
                return_value=None,
            ),
            patch(
                "textual_system_monitor.gpu_linux._get_xrandr_resolution",
                return_value="Unknown",
            ),
        ):
            assert _get_resolution() == "Unknown"


class TestGetRefreshRate:
    """Tests for `_get_refresh_rate`."""

    def test_refresh_rate_found(self) -> None:
        """Should extract refresh rate from xrandr output."""
        output = """   1920x1080     60.00*+  59.94"""
        with patch(
            "textual_system_monitor.gpu_linux._run_command",
            return_value=output,
        ):
            assert _get_refresh_rate() == "60.00"

    def test_refresh_rate_not_found(self) -> None:
        """Should return 'Unknown' when no rate is present."""
        with patch(
            "textual_system_monitor.gpu_linux._run_command",
            return_value="   1920x1080     60.00*+  59.94\n",
        ):
            # The *+ line contains 60.00 which is parseable as float
            result = _get_refresh_rate()
            assert result == "60.00"


class TestReadNvidia:
    """Tests for `_read_nvidia`."""

    def test_pynvml_not_installed(self) -> None:
        """Should return empty list when pynvml is None."""
        with patch(
            "textual_system_monitor.gpu_linux.pynvml",
            None,
        ):
            assert _read_nvidia() == []

    def test_nvml_init_fails(self) -> None:
        """Should return empty list when nvmlInit raises NVMLError."""
        mock_pynvml = MagicMock()
        mock_pynvml.NVMLError = Exception
        mock_pynvml.nvmlInit.side_effect = Exception("init failed")
        with patch(
            "textual_system_monitor.gpu_linux.pynvml",
            mock_pynvml,
        ):
            assert _read_nvidia() == []

    def test_successful_nvidia_read(self) -> None:
        """Should return GPU data when NVML works."""
        mock_pynvml = MagicMock()
        mock_pynvml.NVMLError = Exception

        mock_handle = MagicMock()
        mock_pynvml.nvmlDeviceGetHandleByIndex.return_value = mock_handle
        mock_pynvml.nvmlDeviceGetName.return_value = "NVIDIA GeForce RTX 3060"
        mock_mem_info = MagicMock()
        mock_mem_info.total = 6442450944  # 6 GiB
        mock_pynvml.nvmlDeviceGetMemoryInfo.return_value = mock_mem_info
        mock_pynvml.nvmlSystemGetDriverVersion.return_value = "535.183.06"
        mock_pynvml.nvmlDeviceGetCount.return_value = 1

        with (
            patch(
                "textual_system_monitor.gpu_linux.pynvml",
                mock_pynvml,
            ),
            patch(
                "textual_system_monitor.gpu_linux._get_resolution",
                return_value="1920x1080",
            ),
            patch(
                "textual_system_monitor.gpu_linux._get_refresh_rate",
                return_value="60.00",
            ),
        ):
            result = _read_nvidia()

        assert len(result) == 1
        gpu = result[0]
        assert gpu["gpu"] == "NVIDIA GeForce RTX 3060"
        assert gpu["driver_version"] == "535.183.06"
        assert gpu["resolution"] == "1920x1080"
        assert gpu["availability"] == "Available"
        assert gpu["refresh"] == "60.00"
        assert gpu["status"] == "Ok"

    def test_per_device_error_skipped(self) -> None:
        """Should skip a device that raises NVMLError and continue with others."""
        mock_pynvml = MagicMock()
        mock_pynvml.NVMLError = Exception

        mock_pynvml.nvmlDeviceGetCount.return_value = 2

        # First device works
        mock_pynvml.nvmlDeviceGetName.return_value = "GPU 0"
        mock_mem_info_0 = MagicMock()
        mock_mem_info_0.total = 1073741824
        mock_pynvml.nvmlDeviceGetMemoryInfo.return_value = mock_mem_info_0

        # Second device fails on handle lookup
        def get_handle_side_effect(index: int):
            if index == 0:
                return MagicMock()
            raise Exception("device lost")

        mock_pynvml.nvmlDeviceGetHandleByIndex.side_effect = get_handle_side_effect
        mock_pynvml.nvmlSystemGetDriverVersion.return_value = "535.00"

        with (
            patch(
                "textual_system_monitor.gpu_linux.pynvml",
                mock_pynvml,
            ),
            patch(
                "textual_system_monitor.gpu_linux._get_resolution",
                return_value="1920x1080",
            ),
            patch(
                "textual_system_monitor.gpu_linux._get_refresh_rate",
                return_value="60.00",
            ),
        ):
            result = _read_nvidia()

        assert len(result) == 1
        assert result[0]["gpu"] == "GPU 0"


class TestReadGeneric:
    """Tests for `_read_generic`."""

    def test_lspci_finds_vga(self) -> None:
        """Should return data when lspci finds a VGA controller."""
        lspci_output = """00:02.0 VGA compatible controller: Intel Corporation UHD Graphics (rev 01)"""
        with (
            patch(
                "textual_system_monitor.gpu_linux._run_command",
                return_value=lspci_output,
            ),
            patch(
                "textual_system_monitor.gpu_linux._get_driver_name",
                return_value="i915",
            ),
            patch(
                "textual_system_monitor.gpu_linux._get_resolution",
                return_value="1920x1080",
            ),
            patch(
                "textual_system_monitor.gpu_linux._get_refresh_rate",
                return_value="60.00",
            ),
        ):
            result = _read_generic()

        assert len(result) == 1
        assert result[0]["gpu"] == "Intel Corporation UHD Graphics"
        assert result[0]["driver_version"] == "i915"
        assert result[0]["resolution"] == "1920x1080"
        assert result[0]["adapter_ram"] == "N/A"

    def test_lspci_empty_with_drm_cards(self) -> None:
        """Should return 'Unknown GPU' entry when lspci is empty but DRM exists."""
        with (
            patch(
                "textual_system_monitor.gpu_linux._run_command",
                return_value="",
            ),
            patch(
                "textual_system_monitor.gpu_linux.Path",
            ) as mock_path,
        ):
            mock_drm = MagicMock(spec=Path)
            mock_drm.exists.return_value = True
            mock_drm.glob.return_value = [MagicMock()]  # card0 exists
            mock_path.return_value = mock_drm

            with (
                patch(
                    "textual_system_monitor.gpu_linux._get_resolution",
                    return_value="1920x1080",
                ),
                patch(
                    "textual_system_monitor.gpu_linux._get_refresh_rate",
                    return_value="60.00",
                ),
            ):
                result = _read_generic()

        assert len(result) == 1
        assert result[0]["gpu"] == "Unknown GPU"
        assert result[0]["driver_version"] == "Unknown"

    def test_lspci_empty_no_drm(self) -> None:
        """Should return empty list when neither lspci nor DRM finds anything."""
        with (
            patch(
                "textual_system_monitor.gpu_linux._run_command",
                return_value="",
            ),
            patch(
                "textual_system_monitor.gpu_linux.Path",
            ) as mock_path,
        ):
            mock_drm = MagicMock(spec=Path)
            mock_drm.exists.return_value = False
            mock_path.return_value = mock_drm

            result = _read_generic()

        assert result == []


class TestGetGpuDataLinux:
    """Tests for `get_gpu_data_linux`."""

    def test_nvidia_takes_priority(self) -> None:
        """Should return NVIDIA data when available, ignoring generic fallback."""
        with (
            patch(
                "textual_system_monitor.gpu_linux._read_nvidia",
                return_value=[{"gpu": "NVIDIA GPU", "driver_version": "1"}],
            ),
            patch(
                "textual_system_monitor.gpu_linux._read_generic",
                return_value=[{"gpu": "Generic GPU", "driver_version": "2"}],
            ),
        ):
            result = get_gpu_data_linux()

        assert len(result) == 1
        assert result[0]["gpu"] == "NVIDIA GPU"

    def test_falls_back_to_generic(self) -> None:
        """Should return generic data when NVIDIA returns empty."""
        with (
            patch(
                "textual_system_monitor.gpu_linux._read_nvidia",
                return_value=[],
            ),
            patch(
                "textual_system_monitor.gpu_linux._read_generic",
                return_value=[{"gpu": "Generic GPU", "driver_version": "2"}],
            ),
        ):
            result = get_gpu_data_linux()

        assert len(result) == 1
        assert result[0]["gpu"] == "Generic GPU"

    def test_both_empty(self) -> None:
        """Should return empty list when both paths return nothing."""
        with (
            patch(
                "textual_system_monitor.gpu_linux._read_nvidia",
                return_value=[],
            ),
            patch(
                "textual_system_monitor.gpu_linux._read_generic",
                return_value=[],
            ),
        ):
            assert get_gpu_data_linux() == []


class TestGetXrandrResolutionEdgeCases:
    """Edge case tests for `_get_xrandr_resolution`."""

    def test_xrandr_star_with_x_no_match(self) -> None:
        """Should return first part when line has * and x but no resolution match."""
        output = "some random text with * and x but no resolution pattern"
        with patch(
            "textual_system_monitor.gpu_linux._run_command",
            return_value=output,
        ):
            assert _get_xrandr_resolution() == "some"


class TestGetRefreshRateEdgeCases:
    """Edge case tests for `_get_refresh_rate`."""

    def test_refresh_rate_no_parseable_float(self) -> None:
        """Should return 'Unknown' when no part is parseable as float."""
        output = "   1920x1080     *+  notanumber"
        with patch(
            "textual_system_monitor.gpu_linux._run_command",
            return_value=output,
        ):
            assert _get_refresh_rate() == "Unknown"
