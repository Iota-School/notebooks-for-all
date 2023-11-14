import dataclasses
from json import dumps, loads
from logging import getLogger
from pathlib import Path

import exceptiongroup
from test_nbconvert_html5 import exporter


from pytest import fixture, mark

HERE = Path(__file__).parent
NOTEBOOKS = HERE / "notebooks"
EXPORTS = HERE / "exports"
HTML = EXPORTS / "html"
LOGGER = getLogger(__name__)
AUDIT = EXPORTS / "audit"

# ignore mathjax at the moment. we might be able to turne mathjax to have better
# accessibility. https://github.com/Iota-School/notebooks-for-all/issues/81
MATHJAX = "[id^=MathJax]"


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


@fixture
def axe():
    from requests_cache import install_cache
    import requests

    install_cache("a11y-audit")
    yield requests.get("https://cdn.jsdelivr.net/npm/axe-core").text


@mark.parametrize(
    "notebook",
    list(
        x
        for x in NOTEBOOKS.glob("*.ipynb")
        if x.name not in {"Imaging_Sky_Background_Estimation.ipynb"}
    ),
)
def test_baseline_a11y_template(page, exporter, notebook, axe):
    config = {}
    config.setdefault(
        "runOnly",
        ["act", "best-practice", "experimental", "wcag21a", "wcag21aa", "wcag22aa"],
    )
    config.setdefault("allowedOrigins", ["<same_origin>"])
    target = HTML / notebook.with_suffix(".html").name
    target.parent.mkdir(exist_ok=True, parents=True)
    LOGGER.debug(f"""injecting axe into {target.name}""")
    target.write_text(exporter.from_filename(notebook)[0])

    test = dict(exclude=[MATHJAX])
    page.goto(Path.as_uri(target))
    LOGGER.debug(f"""injecting axe into {target.name}""")
    page.evaluate(axe)
    LOGGER.debug(f"""auditting {target.name} with axe""")
    result = page.evaluate(f"window.axe.run({dumps(test)}, {dumps(config)})")
    AUDIT.mkdir(parents=True, exist_ok=True)
    audit = AUDIT / notebook.with_suffix(".json").name
    LOGGER.info(f"""writing {audit} with {len(result["violations"])} violations""")
    audit.write_text(dumps(result))

    if result["violations"]:
        raise AxeException.from_violations(result)
