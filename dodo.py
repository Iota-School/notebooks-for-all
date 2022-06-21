from pathlib import Path


DIR = Path(__file__).parent
TESTS = DIR / "tests"
NOTEBOOKS = TESTS / "notebooks"
def test_pally():
    yield dict(name="install", actions=[
        "npm install"
    ])
    for file in NOTEBOOKS.glob("*.ipynb"):
        yield dict(name="run", actions=[
            "pally "
        ])