from doit import task_params
from pathlib import Path
from functools import partial
import warnings

HERE = Path(__file__).parent

DOCS = Path("docs")
UTESTS = Path("user-tests")
TESTS = Path("tests")


@task_params(
    [
        dict(name="notebooks", default=[TESTS / "notebooks/lorenz.ipynb"], type=list),
        dict(name="configuration", default="tests/configurations", type=str),
        dict(name="target", default="docs/exports", type=str),
        dict(name="audit", default=True, type=bool),
    ]
)
def task_export(notebooks, configuration, target, audit):
    target = Path(target)
    rel = []

    configs = []

    for c in Path(configuration).glob("*.py"):
        for nb in map(Path, notebooks):
            name = "-".join((nb.stem, c.stem))
            t = target / (name + ".html")
            rel.append(t)
            yield dict(
                name=f"export:{name}",
                actions=[
                    f"jupyter nbconvert --config {c} --output {name} --output-dir {target} {nb}"
                ],
                file_dep=[nb, c],
                targets=[t],
                clean=True,
            )
            configs.append(
                dict(config=c, nb=nb, html=t, audit=t.parent / "data" / (t.name + ".json"))
            )

    if audit:
        from nbconvert_html5.audit import main

        audits = [x["audit"] for x in configs]
        yield dict(
            name=f"audit",
            actions=[partial(main, id=rel, output_dir=Path("docs/exports/data"))],
            targets=audits,
            file_dep=[x["html"] for x in configs],
            clean=True,
        )

    INDEX = DOCS / "index.md"

    def get_violations(targets):
        import pandas
        from json import loads

        return (
            targets.apply(lambda x: pandas.Series(loads(x.read_text())))
            .stack()
            .apply(lambda x: len(x["nodes"]))
            .unstack()
            .fillna(0)
            .sum(1)
            .to_frame("nodes in violation")
        )

    def get_index():
        body = "# sample converted notebooks\n\n"
        import pandas

        df = pandas.DataFrame(configs)

        # config and nb are relative to the github repo
        # audit and html are relative to the docs
        names = df.applymap(lambda x: x.stem)
        violations = get_violations(df.audit)
        df = pandas.concat(
            [
                df[["config", "nb"]]
                .applymap(str)
                .applymap("https://github.com/iota-school/notebooks-for-all/blob/main/".__add__),
                df[["audit", "html"]]
                .applymap(lambda x: x.relative_to("docs"))
                .applymap(str)
                .applymap("/notebooks-for-all/".__add__),
            ]
        )

        df = ("[" + names.stack() + "](" + df.stack() + ")").unstack()
        df = df.set_index("config")[["nb", "html", "audit"]]  # order the columns

        df = df.assign(violations=violations.values)
        body += df.to_markdown()

        INDEX.write_text(body)

    yield dict(name=f"index", file_dep=audits, targets=[INDEX], actions=[get_index], clean=True)


# @task_params(
#     [
#         dict(name="notebooks", default=[TESTS / "notebooks/lorenz.ipynb"], type=list),
#         dict(name="configurations", default=[TESTS / "notebooks/lorenz.ipynb"], type=list),
#         dict(name="audit", default=True, type=bool),
#     ]
# )
# def task_export(notebooks, audit):
#     """export html versions of notebooks"""
#     rel = []
#     for format in ("html", "html5"):
#         for notebook in map(Path, notebooks):
#             target = notebook.with_suffix(notebook.suffix + f".{format}.html")
#             output = DOCS / target
#             if notebook.suffix in {".html"}:
#                 yield dict(
#                     name=f"html:{format}:{notebook}",
#                     actions=[(fix_html, (notebook, output))],
#                     targets=[output],
#                     file_dep=[notebook],
#                 )
#             else:
#                 cmd = f"jupyter nbconvert --to={format} --output={target.name} --output-dir={output.parent} {notebook}"
#                 yield dict(
#                     name=f"html:{format}:{notebook}",
#                     actions=[cmd],
#                     targets=[output],
#                     file_dep=[notebook],
#                 )
#             rel.append(output)

#         rel_targets = [x.parent / "data" / ("axe-" + x.name + ".json") for x in rel]
#     if audit:
#         from nbconvert_html5.audit import main

#         yield dict(
#             name=f"audit",
#             actions=[partial(main, id=rel)],
#             targets=rel_targets,
#             file_dep=rel,
#         )

#     INDEX = DOCS / "index.md"
#     body = "# sample converted notebooks\n\n"
#     for id in rel:
#         id = id.relative_to("docs")
#         body += "* "
#         body += f"[original](https://github.com/Iota-School/notebooks-for-all/blob/main/{id}) "
#         body += f"[html](/notebooks-for-all/{id}) "
#         body += str(id)
#         body += "\n"
#     yield dict(
#         name=f"export_html:{INDEX}",
#         targets=[INDEX],
#         actions=[(lambda x: INDEX.write_text(x) and None, [body])],
#     )
