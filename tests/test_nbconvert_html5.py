from pathlib import Path
from shlex import split
from subprocess import check_output
from sys import executable

import traitlets
from nbconvert import get_export_names, get_exporter
from pytest import fixture, mark

from nbconvert_a11y.form_exporter import get_soup

EXPORTER = "a11y"
HERE = Path(__file__).parent
CONFIG = HERE / "jupyter_nbconvert_config.py"
NOTEBOOKS = HERE / "notebooks"
notebooks = mark.parametrize("notebook", [next(NOTEBOOKS.glob("lorenz-executed.ipynb"))])


@fixture()
def exporter():
    a11y = get_exporter(EXPORTER)()
    a11y.update_config(traitlets.config.PyFileConfigLoader(str(CONFIG.absolute())).load_config())
    return a11y


def test_entry_point_registration():
    assert EXPORTER in get_export_names(), "the entry point is not defined."


@notebooks
def test_a11y_exporter(exporter, notebook):
    html = get_soup(exporter.from_filename(notebook)[0])
    assert html.select_one("main"), "there is not main region"


@notebooks
def test_nbconvert_cli(notebook):
    target = notebook.with_suffix(".html")
    cmd = f"{executable} -m jupyter nbconvert --to {EXPORTER} --config {CONFIG} {notebook}"
    output = check_output(split(cmd)).decode()
    assert target.exists(), output
    target.unlink(True)
