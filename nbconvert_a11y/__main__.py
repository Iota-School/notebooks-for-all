"""__main__.py."""
# this application can have a few developer affordances.
# * rendering & serving templates
# * run accessibility tests
from pathlib import Path

from typer import Typer

from .audit import main as audit

app = Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    rich_markup_mode="rich",
    add_completion=False,
    no_args_is_help=True,
)


@app.command()
def generate_config(
    dir: Path = Path.cwd(), name: str = "jupyter_nbconvert_config.py", force: bool = False
):
    """Generate a default config file for accessibility testing."""
    from .exporters import Html5

    if force and (dir / name).exists():
        (dir / name).unlink()
    Html5.write_config(dir, name)


app.command(name="audit")(audit)

if __name__ == "__main__":
    app()
