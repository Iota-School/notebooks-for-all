"""these tests verify how third party tools effect the accessibility of rendered notebook components.

these tests allow us to track ongoing community progress and record inaccessibilities
upstream of our control.
"""

from os import environ
from unittest import TestCase

import pytest
from flask import url_for
from pytest import fixture, skip

from nbconvert_a11y.pytest_axe import (
    JUPYTER_WIDGETS,
    NO_ALT,
    PYGMENTS,
    SA11Y,
    Violation,
)

# only run these tests when the CI environment variables are defined.
environ.get("CI") or skip(allow_module_level=True)


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
        finally:
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
        finally:
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
        finally:
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
        finally:
            pytest.xfail("an issue report needs to be filed with sa11y.")

    @fixture(autouse=True)
    def url(self, axe, notebook):
        self.axe = axe(notebook("a11y", "lorenz-executed.ipynb", include_sa11y=True)).configure()


class FlaskDev(TestCase):
    """there are accessibility violations in the flask debug templates.

    flask is taught commonly enough that having accessible debugging sessions
    is critical for assistive technology users learning app development.
    """

    def xfail_flask_dev(self):
        print(self.axe.url)
        exception = self.axe.run().results.exception()
        try:
            raise exception
        except* Violation["serious-color-contrast-enhanced"]:
            pass
        except* Violation["serious-color-contrast"]:
            pass
        except* Violation["minor-empty-heading"]:
            pass
        except* Violation["moderate-landmark-one-main"]:
            pass
        except* Violation["moderate-region"]:
            pass
        finally:
            pytest.xfail("there are 2 serious, 2 moderate, and 1 minor accessibility violations")

    @fixture(autouse=True)
    def url(self, axe, live_server):
        # the query string causes the web server to raise an error so we can test flask dev tools
        self.axe = axe(url_for("bad", foo="bar", _external=True)).configure()
