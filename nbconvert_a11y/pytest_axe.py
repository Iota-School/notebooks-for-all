# requires node and axe
# requires playwright
import dataclasses
from functools import lru_cache
from json import dumps, loads
from pathlib import Path
from shlex import quote, split
from subprocess import CalledProcessError, check_output
from typing import Any

import exceptiongroup
from attr import dataclass
from pytest import fixture, mark, param

nbconvert_a11y_DYNAMIC_TEST = "nbconvert_a11y_DYNAMIC_TEST"

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

MATHJAX = "[id^=MathJax]"
tests_axe = {"exclude": [MATHJAX]}


def get_npm_directory(package, data=False):
    try:
        info = loads(check_output(split(f"npm ls --long --depth 0 --json {quote(package)}")))
    except CalledProcessError:
        return None
    if data:
        return info
    return Path(info.get("dependencies").get(package).get("path"))


@dataclass
class AxeResults:
    data: Any

    def raises(self):
        if self.data["violations"]:
            raise AxeException.from_violations(self.data)
        return self

    def dump(self, file: Path):
        if file.is_dir():
            file /= "axe-results.json"
        file.parent.mkdir(exist_ok=True, parents=True)
        file.write_text(dumps(self.data))
        return self


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
                    {},
                ),
            )
        return cls(message, target, data)

    @classmethod
    def from_violations(cls, data):
        out = []
        for violation in (violations := data.get("violations")):
            for node in violation["nodes"]:
                for exc in node["any"]:
                    out.append(cls.new(**exc, target=node["target"]))
        return exceptiongroup.ExceptionGroup(f"{len(violations)} accessibility violations", out)


@mark.parametrize("package", ["axe-core", param("axe-core-doesnt-ship-this", marks=mark.xfail)])
def test_non_package(package):
    assert get_npm_directory(package), "package not found."


@lru_cache(1)
def get_axe():
    return (get_npm_directory("axe-core") / "axe.js").read_text()


def inject_axe(page):
    page.evaluate(get_axe())


def run_axe_test(page, tests_config=None, axe_config=None):
    return AxeResults(
        page.evaluate(
            f"window.axe.run({tests_config and dumps(tests_config) or 'document'}, {dumps(axe_config or {})})"
        )
    )


@fixture()
def axe(page):
    def go(url, tests=tests_axe, axe_config=axe_config_aa):
        page.goto(url)
        inject_axe(page)
        return run_axe_test(page, tests, axe_config)

    return go
