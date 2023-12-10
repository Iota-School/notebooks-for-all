# requires node
# requires jvm

import collections
import functools
import itertools
import json
import operator
import pathlib
import re
import shlex
import shutil
import subprocess
from pathlib import Path

from json import dumps
from logging import getLogger
from pathlib import Path

import exceptiongroup
from pytest import mark, param


from tests.test_smoke import CONFIGURATIONS, get_target_html

EXCLUDE = re.compile(
    """or with a “role” attribute whose value is “table”, “grid”, or “treegrid”.$"""
    # https://github.com/validator/validator/issues/1125
)
VNU = shutil.which("vnu") or shutil.which("vnu.cmd")


def validate_html(*files: pathlib.Path) -> dict:
    return json.loads(
        subprocess.check_output(
            [VNU, "--stdout", "--format", "json", "--exit-zero-always",  *files]
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
            exceptions.append(
                exceptiongroup.ExceptionGroup(
                    msg, [Exception(x["extract"]) for x in collect["error"][msg]]
                )
            )
    if exceptions:
        raise exceptiongroup.ExceptionGroup("nu validator errors", exceptions)


HERE = Path(__file__).parent
NOTEBOOKS = HERE / "notebooks"
EXPORTS = HERE / "exports"
HTML = EXPORTS / "html"
LOGGER = getLogger(__name__)
VALIDATOR = EXPORTS / "validator"

# it would be possible to test loaded baseline documents with playwright.
# export the resting state document and pass them to the validator.
# this would be better validate widgets.

INVALID_MARKUP = mark.xfail(reason="invalid html markup")

htmls = mark.parametrize(
    "html",
    [
        param(
            get_target_html(
                (CONFIGURATIONS / (a := "a11y")).with_suffix(".py"),
                (NOTEBOOKS / (b := "lorenz-executed")).with_suffix(".ipynb"),
            ),
            id="-".join((b, a)),
        ),
        param(
            get_target_html(
                (CONFIGURATIONS / (a := "default")).with_suffix(".py"),
                (NOTEBOOKS / (b := "lorenz-executed")).with_suffix(".ipynb"),
            ),
            marks=[INVALID_MARKUP],
            id="-".join((b, a)),
        ),
    ],
)


@htmls
def test_baseline_w3c(page, html):
    result = validate_html(html)
    VALIDATOR.mkdir(parents=True, exist_ok=True)
    audit = VALIDATOR / html.with_suffix(".json").name
    LOGGER.info(f"""writing {audit} with {len(result.get("violations", ""))} violations""")
    audit.write_text(dumps(result))

    raise_if_errors(result)
