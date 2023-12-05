"""axe accessibility testing on exported nbconvert scripts.

* test the accessibility of exported notebooks
* test the accessibility of nbconvert-a11y dialogs
"""

from json import dumps
from pathlib import Path

from pytest import mark, param
from nbconvert_a11y.pytest_axe import JUPYTER_WIDGETS, MATHJAX

from tests.test_smoke import CONFIGURATIONS, NOTEBOOKS, SKIPCI, get_target_html

TPL_NOT_ACCESSIBLE = mark.xfail(reason="template is not accessible")
HERE = Path(__file__).parent
EXPORTS = HERE / "exports"
HTML = EXPORTS / "html"
AUDIT = EXPORTS / "audit"
TREE = AUDIT / "tree"

# ignore mathjax at the moment. we might be able to turne mathjax to have better
# accessibility. https://github.com/Iota-School/notebooks-for-all/issues/81


@mark.parametrize(
    "config,notebook",
    [
        param(
            CONFIGURATIONS / "a11y.py",
            NOTEBOOKS / "lorenz-executed.ipynb",
            id="lorenz-executed-a11y",
        ),
        param(
            CONFIGURATIONS / "section.py",
            NOTEBOOKS / "lorenz-executed.ipynb",
            id="lorenz-executed-section",
        ),
    ],
)
def test_axe(axe, config, notebook):
    """verify the baseline templates satisify all rules update AAA.

    any modifications to the template can only degrade accessibility.
    this baseline is critical for adding more features. all testing piles
    up without automation. these surface protections allow more manual testing
    or verified conformations of html.
    """
    target = get_target_html(config, notebook)
    audit = AUDIT / target.with_suffix(".json").name

    test = axe(Path.as_uri(target))
    test.run({"exclude": [JUPYTER_WIDGETS, MATHJAX]})
    # this is not a good place to export an audit except to
    # verify what tests apply and what tests don't
    # this could be a good time to export the accessibility tree.
    test.raises()
