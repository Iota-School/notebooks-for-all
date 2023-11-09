from shlex import split
from subprocess import check_output, run
from sys import executable
from nbconvert import get_exporter, get_export_names
from pytest import fixture, mark
import nbconvert_html5, nbconvert, pathlib, bs4, traitlets
from nbconvert_html5.form_exporter import get_soup
from functools import partial
from pathlib import Path

EXPORTER = "a11y"
HERE = Path(__file__).parent
CONFIG = HERE / "jupyter_nbconvert_config.py"
NOTEBOOKS = HERE / "notebooks"
notebooks = mark.parametrize("notebook", [next(NOTEBOOKS.glob("lorenz-executed.ipynb"))])


@fixture
def exporter():
    a11y = get_exporter(EXPORTER)()
    a11y.update_config(traitlets.config.PyFileConfigLoader(str(CONFIG.absolute())).load_config())
    yield a11y


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

