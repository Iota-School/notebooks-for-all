"""these tests verify how third party tools effect the accessibility of rendered notebook components.

these tests allow us to track ongoing community progress and record inaccessibilities
upstream of our control.
"""

from functools import partial
from os import environ
from unittest import TestCase

from pytest import fixture, mark, skip

from nbconvert import get_exporter
from nbconvert_a11y.pytest_axe import (
    JUPYTER_WIDGETS,
    NO_ALT,
    PYGMENTS,
    SA11Y,
    AllOf,
    Violation,
)
from tests.test_color_themes import LORENZ

# only run these tests when the CI environment variables are defined.
environ.get("CI") or skip(allow_module_level=True)
xfail = partial(mark.xfail, raises=AllOf, strict=True)


@fixture()
def exporter(request):
    e = get_exporter("html")()
    return e


@fixture()
def a11y_exporter(request):
    e = get_exporter("a11y")()
    e.wcag_priority = "AA"
    e.include_sa11y = True
    return e


class DefaultTemplate(TestCase):
    """automated accessibility testing of the default nbconvert light theme."""

    # test all of the accessibility violations
    # then incrementally explain them in smaller tests.
    @xfail(
        reason="there is a lot of complexity in ammending accessibility in many projects",
        strict=True,
    )
    def test_all(self):
        raise self.axe.run().raises_allof(
            Violation["critical-image-alt"],
            Violation["serious-color-contrast-enhanced"],
            Violation["serious-aria-input-field-name"],
            Violation["serious-color-contrast"],
            Violation["minor-focus-order-semantics"],
        )

    @xfail(
        reason="the default pygments theme has priority AA and AAA color contrast issues.",
        strict=True,
    )
    def test_highlight_pygments(self):
        """The default template has two serious color contrast violations.

        an issue needs to be opened or referenced.
        """
        # further verification would testing the nbviewer layer.
        raise self.axe.run({"include": [PYGMENTS]}).raises_allof(
            Violation["serious-color-contrast-enhanced"],
            Violation["serious-color-contrast"],
        )

    @xfail(reason="widgets have not recieved a concerted effort.", raises=AllOf, strict=True)
    def test_widget_display(self):
        """The simple lorenz widget generates one minor and one serious accessibility violation."""
        raise self.axe.run({"include": [JUPYTER_WIDGETS], "exclude": [NO_ALT]}).raises_allof(
            Violation["minor-focus-order-semantics"],
            Violation["serious-aria-input-field-name"],
        )

    # todo test mermaid
    # test widgets kitchen sink
    # test pandas

    @fixture(autouse=True)
    def lorenz(self, axe, tmp_path, exporter):
        tmp = (tmp_path / LORENZ.name).with_suffix(".html")
        tmp.write_text(exporter.from_filename(LORENZ)[0])
        self.axe = axe(tmp.as_uri().strip()).configure()


class A11yTemplate(TestCase):
    @xfail(raises=AllOf, strict=True)
    def test_sa11y(self):
        """The simple lorenz widget generates one minor and one serious accessibility violation."""
        raise self.axe.run({"include": [SA11Y]}).raises_allof(
            Violation["serious-label-content-name-mismatch"]
        )

    @fixture(autouse=True)
    def lorenz(self, axe, tmp_path, a11y_exporter):
        tmp = (tmp_path / LORENZ.name).with_suffix(".html")
        tmp.write_text(a11y_exporter.from_filename(LORENZ)[0])
        self.axe = axe(tmp.as_uri().strip()).configure()
