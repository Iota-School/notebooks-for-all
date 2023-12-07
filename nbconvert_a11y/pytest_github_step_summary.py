from dataclasses import dataclass, field
from io import StringIO
from os import environ
from pathlib import Path
from sys import modules

TARGET = Path(environ.get("GITHUB_STEP_SUMMARY", "github-step-summary.md"))

if "pytest" in modules:
    from pytest import fixture

    @fixture(scope="session")
    def github_summary():
        summary = Summary()
        yield Summary()
        summary.write()


@dataclass
class Summary:
    buffer: StringIO = field(default_factory=StringIO)

    def append(self, body):
        self.buffer.write(body)

    def write(self):
        with TARGET.open("a") as file:
            print(self.buffer.getvalue(), file=file)
            self.buffer = StringIO()
