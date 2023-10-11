"""a formal html5 approach to building static notebooks.

this design assumes __notebooks are a feed of forms__.
"""

from nbconvert.exporters.html import HTMLExporter
from contextlib import suppress
from copy import copy, deepcopy
import enum
from functools import lru_cache
from json import loads
from pathlib import Path
from webbrowser import get
import json
import builtins
import bs4
import pygments
from traitlets import Unicode
import nbconvert_html5
import pydantic
import nbformat.v4
import markupsafe
import bs4
import nbconvert_html5
import bs4
from bs4 import BeautifulSoup

singleton = lru_cache(1)

HERE = Path(__file__).parent
TEMPLATES = HERE / "templates"
TEMPLATE = TEMPLATES / "html-templates.html"

# this file contains a template tag that holds the skeleton for notebooks and a cell.

formatter = pygments.formatters.find_formatter_class("html")(style="a11y-light", wrapcode=True)
lex = pygments.lexers.find_lexer_class("IPython3")()


def get_highlighted(x):
    return pygments.highlight(x, lex, formatter)


def strip_comments(tag):
    for child in getattr(tag, "children", ()):
        with suppress(AttributeError):
            if isinstance(child, bs4.Comment):
                child.extract()
        strip_comments(child)
    return tag


class Base(pydantic.BaseModel):
    pass


class T:
    class Notebook(Base):
        class Cell(Base):
            class CellType(enum.Enum):
                raw = "raw"
                markdown = "markdown"
                code = "code"

            cell_type: CellType
            id: str
            source: list[str] | str
            metadata: dict

        class Code(Cell):
            class DisplayData(Base):
                data: dict
                metadata: dict

            class Stdout(Base):
                pass

            class Stderr(Base):
                pass

            execution_count: int | None
            outputs: list[DisplayData | Stdout | Stderr] | None = None

        class Md(Cell):
            attachments: dict | None

        metadata: dict
        cells: list[Cell]
        nbformat_minor: int
        nbformat: int


@singleton
def load_entire_template() -> bs4.BeautifulSoup:
    return strip_comments(get_soup(TEMPLATE.read_text()))


class Notebook(T.Notebook):
    file: Path

    def __init__(self, file, **kwargs):
        if not isinstance(file, dict):
            kwargs.update(loads(Path(file).read_text()))
        super().__init__(file=file, **kwargs)

    def get_doc(self):
        doc = deepcopy(load_entire_template())
        pygments = bs4.Tag(name="style")
        doc.select_one("head").append(pygments)
        pygments.string = formatter.get_style_defs()

        doc.select_one("title").string = str(self.file)

        cells = doc.select_one("section#cells")
        for i, cell in enumerate(self.cells, 1):
            article = Cell(**cell.dict()).get_article(i, len(self.cells))
            cells.append(article)
        doc.select_one("head>template#cell").extract()
        return doc


class Cell(T.Notebook.Cell):
    def __new__(cls, cell_type=None, **kwargs):
        cls = {
            T.Notebook.Cell.CellType.code.value: Code,
            T.Notebook.Cell.CellType.markdown.value: Markdown,
            T.Notebook.Cell.CellType.raw.value: Raw,
        }.get(cell_type.value, cls)
        self = super(type, cls).__new__(cls)
        self.__init__(cell_type=cell_type, **kwargs)
        return self

    def get_template(self) -> bs4.BeautifulSoup:
        """get an html template as a beautiful soup object"""
        return deepcopy(load_cell_template().select_one("article"))

    def _repr_html_(self):
        return str(self.get_article())

    def set_cell_article(self):
        pass

    def get_article(self, count: int = 0, max: int = -1):
        # no captions on markdown cells
        article = self.get_template()
        ID = lambda x="": "-".join(filter(bool, ["cell", x, str(count)]))

        # define the aria properties for the enclosing article tag
        # the article has an ordinal id
        article.attrs["class"] += [self.cell_type.value]
        article.attrs.update(
            {
                "id": ID(),
                "aria-labelledby": ID("name"),
                "aria-describedby": ID("description"),
                "aria-posinset": count,
                "aria-setsize": max,
            }
        )

        # give the inner a form a lexical id
        form = article.select_one("form")
        form.attrs.update(id=self.id or ID("form"))
        input = form.select_one("fieldset[name=input]")
        input.select_one("legend").attrs["id"] = ID("name")
        input.select_one("label.index").string = str(count)
        input.select_one("label.total").string = str(max)

        article.select_one("textarea[name=description]").attrs.update(id=ID("description"))

        output = article.select_one("fieldset[name=input] output")
        source = "".join(self.source)

        output.append(get_soup(get_highlighted(source)))
        # set the markdown source inside a readonly hidden fieldset
        article.select_one("textarea[name=source]").string = source

        return article


