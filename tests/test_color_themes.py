from nbconvert import get_exporter
from pytest import fixture

from nbconvert_a11y.exporter import THEMES
from nbconvert_a11y.pytest_axe import Axe
from tests.test_smoke import NOTEBOOKS

LORENZ = NOTEBOOKS / "lorenz-executed.ipynb"


@fixture(params=list(THEMES))
def exporter(request):
    e = get_exporter("a11y")()
    e.color_theme = request.param
    e.include_settings = True
    e.wcag_priority = "AA"
    return e


@fixture()
def lorenz(page, tmp_path, exporter):
    tmp = tmp_path / f"{exporter.color_theme}.html"
    tmp.write_text(exporter.from_filename(LORENZ)[0])
    return Axe(page=page, url=tmp.absolute().as_uri()).configure()


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
