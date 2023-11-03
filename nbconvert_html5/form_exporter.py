"""a formal html5 approach to building static notebooks.

this design assumes __notebooks are a feed of forms__.
"""

from nbconvert.exporters.html import HTMLExporter
from contextlib import suppress
from functools import lru_cache
from json import loads
from pathlib import Path
import json
import builtins
import bs4
import pygments
from traitlets import Unicode, Bool
import nbformat.v4
import bs4
import bs4
from bs4 import BeautifulSoup

singleton = lru_cache(1)

HERE = Path(__file__).parent
TEMPLATES = HERE / "templates"


SCHEMA = nbformat.validator._get_schema_json(nbformat.v4)


def strip_comments(tag):
    for child in getattr(tag, "children", ()):
        with suppress(AttributeError):
            if isinstance(child, bs4.Comment):
                child.extract()
        strip_comments(child)
    return tag


@lru_cache
def get_markdown_renderer():
    from markdown_it import MarkdownIt
    from mdit_py_plugins.anchors import anchors_plugin

    md = MarkdownIt("gfm-like", options_update=dict(inline_definitions=True, langPrefix=""))
    md.use(anchors_plugin)
    md.options.update(highlight=highlight)
    return md


def get_markdown(md, **kwargs):
    return get_markdown_renderer().render("".join(md), **kwargs)


def highlight(code, lang="python", attrs=None):
    import pygments, html

    try:
        return pygments.highlight(
            code,
            pygments.lexers.get_lexer_by_name(lang or "python"),
            pygments.formatters.get_formatter_by_name(
                "html", debug_token_types=True, title=f"{lang} code", wrapcode=True
            ),
        )
    except:
        return f"""<pre><code>{html.escape(code)}</code></pre>"""


def get_soup(x):
    return bs4.BeautifulSoup(x, features="html5lib")


class FormExporter(HTMLExporter):
    """an embellished HTMLExporter that allows modifications of exporting and the exported.

    the `nbconvert` exporter has a lot machinery for converting notebook data into strings.
    this class introduces a `post_process` trait that allows modifications after creating html content.
    this method allows tools like `html.parser` and `bs4.BeautifulSoup` to make modifications at the end.

    changes to the template and exporter machinery are foundational changes that take time.
    post modifications make it possible to quick changes in manual testing scenarios or configure
    def post_process_code_cell(self, cell):
        pass
    A/B testing with out requiring `nbconvert` or notebook knowleldge."""

    template_file = Unicode("semantic-forms/table.html.j2").tag(config=True)
    include_axe = Bool(False).tag(config=True)
    include_settings = Bool(False).tag(config=True)
    include_cell_index = Bool(True).tag(config=True)
    exclude_anchor_links = Bool(True).tag(config=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from nbconvert.filters import strings

        for k, v in vars(strings).items():
            if callable(v):
                if not k.startswith("_"):
                    self.environment.filters.setdefault(k, v)
        self.environment.globals.update(vars(builtins))
        import html

        self.environment.globals.update(json=json, markdown=get_markdown, highlight=highlight)
        self.environment.filters.update(escape_html=html.escape)
        self.environment.globals.update(
            formatter=pygments.formatters,
            count_loc=count_loc,
            count_outputs=count_outputs,
            count_code_cells=count_code_cells,
            ordered=ordered,
            schema=SCHEMA,
        )

    def from_notebook_node(self, nb, resources=None, **kw):
        resources = resources or dict()
        resources.setdefault("include_axe", self.include_axe)
        resources.setdefault("include_settings", self.include_settings)
        html, resources = super().from_notebook_node(nb, resources, **kw)
        html = self.post_process_html(html)
        return html, resources

    def post_process_html(self, body):
        soup = soupify(body)
        describe_main(soup)
        heading_links(soup)
        details = soup.select_one("""[aria-labelledby="nb-toc"] details""")
        if details:
            details.extend(soupify(toc(soup)).body.children)
            for x in details.select("ul"):
                x.name = "ol"
            details.select_one("ol").attrs["aria-labelledby"] = "nb-toc"
        return soup.prettify(formatter="html5")


class A11yExporter(FormExporter):
    template_file = Unicode("a11y/table.html.j2").tag(config=True)


def soupify(body: str) -> BeautifulSoup:
    """convert a string of html to an beautiful soup object"""
    return BeautifulSoup(body, features="html5lib")


def mdtoc(html):
    import io

    toc = io.StringIO()
    for header in html.select("#cells :is(h1,h2,h3,h4,h5,h6)"):
        id = header.attrs.get("id")
        if not id:
            from slugify import slugify

            id = slugify(header.string)

        # there is missing logistics for managely role=heading
        # adding code group semantics will motivate this addition

        l = int(header.name[-1])
        toc.write("  " * (l - 1) + f"* [{header.string}](#{id})\n")
    return toc.getvalue()


def toc(html):
    return get_markdown(mdtoc(html))


def heading_links(html):
    for header in html.select(":is(h1,h2,h3,h4,h5,h6):not([role])"):
        id = header.attrs.get("id")
        if not id:
            from slugify import slugify

            id = slugify(header.string)

        link = soupify(f"""<a href="#{id}">{header.string}</a>""").body.a
        header.clear()
        header.append(link)


# * navigate links
# * navigate headers
# * navigate table
# * navigate landmarks


def count_loc(nb):
    return sum(map(len, (x.source.splitlines() for x in nb.cells)))


def count_outputs(nb):
    return sum(map(len, (x.get("outputs", "") for x in nb.cells)))


def count_code_cells(nb):
    return len(list(None for x in nb.cells if x["cell_type"] == "code"))


def describe_main(soup):
    x = soup.select_one("#toc > details > summary")
    if x:
        x.attrs["aria-describedby"] = soup.select_one("main").attrs[
            "aria-describedby"
        ] = (
            desc
        ) = "nb-cells-count-label nb-cells-label nb-code-cells nb-code-cells-label nb-ordered nb-loc nb-loc-label"


def ordered(nb):
    start = 0
    for cell in nb.cells:
        if cell["cell_type"] == "code":
            start += 1
            if start != cell["execution_count"]:
                if start:
                    return "executed out of order"
    if start:
        return "executed in order"
    return "unexecuted"
