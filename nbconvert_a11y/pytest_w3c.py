# requires node
# requires jvm
import collections
import functools
import itertools
import operator
import os
import re
import shutil
import socket
import sys
import time
import uuid
from json import loads
from pathlib import Path
from subprocess import Popen, check_output
from typing import Any, Callable, Dict, Generator, Tuple
from urllib.request import urlopen

import exceptiongroup
import pytest
import requests

from nbconvert_a11y.pytest_axe import Collector, Results, Violation

HERE = Path(__file__).parent

ENV_JAVA_PATH = "NBA11Y_JAVA_PATH"
ENV_VNU_JAR_PATH = "NBA11Y_VNU_JAR_PATH"
ENV_VNU_SERVER_URL = "NBA11Y_VNU_SERVER_URL"

TVnuResults = Dict[str, Any]
TVnuValidator = Callable[[Path], TVnuResults]

EXCLUDE = re.compile(
    """or with a “role” attribute whose value is “table”, “grid”, or “treegrid”.$"""
    # https://github.com/validator/validator/issues/1125
)


class Validator(Collector):
    server_url: Any = None

    def run(self):
        if self.server_url:
            self.results = ValidatorResults(validate_path(self.server_url, self.url))
        else:
            self.results = ValidatorResults(validate_url(self.url))
        return self


class ValidatorViolation(Violation):
    type: Any = None
    url: Any = None
    firstLine: Any = None
    lastLine: Any = None
    lastColumn: Any = None
    firstColumn: Any = None
    message: Any = None
    extract: Any = None
    subType: Any = None
    hiliteStart: Any = None
    hiliteLength: Any = None
    map = {}

    @classmethod
    def from_violations(cls, data):
        out = []
        for message in (messages := data.get("messages")):
            out.append(ValidatorViolation(**message))

        return exceptiongroup.ExceptionGroup(f"{len(messages)} html violations", out)

    @classmethod
    def cast(cls, message):
        CSS_START = re.compile(r"""^“\S+”:""")
        t = (ValidatorViolation[message["type"]],)
        if message.get("subType"):
            t += (ValidatorViolation[message.get("subType")],)
        msg = message["message"]
        if msg.startswith("CSS:"):
            msg = msg[5:]
            t += (ValidatorViolation["css"],)
            if CSS_START.match(msg):
                prop, _, msg = msg.partition(": ")
                t += (ValidatorViolation[prop[1:-1]],)
                id = f"""{message["type"]}-{prop[1:-1]}"""
            else:
                id = f"""{message["type"]}-{msg.strip()}"""
        else:
            id = f"""{message["type"]}-{msg.strip()}"""
            msg = message["extract"]
        return cls.map.setdefault(id, type(id, t, {}))


class ValidatorResults(Results):
    def exception(self):
        if self.data["messages"]:
            return ValidatorViolation.from_violations(self.data)


def get_vnu_path():
    return shutil.which("vnu") or shutil.which("vnu.cmd")


def validate_url(url):
    return loads(
        check_output([get_vnu_path(), "--stdout", "--format", "json", "--exit-zero-always", url])
    )


@pytest.fixture()
def validate_html_url():
    def go(url):
        return Validator(url=url)

    return go


@pytest.fixture()
def validate_html_path(a_vnu_server_url: str) -> TVnuValidator:
    def go(url):
        return Validator(url=url, server_url=a_vnu_server_url)

    return go


def validate_path(a_vnu_server_url, path: Path) -> TVnuResults:
    url = f"{a_vnu_server_url}?out=json"
    data = path.read_bytes()
    headers = {"Content-Type": "text/html"}
    res = requests.post(url, data, headers=headers)
    return res.json()


