from textual_system_monitor.utilities import compute_percentage_color


async def test_percent_green():
    _, color = compute_percentage_color(1)
    assert color == "green"


async def test_percent_yellow():
    _, color = compute_percentage_color(80)
    assert color == "yellow"


async def test_percent_red():
    _, color = compute_percentage_color(95)
    assert color == "red"


async def test_too_low():
    _, color = compute_percentage_color(-100)
    assert color == "green"


async def test_too_high():
    _, color = compute_percentage_color(200)
    assert color == "red"
