# requires node
# requires jvm

import itertools, operator, functools, collections, exceptiongroup, re
import pathlib, json, subprocess, shlex

EXCLUDE = re.compile(
    """or with a “role” attribute whose value is “table”, “grid”, or “treegrid”.$"""
    # https://github.com/validator/validator/issues/1125
)


@functools.lru_cache(1)
def vnu_jar():
    VNU_JAR = (
        pathlib.Path(subprocess.check_output(shlex.split("npm root vnu-jar")).strip().decode())
        / "vnu-jar/build/dist/vnu.jar"
    )
    assert VNU_JAR.exists()
    return VNU_JAR


def validate_html(*files: pathlib.Path) -> dict:
    return json.loads(
        subprocess.check_output(
            shlex.split(f"java -jar {vnu_jar()} --stdout --format json --exit-zero-always")
            + list(files)
        ).decode()
    )


def organize_validator_results(results):
    collect = collections.defaultdict(functools.partial(collections.defaultdict, list))
    for (error, msg), group in itertools.groupby(
        results["messages"], key=operator.itemgetter("type", "message")
    ):
        for item in group:
            collect[error][msg].append(item)
    return collect

def raise_if_errors(results, exclude=EXCLUDE):
    collect = organize_validator_results(results)
    exceptions = []
    for msg in collect["error"]:
        if not exclude or not exclude.search(msg):
            exceptions.append(exceptiongroup.ExceptionGroup(msg, [Exception(x["extract"]) for x in collect["error"][msg]]))
    if exceptions:
            raise exceptiongroup.ExceptionGroup("nu validator errors", exceptions)


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
VALIDATOR = EXPORTS / "validator"

# it would be possible to test loaded baseline documents with playwright.
# export the resting state document and pass them to the validator. 
# this would be better validate widgets.

@mark.parametrize(
    "notebook",
    list(
        x
        for x in NOTEBOOKS.glob("*.ipynb")
        if x.name not in {"Imaging_Sky_Background_Estimation.ipynb"}
    ),
)
def test_baseline_w3c(page, exporter, notebook):
    config = {}
    config.setdefault(
        "runOnly",
        ["act", "best-practice", "experimental", "wcag21a", "wcag21aa", "wcag22aa"],
    )
    target = HTML / notebook.with_suffix(".html").name
    target.parent.mkdir(exist_ok=True, parents=True)
    target.write_text(exporter.from_filename(notebook)[0])

    result = validate_html(target)
    VALIDATOR.mkdir(parents=True, exist_ok=True)
    audit = VALIDATOR / notebook.with_suffix(".json").name
    LOGGER.info(f"""writing {audit} with {len(result.get("violations", ""))} violations""")
    audit.write_text(dumps(result))

    raise_if_errors(result)