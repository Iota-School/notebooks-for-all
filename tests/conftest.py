import urllib
from ast import literal_eval
from os import environ
from pathlib import Path
from unittest import TestLoader

import pytest
from flask import Flask, request, url_for

import nbconvert.nbconvertapp
from nbconvert import get_exporter

collect_ignore = ["notebooks/lorenz.ipynb"]
HERE = Path(__file__).parent
CONFIGURATIONS = HERE / "configurations"
NOTEBOOKS = HERE / "notebooks"
EXPORTS = HERE / "exports"
HTML = EXPORTS / "html"
CI = environ.get("CI")

TestLoader.testMethodPrefix = "test", "xfail"


def pytest_configure(config):
    config.addinivalue_line("python_functions", ("test_", "xfail_"))


def format_qs_value(x):
    for x in map(bytes.decode, x):
        if x in {"True", False}:
            return literal_eval(x)
        if x.isnumeric():
            return float(x)
        return x


def make_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True

    @app.route("/")
    def list():
        return "\n".join(map(str, NOTEBOOKS.glob("*.ipynb")))

    @app.route("/<exporter>/<name>")
    def nb(exporter, name):
        params = {
            k.decode(): format_qs_value(v)
            for k, v in urllib.parse.parse_qs(request.query_string).items()
        }
        if "config" in params:
            app = nbconvert.nbconvertapp.NbConvertApp(
                config_file=str(CONFIGURATIONS / params["config"])
            )
            app.load_config_file()
            params = dict(config=app.config)

        e = get_exporter(exporter)(**params)
        return e.from_filename(NOTEBOOKS / name)[0]

    @app.route("/bad")
    def bad():
        if request.query_string:
            assert False, "this causes a flask failure when the query string is non empty"
        return ""

    return app


@pytest.fixture(scope="session")
def app():
    return make_app()


@pytest.fixture(scope="session")
def notebook(live_server):
    def url(exporter="a11y", name="lorenz-executed.ipynb", **qs):
        return url_for("nb", exporter=exporter, name=name, **qs, _external=True)

    return url


if __name__ == "__main__":
    make_app().run(debug=True, port=5000)
