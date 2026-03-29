import pytest

from src.utilities import compute_percentage_color

@pytest.mark.asyncio
async def test_percent_green():
    _, color = compute_percentage_color(1)
    assert color == "green"

@pytest.mark.asyncio
async def test_percent_yellow():
    _, color = compute_percentage_color(80)
    assert color == "yellow"

@pytest.mark.asyncio
async def test_percent_red():
    _, color = compute_percentage_color(95)
    assert color == "red"

@pytest.mark.asyncio
async def test_too_low():
    _, color = compute_percentage_color(-100)
    assert color == "green"

@pytest.mark.asyncio
async def test_too_high():
    _, color = compute_percentage_color(200)
    assert color == "red"
