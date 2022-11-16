from doit import task_params
from pathlib import Path
import warnings

HERE = Path(__file__).parent
REL = HERE.absolute().as_uri()
TESTS = HERE / "tests"
NOTEBOOKS = TESTS / "notebooks"


def test_pally():
    yield dict(name="install", actions=["npm install"])
    for file in NOTEBOOKS.glob("*.ipynb"):
        yield dict(name="run", actions=["pally "])


DOCS = Path("docs")
UTESTS = Path("user-tests")
TESTS = Path("tests")


@task_params([dict(name="notebooks", default=[TESTS / "notebooks/lorenz.ipynb"], type=list)])
def task_export_html(notebooks):
    """export html versions of notebooks"""
    rel = []
    for format in ("html", "html5"):
        for notebook in map(Path, notebooks):
            target = notebook.with_suffix(f".{format}.html")
            output = DOCS / target
            cmd = f"jupyter nbconvert --to={format} --output={target.name} --output-dir={output.parent} {notebook}"
            yield dict(name=f"export_html:{format}:{notebook}", actions=[cmd], targets=[target], file_dep=[notebook])
            rel.append(output)

    INDEX = DOCS / "index.md"
    body = "# sample converted notebooks\n\n"
    for id in rel:
        body += "* "
        body += F"[notebook](https://github.com/Iota-School/notebooks-for-all/blob/main/{id}) "
        body += F"[html](/notebooks-for-all/{id.relative_to('docs')}) "
        body += str(id)
        body += "\n"
    yield dict(name=F"export_html:{INDEX}", targets=[INDEX], actions=[
        (lambda x: INDEX.write_text(x) and None, [body])
    ])
