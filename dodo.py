from doit import task_params
from pathlib import Path
from functools import partial
import warnings

HERE = Path(__file__).parent

DOCS = Path("docs")
UTESTS = Path("user-tests")
TESTS = Path("tests")


def fix_html(path, to):
    from nbconvert_html5.modifiers import set_notebook

    to.parent.mkdir(exist_ok=True, parents=True)
    to.write_text(str(set_notebook(path.read_text())))


@task_params(
    [
        dict(name="notebooks", default=[TESTS / "notebooks/lorenz.ipynb"], type=list),
        dict(name="audit", default=True, type=bool),
    ]
)
def task_export(notebooks, audit):
    """export html versions of notebooks"""
    rel = []
    for format in ("html", "html5"):
        for notebook in map(Path, notebooks):
            target = notebook.with_suffix(notebook.suffix + f".{format}.html")
            output = DOCS / target
            if notebook.suffix in {".html"}:
                yield dict(
                    name=f"html:{format}:{notebook}",
                    actions=[(fix_html, (notebook, output))],
                    targets=[output],
                    file_dep=[notebook],
                )
            else:
                cmd = f"jupyter nbconvert --to={format} --output={target.name} --output-dir={output.parent} {notebook}"
                yield dict(
                    name=f"html:{format}:{notebook}",
                    actions=[cmd],
                    targets=[output],
                    file_dep=[notebook],
                )
            rel.append(output)

        rel_targets = [x.parent / "data" / ("axe-" + x.name + ".json") for x in rel]
    if audit:
        from nbconvert_html5.audit import main

        yield dict(
            name=f"audit",
            actions=[partial(main, id=rel)],
            targets=rel_targets,
            file_dep=rel,
        )

    INDEX = DOCS / "index.md"
    body = "# sample converted notebooks\n\n"
    for id in rel:
        id = id.relative_to("docs")
        body += "* "
        body += f"[original](https://github.com/Iota-School/notebooks-for-all/blob/main/{id}) "
        body += f"[html](/notebooks-for-all/{id}) "
        body += str(id)
        body += "\n"
    yield dict(
        name=f"export_html:{INDEX}",
        targets=[INDEX],
        actions=[(lambda x: INDEX.write_text(x) and None, [body])],
    )
