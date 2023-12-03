"""smoke tests that verify the python module execution.
these tests do not invoke any browsers.

the tests verify:
* the nbconvert exporters are properly exported.
* config files are applied to exports
"""

from functools import lru_cache
from logging import getLogger
from os import environ
from pathlib import Path
from shutil import copyfile

import nbconvert.nbconvertapp
from pytest import mark, param

import nbconvert_a11y
import jupyter_core.paths

from nbconvert_a11y.a11y_exporter import get_soup

SKIP_BASELINE = "baseline tests skipped locally"
LOGGER = getLogger(__name__)
HERE = Path(__file__).parent
CONFIGURATIONS = HERE / "configurations"
NOTEBOOKS = HERE / "notebooks"
EXPORTS = HERE / "exports"
HTML = EXPORTS / "html"
CI = environ.get("CI")
SKIPCI = mark.skipif(not CI, reason=SKIP_BASELINE)


@lru_cache
def exporter_from_config(config: Path) -> nbconvert.Exporter:
    """Create a nbconvert exporter from an IPython configuration file."""
    app = nbconvert.nbconvertapp.NbConvertApp(config_file=str(config))
    app.load_config_file()
    return nbconvert.get_exporter(app.export_format)(config=app.config)


def get_target_html(config, notebook):
    target = (HTML / "-".join([notebook.stem, config.stem])).with_suffix(".html")
    target.parent.mkdir(exist_ok=True, parents=True)
    return target


configs = mark.parametrize(
    "config",
    [
        param((CONFIGURATIONS / (id := "a11y")).with_suffix(".py"), id=id),
        param((CONFIGURATIONS / (id := "section")).with_suffix(".py"), id=id),
        param((CONFIGURATIONS / (id := "list")).with_suffix(".py"), id=id),
        param(
            (CONFIGURATIONS / (id := "default")).with_suffix(".py"),
            id=id,
            marks=SKIPCI,
        ),
    ],
)

notebooks = mark.parametrize(
    "notebook",
    [
        param((NOTEBOOKS / (id := "lorenz")).with_suffix(".ipynb"), id=id),
        param((NOTEBOOKS / (id := "lorenz-executed")).with_suffix(".ipynb"), id=id),
    ],
)


assets = mark.parametrize("asset", ["settings.js", "style.css"])


@configs
def test_config_loading(config):
    """Verify configs are loaded."""
    exporter_from_config(config)  # will ExporterNameError if there is a failure.


@assets
def test_static_assets(asset):
    """This is a bad test. it won't fail, but needs to run to collect testing assets."""
    target = HTML / asset
    target.parent.mkdir(exist_ok=True, parents=True)
    for path in map(
        Path, jupyter_core.paths.jupyter_path("nbconvert", "templates", "a11y", "static", asset)
    ):
        if path.exists():
            copyfile(path, target)
            break
    assert target.exists(), f"{asset} couldn't be created"


@configs
@notebooks
def test_export_notebooks(config, notebook):
    """Verify that all the internals work sufficiently to export notebooks."""
    html, resources = exporter_from_config(config).from_filename(notebook)
    TARGET = get_target_html(config, notebook)
    TARGET.write_text(html)
    LOGGER.debug(f"writing html to {TARGET}")

@mark.parametrize("target", [get_target_html(CONFIGURATIONS / "a11y.py", NOTEBOOKS / "lorenz-executed.ipynb")])
def test_a11y_template_content(target):
    soup = get_soup(target.read_text())

    assert soup.select_one("#toc"), "toc does not exist"
