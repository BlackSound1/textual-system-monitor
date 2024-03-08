INTERVAL = 1 / 5


def compute_percentage_color(pct: float) -> str:
    """
    Takes a given percentage and returns that percentage, colored according to
    whether usage is high, medium, or low.

    :param pct: The uncolored percentage value
    :return: The colored percentage value as a string
    """

    if pct <= 75:
        pct = f"[green]{pct:.1f}[/green]"
    elif 75 < pct < 90:
        pct = f"[yellow]{pct:.1f}[/yellow]"
    else:
        pct = f"[red]{pct:.1f}[/red]"

    return pct
