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


@aa_config_notebooks
def test_axe_aa(axe, config, notebook):
    target = get_target_html(config, notebook)
    audit = AUDIT / target.with_suffix(".json").name
    axe(Path.as_uri(target)).dump(audit).raises()


@aaa_config_notebooks
def test_axe_aaa(axe, config, notebook):
    target = get_target_html(config, notebook)
    audit = AUDIT / target.with_suffix(".json").name
    axe(Path.as_uri(target), axe_config=axe_config_aaa).dump(audit).raises()
