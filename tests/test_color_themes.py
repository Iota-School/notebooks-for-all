from pytest import fixture

from nbconvert import get_exporter
from nbconvert_a11y.exporter import THEMES
from nbconvert_a11y.pytest_axe import Axe

LORENZ = "lorenz-executed.ipynb"


@fixture(params=list(THEMES))
def lorenz(page, request, notebook):
    return Axe(
        page=page,
        url=notebook(
            "a11y", LORENZ, color_theme=request.param, include_settings=True, wcag_priority="AA"
        ),
    ).configure()


def test_dark_themes(lorenz):
    lorenz.page.click("""[aria-controls="nb-settings"]""")
    lorenz.page.locator("select[name=color-scheme]").select_option("dark mode")
    lorenz.page.keyboard.press("Escape")
    # force the background to be black because axe detects a white background in dark mode.
    lorenz.page.eval_on_selector("body", """x => x.style.backgroundColor = `#000000`""")
    lorenz.run(dict(include=[".nb-source"])).raises()
    # accessible pygments disclsoes that we should expect some color contrast failures on some themes.
    # there isnt much code which might not generate enough conditions to create color contrast issues.


def test_light_themes(lorenz):
    lorenz.run(dict(include=[".nb-source"])).raises()
