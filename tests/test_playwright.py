import contextlib
import dataclasses
from json import dumps, loads
from logging import getLogger
from pathlib import Path

import exceptiongroup
from test_nbconvert_html5 import exporter


from pytest import fixture, mark, param

from tests.test_smoke import CONFIGURATIONS, NOTEBOOKS, SKIPCI, get_target_html

TPL_NOT_ACCESSIBLE = mark.xfail(reason="template is not accessible")
HERE = Path(__file__).parent
EXPORTS = HERE / "exports"
HTML = EXPORTS / "html"
LOGGER = getLogger(__name__)
AUDIT = EXPORTS / "audit"

# ignore mathjax at the moment. we might be able to turne mathjax to have better
# accessibility. https://github.com/Iota-School/notebooks-for-all/issues/81
MATHJAX = "[id^=MathJax]"

aa_config_notebooks = mark.parametrize(
    "config,notebook",
    [
        param(
            (CONFIGURATIONS / (a := "a11y")).with_suffix(".py"),
            (NOTEBOOKS / (b := "lorenz-executed")).with_suffix(".ipynb"),
            id="-".join((b, a)),
        ),
        param(
            (CONFIGURATIONS / (a := "default")).with_suffix(".py"),
            (NOTEBOOKS / (b := "lorenz-executed")).with_suffix(".ipynb"),
            marks=[SKIPCI, TPL_NOT_ACCESSIBLE],
            id="-".join((b, a)),
        ),
    ],
)

aaa_config_notebooks = mark.parametrize(
    "config,notebook",
    [
        param(
            (CONFIGURATIONS / (a := "a11y")).with_suffix(".py"),
            (NOTEBOOKS / (b := "lorenz-executed")).with_suffix(".ipynb"),
            id="-".join(
                (b, a),
            ),
            marks=[TPL_NOT_ACCESSIBLE],
        )
    ],
)


@dataclasses.dataclass
class AxeException(Exception):
    message: str
    target: list
    data: dict = dataclasses.field(repr=False)

    types = {}

    @classmethod
    def new(cls, id, impact, message, data, target, **kwargs):
        if id in cls.types:
            cls = cls.types.get(id)
        else:
            cls = cls.types.setdefault(
                id,
                type(
                    f"{impact.capitalize()}{''.join(map(str.capitalize, id.split('-')))}Exception",
                    (cls,),
                    dict(),
                ),
            )
        return cls(message, target, data)

    @classmethod
    def from_violations(cls, data):
        out = []
        for violation in (violations := data.get("violations")):
            for node in violation["nodes"]:
                for exc in node["any"]:
                    out.append(cls.new(**exc, target=["target"]))
        return exceptiongroup.ExceptionGroup(f"{len(violations)} accessibility violations", out)


def get_axe():
    from requests_cache import install_cache
    import requests

    install_cache("a11y-audit")
    return requests.get("https://cdn.jsdelivr.net/npm/axe-core").text


axe_config_aa = {
    "runOnly": ["act", "best-practice", "experimental", "wcag21a", "wcag21aa", "wcag22aa"],
    "allowedOrigins": ["<same_origin>"],
}

axe_config_aaa = {
    "runOnly": [
        "act",
        "best-practice",
        "experimental",
        "wcag21a",
        "wcag21aa",
        "wcag22aa",
        "wcag2aaa",
    ],
    "allowedOrigins": ["<same_origin>"],
}

tests_axe = {"exclude": [MATHJAX]}


@fixture
def axe(page):
    def go(url, tests=tests_axe, axe_config=axe_config_aa):
        page.goto(url)
        page.evaluate(get_axe())
        return page.evaluate(
            f"window.axe.run({tests and dumps(tests) or 'document'}, {dumps(axe_config)})"
        )

    yield go


@aa_config_notebooks
def test_axe_aa(axe, config, notebook):
    target = get_target_html(config, notebook)
    results = axe(Path.as_uri(target))
    AUDIT.mkdir(parents=True, exist_ok=True)
    audit = AUDIT / target.with_suffix(".json").name
    LOGGER.info(f"""writing {audit} with {len(results["violations"])} violations""")
    audit.write_text(dumps(results))

    if results["violations"]:
        raise AxeException.from_violations(results)


@aaa_config_notebooks
def test_axe_aaa(axe, config, notebook):
    target = get_target_html(config, notebook)
    results = axe(Path.as_uri(target), axe_config=axe_config_aaa)
    AUDIT.mkdir(parents=True, exist_ok=True)
    audit = AUDIT / target.with_suffix(".json").name
    LOGGER.info(f"""writing {audit} with {len(results["violations"])} violations""")
    audit.write_text(dumps(results))
    print(results)
    if results["violations"]:
        raise AxeException.from_violations(results)
