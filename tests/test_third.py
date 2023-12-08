"""these tests verify how third party tools effect the accessibility of rendered notebook components.

these tests allow us to track ongoing community progress and record inaccessibilities
upstream of our control.
"""

from functools import partial
from os import environ
from pathlib import Path
from unittest import TestCase

from pytest import fixture, skip, mark
from nbconvert_a11y.pytest_axe import JUPYTER_WIDGETS, MATHJAX, NO_ALT, PYGMENTS, AllOf, Violation
from tests.test_smoke import CONFIGURATIONS, NOTEBOOKS, get_target_html

# only run these tests when the CI environment variables are defined.
environ.get("CI") or skip(allow_module_level=True)
xfail = partial(mark.xfail, raises=AllOf, strict=True)


class DefaultTemplate(TestCase):
    """automated accessibility testing of the default nbconvert light theme."""

    # test all of the accessibility violations
    # then incrementally explain them in smaller tests.
    @xfail(reason="there is a lot of complexity in ammending accessibility in many projects")
    def test_all(self):
        raise self.axe.run().raises_allof(
            Violation["critical-image-alt"],
            Violation["serious-color-contrast-enhanced"],
            Violation["serious-aria-input-field-name"],
            Violation["serious-color-contrast"],
            Violation["minor-focus-order-semantics"],
        )

    @xfail(reason="the default pygments theme has priority AA and AAA color contrast issues.")
    def test_highlight_pygments(self):
        """the default template has two serious color contrast violations.

        an issue needs to be opened or referenced.
        """
        # further verification would testing the nbviewer layer.
        raise self.axe.run({"include": [PYGMENTS]}).raises_allof(
            Violation["serious-color-contrast-enhanced"],
            Violation["serious-color-contrast"],
        )

    @xfail(reason="widgets have not recieved a concerted effort.")
    def test_widget_display(self):
        """the simple lorenz widget generates one minor and one serious accessibility violation."""
        raise self.axe.run({"include": [JUPYTER_WIDGETS], "exclude": [NO_ALT]}).raises_allof(
            Violation["minor-focus-order-semantics"],
            Violation["serious-aria-input-field-name"],
        )

    # todo test mermaid
    # test widgets kitchen sink
    # test pandas

    @fixture(autouse=True)
    def lorenz(
        self,
        axe,
        config=(CONFIGURATIONS / (a := "default")).with_suffix(".py"),
        notebook=(NOTEBOOKS / (b := "lorenz-executed")).with_suffix(".ipynb"),
    ):
        self.axe = axe(Path.as_uri(get_target_html(config, notebook))).configure()
