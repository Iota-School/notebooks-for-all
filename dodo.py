from pathlib import Path


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


def task_render(notebooks: list[Path] = [
    UTESTS / "1-navigation/stsci_example_notebook.ipynb",
    TESTS / "notebooks/lorenz.ipynb",
    TESTS / "notebooks/lorenz-executed.ipynb"
]):
    rel = []
    for format in ("html", "html5"):
        for notebook in notebooks:
            target = notebook.with_suffix(f".{format}.html")
            output = DOCS / target
            cmd = f"jupyter nbconvert --to={format} --output={target.name} --output-dir={output.parent} {notebook}"
            yield dict(name=f"render:{format}:{notebook}", actions=[cmd])
            rel.append(
                output.absolute().as_uri()[len(DOCS.absolute().as_uri()):]
            )
    print(rel)