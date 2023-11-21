import ast
import builtins
import json
import operator
from functools import lru_cache
from pathlib import Path

import pandas as pd
import tomli
from jinja2 import Environment, FileSystemLoader

DIR = Path(__file__).parent.parent.parent
PYPROJECT = DIR / "pyproject.toml"
DOCS = DIR / "tests"
EXPORTS = DOCS / "exports"
CONFIGS = EXPORTS / "configs"
REPORTS = EXPORTS / "reports"
AUDITS = EXPORTS / "audit"
NBS = EXPORTS / "notebooks"
HTML = EXPORTS / "html"
config = tomli.loads(PYPROJECT.read_text())

DOIT = config["tool"]["doit"]

notebooks = [Path(x).name for x in DOIT["tasks"]["copy"]["notebooks"]]
configs = [Path(x).name for x in DOIT["tasks"]["copy"]["configurations"]]
print(configs, notebooks)


@lru_cache
def get_environment():
    env = Environment(loader=FileSystemLoader(DOCS / "templates"))
    env.globals.update(vars(builtins), getdoc=getdoc)
    return env


@lru_cache
def get_data():
    df = pd.DataFrame(
        index=pd.MultiIndex.from_product(
            (
                sorted(NBS.glob("*.ipynb"), key=lambda x: notebooks.index(x.name)),
                sorted(CONFIGS.glob("*.py"), key=lambda x: configs.index(x.name)),
            ),
            names=["nb", "config"],
        )
    )

    df = df.assign(
        html=df.index.map(
            lambda x: (HTML / "-".join(map(operator.attrgetter("stem"), x))).with_suffix(".html")
        )
    )
    print(df.html)
    assert df.html.apply(Path.exists).all(), "the translation of the config/nb pairs failed"

    return df.assign(
        audit=df.html.apply(lambda x: (x.parent.parent / "audits" / x.name).with_suffix(".json"))
    )

    # assert df.audit.apply(Path.exists).all(), "the audit reports have not been generated"


def write_experiments():
    REPORTS.mkdir(exist_ok=True)
    body = get_environment().get_template("experiments.md.j2")
    (REPORTS / "experiment.md").write_text(body.render(df=get_data()))


def write_notebooks():
    REPORTS.mkdir(exist_ok=True)
    body = get_environment().get_template("notebooks.md.j2")
    (REPORTS / "notebooks.md").write_text(body.render(df=get_data(), SITE=DOCS))


def write_configs():
    REPORTS.mkdir(exist_ok=True)
    body = get_environment().get_template("configs.md.j2")
    (REPORTS / "configs.md").write_text(body.render(df=get_data()))


def getdoc_nb(path):
    source = ""
    for i, cell in enumerate(json.loads(path.read_text())["cells"]):
        if i > 1 or cell["cell_type"] == "code":
            break
        source += "".join(cell["source"]) + "\n" * 2
    return source


def getdoc_py(path):
    return ast.literal_eval(ast.parse(path.read_text()).body[0].value)


def getdoc(path):
    f = {".py": getdoc_py, ".ipynb": getdoc_nb}.get(path.suffix)
    return f and f(path)