@pytest.fixture(scope="session")
def validate_html_file(a_vnu_server_url: str) -> TVnuValidator:
    """Wrap the nvu validator REST API in a synchronous request

    https://github.com/validator/validator/wiki/Service-%C2%BB-Input-%C2%BB-POST-body
    """

    def post(path: Path | str) -> TVnuResults:
        url = f"{a_vnu_server_url}?out=json"
        data = path.read_bytes()
        headers = {"Content-Type": "text/html"}
        res = requests.post(url, data, headers=headers)
        return res.json()

    return post


@pytest.fixture(scope="session")
def a_vnu_server_url(
    worker_id: str, tmp_path_factory: pytest.TempPathFactory
) -> Generator[None, None, str]:
    """Get the URL for a running VNU server."""
    url: str | None = os.environ.get(ENV_VNU_SERVER_URL)

    if url is not None:
        return url

    proc: Popen | None = None
    owns_lock = False
    proto = "http"
    host = "127.0.0.1"
    root_tmp_dir = tmp_path_factory.getbasetemp().parent
    lock_dir = root_tmp_dir / "vnu_server"
    needs_lock = lock_dir / f"test-{uuid.uuid4()}"

    if worker_id == "master":
        port, url, proc = _start_vnu_server(proto, host)
        owns_lock = True
    else:
        port = None
        retries = 10

        try:
            lock_dir.mkdir()
            owns_lock = True
        except:
            pass

        needs_lock.mkdir()

        if owns_lock:
            port, url, proc = _start_vnu_server(proto, host)
            (lock_dir / f"port-{port}").mkdir()
        else:
            while retries:
                retries -= 1
                try:
                    port = int(next(lock_dir.glob("port-*")).name.split("-")[-1])
                    url = f"{proto}://{host}:{port}"
                except:
                    time.sleep(1)
            if port is None and not retries:
                raise RuntimeError("Never started vnu server")

    yield url

    if needs_lock.exists():
        shutil.rmtree(needs_lock)

    if owns_lock:
        while True:
            needs = [*lock_dir.glob("test-*")]
            if needs:
                time.sleep(1)
                continue
            break

        print(f"... tearing down vnu server at {url}")
        proc.terminate()
        if lock_dir.exists():
            shutil.rmtree(lock_dir)


# utilities
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


def _start_vnu_server(proto: str, host: str) -> Tuple[str, Popen]:
    """Start a vnu HTTP server."""
    port = get_an_unused_port()
    url = f"{proto}://{host}:{port}/"
    server_args = get_vnu_args(host, port)
    url = f"{proto}://{host}:{port}"
    print(f"... starting vnu server at {url}")
    print(">>>", "\t".join(server_args))
    proc = Popen(server_args)
    wait_for_vnu_to_start(url)
    print(f"... vnu server started at {url}")

    return port, url, proc


def wait_for_vnu_to_start(url: str, retries: int = 10, sleep: int = 1):
    last_error = None

    time.sleep(sleep)

    while retries:
        retries -= 1
        try:
            return urlopen(url, timeout=sleep)
        except Exception as err:
            last_error = err
            time.sleep(sleep)

    raise RuntimeError(f"{last_error}")


def get_vnu_args(host: str, port: int):
    win = os.name == "nt"

    java = Path(os.environ.get(ENV_JAVA_PATH, shutil.which("java") or shutil.which("java.exe")))
    jar = Path(
        os.environ.get(
            ENV_JAVA_PATH, (Path(sys.prefix) / ("Library/lib" if win else "lib") / "vnu.jar")
        )
    )

    if any(not j.exists() for j in [java, jar]):
        raise RuntimeError(
            "Failed to find java or vnu.jar:\b"
            f"  - {java.exists()} {java}"
            "\n"
            f"  - {jar.exists()} {jar}"
        )

    server_args = [
        java,
        "-cp",
        jar,
        f"-Dnu.validator.servlet.bind-address={host}",
        "nu.validator.servlet.Main",
        port,
    ]

    return list(map(str, server_args))


def get_an_unused_port() -> Callable[[], int]:
    """Find an unused network port (could still create race conditions)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port
