"""a formal html5 approach to building static notebooks.

this design assumes __notebooks are a feed of forms__.
"""

import builtins
import json
from contextlib import suppress
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import bs4
import nbformat.v4
import pygments
from bs4 import BeautifulSoup
from nbconvert.exporters.html import HTMLExporter
from traitlets import Bool, CUnicode, Enum, Unicode
from traitlets.config import Config

singleton = lru_cache(1)

HERE = Path(__file__).parent
TEMPLATES = HERE / "templates"

AXE_VERSION = "4.8.2"
AXE = f"https://cdnjs.cloudflare.com/ajax/libs/axe-core/{AXE_VERSION}/axe.min.js"
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

    md = MarkdownIt("gfm-like", options_update={"inline_definitions": True, "langPrefix": ""})
    md.use(anchors_plugin)
    md.options.update(highlight=highlight)
    return md


def get_markdown(md, **kwargs):
    return get_markdown_renderer().render("".join(md), **kwargs)


def highlight(code, lang="python", attrs=None, experimental=True):
    import html

    import pygments

    if lang == "code":
        lang = "python"
    elif lang == "raw":
        return ""

    lang = lang or pygments.lexers.get_lexer_by_name(lang or "python")

    formatter = pygments.formatters.get_formatter_by_name(
        "html", debug_token_types=True, title=f"{lang} code", wrapcode=True
    )
    try:
        return pygments.highlight(
            code, pygments.lexers.get_lexer_by_name(lang or "python"), formatter
        )
    except BaseException as e:
        print(code, e)

    return f"""<pre><code>{html.escape(code)}</code></pre>"""


def get_soup(x):
    return bs4.BeautifulSoup(x, features="html5lib")


THEMES = {
    "a11y": "a11y-{}",
    "a11y-high-contrast": "a11y-high-contrast-{}",
    "gh": "github-{}",
    "gh-colorblind": "github-{}-colorblind",
    "gh-high": "github-{}-high-contrast",
    "gotthard": "gotthard-{}",
    "blinds": "blinds-{}",
}


class FormExporter(HTMLExporter):
    """an embellished HTMLExporter that allows modifications of exporting and the exported.

    the `nbconvert` exporter has a lot machinery for converting notebook data into strings.
    this class introduces a `post_process` trait that allows modifications after creating html content.
    this method allows tools like `html.parser` and `bs4.BeautifulSoup` to make modifications at the end.

    changes to the template and exporter machinery are foundational changes that take time.
    post modifications make it possible to quick changes in manual testing scenarios or configure
    def post_process_code_cell(self, cell):
        pass
    A/B testing with out requiring `nbconvert` or notebook knowleldge.
    """

    template_file = Unicode("semantic-forms/table.html.j2").tag(config=True)
    include_axe = Bool(False).tag(config=True)
    axe_url = CUnicode(AXE).tag(config=True)
    include_settings = Bool(True).tag(config=True)
    include_help = Bool(True).tag(config=True)
    include_toc = Bool(True).tag(config=True)
    wcag_priority = Enum(["AAA", "AA", "A"], "AA").tag(config=True)
    accesskey_navigation = Bool(True).tag(config=True)
    include_cell_index = Bool(True).tag(config=True)
    exclude_anchor_links = Bool(True).tag(config=True)
    code_theme = Enum(list(THEMES), "gh-high").tag(config=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        from nbconvert.filters import strings

        for k, v in vars(strings).items():
            if callable(v) and not k.startswith("_"):
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
            datetime=datetime,
        )

    def from_notebook_node(self, nb, resources=None, **kw):
        resources = resources or {}
        resources["include_axe"] = self.include_axe
        resources["include_settings"] = self.include_settings
        resources["include_help"] = self.include_help
        resources["include_toc"] = self.include_toc
        resources["wcag_priority"] = self.wcag_priority
        resources["accesskey_navigation"] = self.accesskey_navigation
        resources["code_theme"] = THEMES[self.code_theme]
        resources["axe_url"] = self.axe_url

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

    @property
    def default_config(self):
        c = super().default_config
        c.merge(
            {
                "CSSHTMLHeaderPreprocessor": {"enabled": False},
            }
        )
        return c


class A11yExporter(FormExporter):
    template_file = Unicode("a11y/table.html.j2").tag(config=True)


def soupify(body: str) -> BeautifulSoup:
    """Convert a string of html to an beautiful soup object."""
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

        level = int(header.name[-1])
        toc.write("  " * (level - 1) + f"* [{header.string}](#{id})\n")
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
    return len([None for x in nb.cells if x["cell_type"] == "code"])


def describe_main(soup):
    x = soup.select_one("#toc > details > summary")
    if x:
        x.attrs["aria-describedby"] = soup.select_one("main").attrs[
            "aria-describedby"
        ] = "nb-cells-count-label nb-cells-label nb-code-cells nb-code-cells-label nb-ordered nb-loc nb-loc-label"


def ordered(nb) -> str:
    start = 0
    for cell in nb.cells:
        if cell["cell_type"] == "code":
            start += 1
            if start != cell["execution_count"] and start:
                return "executed out of order"
    if start:
        return "executed in order"
    return "unexecuted"
