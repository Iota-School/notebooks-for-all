from json import dumps
from logging import getLogger
from pathlib import Path
from requests_cache import install_cache
import requests

install_cache("a11y-audit")

from pytest import mark

HERE = Path(__file__).parent
LOGGER = getLogger(__name__)
HTML = HERE.parent / "site" / "exports" / "html"
AUDIT = HTML.parent / "audit"


@mark.parametrize(
    "notebook",
    list(
        x
        for x in HTML.glob("*.html")
        if x.name not in {"Imaging_Sky_Background_Estimation-a11y.html"}
    )[:1],
)
def test_baseline_exports(page, notebook):
    config = {}
    config.setdefault("runOnly", ["best-practice", "wcag22aa", "wcag2aaa"])
    config.setdefault("allowedOrigins", ["<same_origin>"])
    source = notebook.absolute()
    page.goto(Path.as_uri(source))
    LOGGER.debug(f"""injecting axe into {source.name}""")
    page.evaluate(requests.get("https://cdn.jsdelivr.net/npm/axe-core").text)
    LOGGER.debug(f"""auditting {source.name} with axe""")
    result = page.evaluate(f"window.axe.run(window.document, {dumps(config)})")
    AUDIT.mkdir(parents=True, exist_ok=True)
    target = AUDIT / notebook.with_suffix(".json").name
    LOGGER.info(f"""writing {target} with {len(result["violations"])} violations""")
    target.write_text(dumps(result))
