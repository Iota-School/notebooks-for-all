"""these tests verify how third party tools effect the accessibility of rendered notebook components.

these tests allow us to track ongoing community progress and record inaccessibilities
upstream of our control.
"""

from functools import partial
from os import environ
from unittest import TestCase

import pytest
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
    def xfail_all(self):
        exceptions = self.axe.run().results.exception()
        try:
            raise exceptions
        except* Violation["critical-image-alt"]:
            ...
        except* Violation["serious-color-contrast-enhanced"]:
            ...
        except* Violation["serious-aria-input-field-name"]:
            ...
        except* Violation["serious-color-contrast"]:
            ...
        except* Violation["minor-focus-order-semantics"]:
            ...
        pytest.xfail("there are 1 critical, 3 serious, and 1 minor accessibility violations")

    def xfail_pygments_highlight_default(self):
        """The default template has two serious color contrast violations.

        an issue needs to be opened or referenced.
        """
        # further verification would testing the nbviewer layer.
        exceptions = self.axe.run({"include": [PYGMENTS]}).results.exception()
        try:
            raise exceptions
        except* Violation["serious-color-contrast-enhanced"]:
            ...
        except* Violation["serious-color-contrast"]:
            ...
        pytest.xfail("there are 2 serious color contrast violations.")

    def xfail_widget_display(self):
        """The simple lorenz widget generates one minor and one serious accessibility violation."""
        exceptions = self.axe.run(
            {"include": [JUPYTER_WIDGETS], "exclude": [NO_ALT]}
        ).results.exception()
        try:
            raise exceptions
        except* Violation["minor-focus-order-semantics"]:
            ...
        except* Violation["serious-aria-input-field-name"]:
            ...
        pytest.xfail("widgets have not recieved a concerted effort.")

    @fixture(autouse=True)
    def url(self, axe, notebook):
        self.axe = axe(notebook("html", "lorenz-executed.ipynb")).configure()

class A11yTemplate(TestCase):
    def xfail_sa11y(self):
        """The simple lorenz widget generates one minor and one serious accessibility violation."""
        exceptions = self.axe.run({"include": [SA11Y]}).results.exception()
        try:
            raise exceptions
        except* Violation["serious-label-content-name-mismatch"]:
            ...
        pytest.xfail("an issue report needs to be filed with sa11y.")

    @fixture(autouse=True)
    def url(self, axe, notebook):
        self.axe = axe(notebook("a11y", "lorenz-executed.ipynb", **{
            "include_sa11y": True
        })).configure()
        print(self.axe.url)
