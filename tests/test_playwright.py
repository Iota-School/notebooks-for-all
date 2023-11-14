from json import dumps, loads
from logging import getLogger
from pathlib import Path
from test_nbconvert_html5 import exporter


from pytest import fixture, mark

HERE = Path(__file__).parent
NOTEBOOKS = HERE / "notebooks"
EXPORTS = HERE / "exports"
HTML =  EXPORTS / "html"
LOGGER = getLogger(__name__)
AUDIT = EXPORTS / "audit"

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
    config.setdefault("runOnly", ["best-practice", "wcag22aa", "wcag22a"])
    config.setdefault("allowedOrigins", ["<same_origin>"])
    target = HTML / notebook.with_suffix(".html").name
    target.parent.mkdir(exist_ok=True, parents=True)
    LOGGER.debug(f"""injecting axe into {target.name}""")
    target.write_text(exporter.from_filename(notebook)[0])
    
    test = dict(
        exclude=["#MathJax_Message"]
    )
    page.goto(Path.as_uri(target))
    LOGGER.debug(f"""injecting axe into {target.name}""")
    page.evaluate(axe)
    LOGGER.debug(f"""auditting {target.name} with axe""")
    result = page.evaluate(f"window.axe.run({dumps(test)}, {dumps(config)})")
    AUDIT.mkdir(parents=True, exist_ok=True)
    audit = AUDIT / notebook.with_suffix(".json").name
    LOGGER.info(f"""writing {audit} with {len(result["violations"])} violations""")
    audit.write_text(dumps(result))

    assert not result["violations"], result