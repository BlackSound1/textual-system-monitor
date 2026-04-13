from textual_system_monitor.utilities import bytes_to_human


async def test_documentation_examples() -> None:
    assert bytes_to_human(10_000) == "9.8 KiB"
    assert bytes_to_human(100_001_221) == "95.4 MiB"


async def test_bytes_only() -> None:
    assert bytes_to_human(100) == "100.0 B"


async def test_neg_bytes() -> None:
    assert bytes_to_human(-1) == "0.0 B"


async def test_KB() -> None:
    assert bytes_to_human(1_024) == "1.0 KiB"
    assert bytes_to_human(1_000, base=1000) == "1.0 KB"


async def test_MB() -> None:
    assert bytes_to_human(1_048_576) == "1.0 MiB"
    assert bytes_to_human(1_000_000, base=1000) == "1.0 MB"


async def test_GB() -> None:
    assert bytes_to_human(1_073_741_824) == "1.0 GiB"
    assert bytes_to_human(1_000_000_000, base=1000) == "1.0 GB"


async def test_TB() -> None:
    assert bytes_to_human(1_099_511_627_776) == "1.0 TiB"
    assert bytes_to_human(1_000_000_000_000, base=1000) == "1.0 TB"


async def test_PB() -> None:
    assert bytes_to_human(1_125_899_906_842_624) == "1.0 PiB"
    assert bytes_to_human(1_000_000_000_000_000, base=1000) == "1.0 PB"


async def test_EB() -> None:
    assert bytes_to_human(1_152_921_504_606_846_976) == "1.0 EiB"
    assert bytes_to_human(1_000_000_000_000_000_000, base=1000) == "1.0 EB"


async def test_ZB() -> None:
    assert bytes_to_human(1_180_591_620_717_411_303_424) == "1.0 ZiB"
    assert bytes_to_human(1_000_000_000_000_000_000_000, base=1000) == "1.0 ZB"


async def test_YB() -> None:
    assert bytes_to_human(1_208_925_819_614_629_174_706_176) == "1.0 YiB"
    assert bytes_to_human(1_000_000_000_000_000_000_000_000, base=1000) == "1.0 YB"
