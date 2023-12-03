"""axe accessibility testing on exported nbconvert scripts.

* test the accessibility of exported notebooks
* test the accessibility of nbconvert-a11y dialogs
"""

from json import dumps
from logging import getLogger
from pathlib import Path

from pytest import mark, param

from tests.test_smoke import CONFIGURATIONS, NOTEBOOKS, SKIPCI, get_target_html

TPL_NOT_ACCESSIBLE = mark.xfail(reason="template is not accessible")
HERE = Path(__file__).parent
EXPORTS = HERE / "exports"
HTML = EXPORTS / "html"
LOGGER = getLogger(__name__)
AUDIT = EXPORTS / "audit"
TREE = AUDIT / "tree"

# ignore mathjax at the moment. we might be able to turne mathjax to have better
# accessibility. https://github.com/Iota-School/notebooks-for-all/issues/81
MATHJAX = "[id^=MathJax]"


config_notebooks_aa = mark.parametrize(
    "config,notebook",
    [
        param(
            (CONFIGURATIONS / (a := "default")).with_suffix(".py"),
            (NOTEBOOKS / (b := "lorenz-executed")).with_suffix(".ipynb"),
            marks=[SKIPCI, TPL_NOT_ACCESSIBLE],
            id="-".join((b, a)),
        )
    ],
)

config_notebooks_aaa = mark.parametrize(
    "config,notebook",
    [
        param(
            (CONFIGURATIONS / (a := "a11y")).with_suffix(".py"),
            (NOTEBOOKS / (b := "lorenz-executed")).with_suffix(".ipynb"),
            id="-".join(
                (b, a),
            ),
        ),
        param(
            (CONFIGURATIONS / (a := "section")).with_suffix(".py"),
            (NOTEBOOKS / (b := "lorenz-executed")).with_suffix(".ipynb"),
            id="-".join(
                (b, a),
            ),
        ),
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


@config_notebooks_aa
def test_axe_aa(axe, config, notebook):
    target = get_target_html(config, notebook)
    audit = AUDIT / target.with_suffix(".json").name

    axe(Path.as_uri(target)).dump(audit).raises()


@config_notebooks_aaa
def test_axe_aaa(axe, page, config, notebook):
    target = get_target_html(config, notebook)
    audit = AUDIT / target.with_suffix(".json").name
    tree = TREE / audit.name
    test = axe(Path.as_uri(target), axe_config=axe_config_aaa).dump(audit)
    tree.parent.mkdir(parents=True, exist_ok=True)
    tree.write_text(dumps(page.accessibility.snapshot()))
    test.raises()
