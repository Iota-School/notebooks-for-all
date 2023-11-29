"""specific ui and accessibility tests for the custom a11y template."""


from pytest import fixture, mark, param

from nbconvert_a11y.pytest_axe import inject_axe, run_axe_test
from tests.test_smoke import CONFIGURATIONS, NOTEBOOKS, get_target_html

NEEDS_WORK = "state needs work"


@fixture(
    params=[
        param(
            get_target_html(CONFIGURATIONS / "a11y.py", NOTEBOOKS / "lorenz-executed.ipynb"),
            id="executed-a11y",
        )
    ],
)
def test_page(request, page):
    # https://github.com/microsoft/playwright-pytest/issues/73
    page.goto(request.param.absolute().as_uri())
    inject_axe(page)
    yield page
    page.close()


@mark.parametrize(
    "dialog",
    [
        "[aria-controls=nb-settings]",
        "[aria-controls=nb-help]",
        "[aria-controls=nb-metadata]",
        "[aria-controls=nb-audit]",
        param("[aria-controls=nb-expanded-dialog]", marks=mark.xfail(reason=NEEDS_WORK)),
        param("[aria-controls=nb-visibility-dialog]", marks=mark.xfail(reason=NEEDS_WORK)),
        # param("nada", marks=mark.xfail(reason="no selector")),
        # failing selectors timeout and slow down tests.
    ],
)
def test_dialogs(test_page, dialog):
    """Test the controls in dialogs."""
    # dialogs are not tested in the baseline axe test. they need to be active to test.
    # these tests activate the dialogs to assess their accessibility with the active dialogs.
    test_page.click(dialog)
    run_axe_test(test_page).raises()


SNIPPET_FONT_SIZE = (
    """window.getComputedStyle(document.querySelector("body")).getPropertyValue("font-size")"""
)


def test_settings_font_size(test_page):
    """Test that the settings make their expected changes."""
    assert test_page.evaluate(SNIPPET_FONT_SIZE) == "16px", "the default font size is unexpected"
    test_page.click("[aria-controls=nb-settings]")
    test_page.locator("[name=font-size]").select_option("xx-large")
    assert test_page.evaluate(SNIPPET_FONT_SIZE) == "32px", "font size not changed"
