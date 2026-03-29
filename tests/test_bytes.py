from src.utilities import bytes_to_human


async def test_documentation_examples() -> None:
    assert bytes_to_human(10_000) == '9.8 KiB'
    assert bytes_to_human(100_001_221) == '95.4 MiB'

async def test_bytes_only() -> None:
    assert bytes_to_human(100) == '100.0 B'

async def test_neg_bytes() -> None:
    assert bytes_to_human(-1) == "0.0 B"

async def test_KB() -> None:
    assert bytes_to_human(1_024) == "1.0 KiB"

async def test_MB() -> None:
    assert bytes_to_human(1_048_576) == "1.0 MiB"

async def test_GB() -> None:
    assert bytes_to_human(1_073_741_824) == "1.0 GiB"

async def test_TB() -> None:
    assert bytes_to_human(1_099_511_627_776) == "1.0 TiB"

async def test_PB() -> None:
    assert bytes_to_human(1_125_899_906_842_624) == "1.0 PiB"

async def test_EB() -> None:
    assert bytes_to_human(1_152_921_504_606_846_976) == "1.0 EiB"

async def test_ZB() -> None:
    assert bytes_to_human(1_180_591_620_717_411_303_424) == "1.0 ZiB"

async def test_YB() -> None:
    assert bytes_to_human(1_208_925_819_614_629_174_706_176) == "1.0 YiB"