class Raw(Cell):
    pass


class Code(T.Notebook.Code, Cell):
    def get_article(self, count: int = 0, max: int = -1):
        article = super().get_article(count, max)
        for j, output in enumerate(self.outputs or ()):
            """if "data" in output:
            out = DisplayData(**output).get_output(i, j)
            article.append(out)"""
        if not self.outputs:
            article.select_one("fieldset[name=output]").attrs["hidden"] = None
        return article


class Markdown(T.Notebook.Md, Cell):
    def get_article(self, count: int = 0, max: int = -1):
        return super().get_article(count, max)


class DisplayData(T.Notebook.Code.DisplayData):
    _dispatchers = dict()

    def __class_getitem__(cls, type):
        return cls._dispatchers.get(type, cls)

    def __init_subclass__(cls, type=None):
        if type:
            cls._dispatchers[type] = cls

    def get_priority_type(cls):
        return cls[next(filter(self.data.__contains__, get_display_data_priority()), cls)]

    def __new__(cls, data, metadata, parent):
        cls = get_priority_type(data)
        self = super(type, cls).__new__(cls)
        self.__init__(data, metadata, parent)
        return self

    def get_output(self, cell: int = None, output: int = None):
        tag = bs4.Tag("output")
        if all(x is not None for x in (cell, outputs)):
            tag.attrs.update(id=f"cell-{cell}-output-{output}")
        return tag


class DisplayJavascript(DisplayData, type="application/javascript"):
    def get_output(self, cell: int = None, output: int = None):
        parent = super().get_output(cell, output)
        script = bs4.Tag(name="script", type=Javascript.type)
        parent.append(script)
        script.string = self.data[Javascript.type]
        return parent


class DisplayHtml(DisplayData, type="text/html"):
    def get_output(self, cell: int = None, output: int = None):
        parent = super().get_output(cell, output)
        parent.extend(bs4.BeautifulSoup(self.data[Html.type]).children)
        return parent


class DisplayMarkdown(DisplayHtml, type="text/markdown"):
    def get_output(self, data, metadata, parent):
        parent = super().get_output(cell, output)
        parent.extend(bs4.BeautifulSoup(get_markdown(data[Markdown.type])).children)
        return parent


@singleton
def load_cell_template():
    return load_entire_template().select_one("head>template#cell")


@singleton
def get_display_data_priority() -> list:
    """>>> get_display_data_priority()
    ['application/vnd.jupyter.widget-view+json', 'application/javascript', 'text/html', 'text/markdown', 'image/svg+xml', 'text/latex', 'image/png', 'image/jpeg', 'text/plain']
    """

    return __import__("nbconvert").get_exporter("html")().config.NbConvertBase.display_data_priority


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
    return bs4.BeautifulSoup(x, features="html.parser")


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
    exclude_anchor_links = True

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
        )

    def from_notebook_node(self, nb, resources=None, **kw):
        html, resources = super().from_notebook_node(nb, resources, **kw)
        html = self.post_process_html(html)
        return html, resources

    def post_process_html(self, body):
        soup = soupify(body)
        describe_main(soup)
        heading_links(soup)
        details = soup.select_one("""[aria-labelledby="nb-toc"] details""")
        if details:
            details.extend(soupify(toc(soup)).children)
            for x in details.select("ul"):
                x.name = "ol"
            details.select_one("ol").attrs["aria-labelledby"] = "nb-toc"
        return soup.encode(formatter="html5")


def soupify(body: str) -> BeautifulSoup:
    """convert a string of html to an beautiful soup object"""
    return BeautifulSoup(body, features="html.parser")


def mdtoc(html):
    import io

    toc = io.StringIO()
    for header in html.select("h1,h2,h3,h4,h5,h6"):
        id = header.attrs.get("id")
        l = int(header.name[-1])
        toc.write("  " * (l - 1) + f"* [{header.string}](#{header.attrs.get('id')})\n")
    return toc.getvalue()


def toc(html):
    return get_markdown(mdtoc(html))


def heading_links(html):
    for header in html.select("h1,h2,h3,h4,h5,h6"):
        id = header.attrs.get("id")
        if not id:
            from slugify import slugify

            id = slugify(header.string)
        if id:
            link = soupify(f"""<a href="#{id}">{header.encode_contents().decode()}</a>""")
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
