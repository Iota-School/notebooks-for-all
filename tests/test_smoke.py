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

TEMPLATES = Path(nbconvert_a11y.__file__).parent / "templates/a11y"
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


assets = mark.parametrize("assets", [TEMPLATES / "settings.js", TEMPLATES / "style.css"])


@configs
def test_config_loading(config):
    """Verify configs are loaded."""
    exporter_from_config(config)  # will ExporterNameError if there is a failure.


@assets
def test_static_assets(assets):
    """This is a bad test. it won't fail, but needs to run to collect testing assets."""
    target = HTML / assets.name
    try:
        assert target.exists(), f"{assets.name} doesn't exist."
    except AssertionError:
        target.parent.mkdir(exist_ok=True, parents=True)
        copyfile(assets, target)
        assert target.exists(), f"{assets.name} couldn't be created"


@configs
@notebooks
def test_export_notebooks(config, notebook):
    """Verify that all the internals work sufficiently to export notebooks."""
    html, resources = exporter_from_config(config).from_filename(notebook)
    TARGET = get_target_html(config, notebook)
    TARGET.write_text(html)
    LOGGER.debug(f"writing html to {TARGET}")
