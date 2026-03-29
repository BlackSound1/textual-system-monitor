from src.app import Monitor


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
