"""axe accessibility testing on exported nbconvert scripts.

* test the accessibility of exported notebooks
* test the accessibility of nbconvert-a11y dialogs
"""


from pytest import mark

from nbconvert_a11y.pytest_axe import JUPYTER_WIDGETS, MATHJAX, SA11Y


@mark.parametrize(
    "config,exporter_name,name",
    [
        ("a11y.py", "a11y-table", "lorenz-executed.ipynb"),
        ("section.py", "a11y-landmark", "lorenz-executed.ipynb"),
        ("list.py", "a11y-list", "lorenz-executed.ipynb"),
    ],
)
def test_axe(axe, notebook, config, exporter_name, name):
    """Verify the baseline templates satisify all rules update AAA.

    any modifications to the template can only degrade accessibility.
    this baseline is critical for adding more features. all testing piles
    up without automation. these surface protections allow more manual testing
    or verified conformations of html.
    """
    test = axe(notebook(exporter_name, name, config=config))
    # ignore mathjax at the moment. we might be able to turne mathjax to have better
    # accessibility. https://github.com/Iota-School/notebooks-for-all/issues/81
    test.run({"exclude": [JUPYTER_WIDGETS, MATHJAX, SA11Y]})
    test.raises()
