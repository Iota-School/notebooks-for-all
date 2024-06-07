"""a formal html5 approach to building static notebooks.

this design assumes __notebooks are a feed of forms__.
"""

import builtins
from copy import copy, deepcopy
import json
from contextlib import suppress
from datetime import datetime
from functools import lru_cache
from io import StringIO
from pathlib import Path

import bs4
import nbformat.v4
import pygments
from bs4 import BeautifulSoup
from traitlets import Bool, CUnicode, Enum, Unicode

from nbconvert import Exporter
from nbconvert.exporters.html import HTMLExporter

singleton = lru_cache(1)

HERE = Path(__file__).parent
TEMPLATES = HERE / "templates"

AXE_VERSION = "4.8.2"
AXE = f"https://cdnjs.cloudflare.com/ajax/libs/axe-core/{AXE_VERSION}/axe.min.js"
SCHEMA = nbformat.validator._get_schema_json(nbformat.v4)


class Roles:
    """different aria settings for the notebook respresentation"""

    options = "Presentation", "Group", "Region", "List", "Table"

    class Presentation:
        table = "none"
        rowgroup = "none"
        row = "none"
        columnheader = "none"
        rowheader = "none"
        cell = "none"

    class Group(Presentation):
        row = "group"

    class Region(Presentation):
        row = "region"

    class List(Presentation):
        rowgroup = "list"
        row = "listitem"

    class Table:
        table = "table"
        rowgroup = "rowgroup"
        row = "row"
        columnheader = "columnheader"
        rowheader = "rowheader"
        cell = "cell"


THEMES = {
    "a11y": "a11y-{}",
    "a11y-high-contrast": "a11y-high-contrast-{}",
    "gh": "github-{}",
    "gh-colorblind": "github-{}-colorblind",
    "gh-high": "github-{}-high-contrast",
    "gotthard": "gotthard-{}",
    "blinds": "blinds-{}",
}


class PostProcess(HTMLExporter):
    """an exporter that allows post processing after the templating step

    this class introduces the `post_process_html` protocol that can be used to modify
    exported html.
    """

    def from_notebook_node(self, nb, resources=None, **kw):
        html, resources = super().from_notebook_node(nb, resources, **kw)
        html = self.post_process_html(html) or html
        return html, resources

    def post_process_html(self, body): ...


class A11yExporter(PostProcess):
    """an accessible reference implementation for computational notebooks implemented for ipynb files.

    this template provides a flexible screen reader experience with settings to control and customize the reading experience.
    """

    template_file = Unicode("a11y/table.html.j2").tag(config=True)
    include_axe = Bool(False, help="include axe auditing tools in the rendered page.").tag(
        config=True
    )
    axe_url = CUnicode(AXE, help="the remote source for the axe resources.").tag(config=True)
    include_sa11y = Bool(True, help="include sa11y accessibility authoring tool").tag(config=True)
    include_settings = Bool(True, help="include configurable accessibility settings dialog.").tag(
        config=True
    )
    # if help is not included the a bunch of aria label get fucked up and we fail
    # accessibility. if help information isn't included then we'll at least to included
    # a vocabulary to reference from the aria-labelledby aria-describedby
    include_help = Bool(
        True, help="include help and supplementary descriptions about notebooks and cells"
    ).tag(config=True)
    include_toc = Bool(
        True, help="collect a table of contents of the headings in the document"
    ).tag(config=True)
    include_summary = Bool(True, help="collect notebook properties into a summary").tag(config=True)
    wcag_priority = Enum(
        ["AAA", "AA", "A"], "AA", help="the default inital wcag priority to start with"
    ).tag(config=True)
    accesskey_navigation = Bool(
        True, help="use numeric accesskeys to access the first 10 cells"
    ).tag(config=True)
    include_cell_index = Bool(
        True, help="show the ordinal cell index, typically this is ignored from notebooks."
    ).tag(config=True)
    include_visibility = Bool(True, help="include visibility toggle").tag(config=True)
    include_upload = Bool(False, help="include template for uploading new content").tag(config=True)
    allow_run_mode = Bool(False, help="enable buttons for a run mode").tag(config=True)
    hide_anchor_links = Bool(False).tag(config=True)
    hidden_anchor_links = Bool(False).tag(config=True)
    code_theme = Enum(list(THEMES), "gh-high", help="an accessible pygments dark/light theme").tag(
        config=True
    )
    table_pattern = Enum(
        list(Roles.options),
        "List",
        help="the presentation format of the cells to assistive technology",
    ).tag(config=True)
    # TF: id love for these definitions to have their own parent class.
    prompt_in = CUnicode("In").tag(config=True)
    prompt_out = CUnicode("Out").tag(config=True)
    prompt_left = CUnicode("[").tag(config=True)
    prompt_right = CUnicode("]").tag(config=True)
    validate_nb = Bool(False).tag(config=True)
    exclude_anchor_links = Bool(True).tag(config=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        from nbconvert.filters import strings

        for k, v in vars(strings).items():
            if callable(v) and not k.startswith("_"):
                self.environment.filters.setdefault(k, v)
        self.environment.globals.update(vars(builtins))
        import html

        self.environment.globals.update(json=json, markdown=get_markdown, highlight=highlight)
        self.environment.filters.update(
            escape_html=html.escape,
            count_loc=count_loc,
            count_cell_loc=count_cell_loc,
            count_outputs=count_outputs,
            count_code_cells=count_code_cells,
            is_ordered=is_ordered,
        )
        self.environment.globals.update(
            formatter=pygments.formatters,
            schema=SCHEMA,
            datetime=datetime,
        )

    @property
    def default_config(self):
        c = super().default_config
        c.merge(
            {
                "CSSHTMLHeaderPreprocessor": {"enabled": False},
            }
        )
        return c

    def init_resources(self, resources=None):
        resources = self._init_resources(resources)
        resources["include_axe"] = self.include_axe
        resources["include_settings"] = self.include_settings
        resources["include_help"] = self.include_help
        resources["include_toc"] = self.include_toc
        resources["include_summary"] = self.include_summary
        resources["include_visibility"] = self.include_visibility
        resources["include_upload"] = self.include_upload
        resources["wcag_priority"] = self.wcag_priority
        resources["accesskey_navigation"] = self.accesskey_navigation
        resources["code_theme"] = THEMES[self.code_theme]
        resources["axe_url"] = self.axe_url
        resources["include_sa11y"] = self.include_sa11y
        resources["prompt_in"] = self.prompt_in
        resources["prompt_out"] = self.prompt_out
        resources["prompt_left"] = self.prompt_left
        resources["prompt_right"] = self.prompt_right
        resources["hidden_anchor_links"] = self.hidden_anchor_links
        resources["hide_anchor_links"] = self.hide_anchor_links
        resources["table_pattern"] = getattr(Roles, self.table_pattern)
        resources["allow_run_mode"] = self.allow_run_mode
        return resources

    def from_notebook_node(self, nb, resources=None, **kw):
        # this is trash and needs serious fixing

        return super().from_notebook_node(nb, self.init_resources(resources), **kw)

    def post_process_html(self, body):
        """A final pass at the exported html to add table of contents, heading links, and other a11y affordances."""
        soup = soupify(body)
        heading_links(soup)
        if self.include_toc:
            details = soup.select_one("""[aria-labelledby="nb-toc"] details""")
            if details:
                if not details.select_one("nav"):
                    details.append(toc(soup))
        return soup.prettify(formatter="html5")

    def _preprocess(self, nb, resources):
        nbc = deepcopy(nb)
        resc = deepcopy(resources)

        for preprocessor in self._preprocessors:
            nbc, resc = preprocessor(nbc, resc)

        if self.validate_nb:
            self._validate_preprocessor(nbc, preprocessor)

        return nbc, resc


class SectionExporter(A11yExporter):
    template_file = Unicode("a11y/section.html.j2").tag(config=True)


class ListExporter(A11yExporter):
    template_file = Unicode("a11y/list.html.j2").tag(config=True)


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
    """Exporter markdown as html"""
    return get_markdown_renderer().render("".join(md), **kwargs)


def highlight(code, lang="python", attrs=None, experimental=True):
    """Highlight code blocks"""
    import html

    import pygments

    if lang == "code":
        lang = "python"
    elif lang == "raw":
        return ""

    lang = lang or pygments.lexers.get_lexer_by_name(lang or "python")

    formatter = pygments.formatters.get_formatter_by_name(
        "html", debug_token_types=False, title=f"{lang} code", wrapcode=True
    )
    try:
        return pygments.highlight(
            code, pygments.lexers.get_lexer_by_name(lang or "python"), formatter
        )
    except BaseException as e:
        print(code, e)

    return f"""<pre><code>{html.escape(code)}</code></pre>"""


def soupify(body: str) -> BeautifulSoup:
    """Convert a string of html to an beautiful soup object."""
    return BeautifulSoup(body, features="html5lib")


def toc(html):
    """Create a table of contents in markdown that will be converted to html"""

    toc = BeautifulSoup(features="html.parser")
    toc.append(nav := toc.new_tag("nav"))
    nav.append(ol := toc.new_tag("ol"))
    last_level = 1
    headers = set()
    for header in html.select(".cell :is(h1,h2,h3,h4,h5,h6)"):
        if header in headers:
            continue
        headers.add(header)
        id = header.attrs.get("id")
        if not id:
            continue
        # there is missing logistics for managely role=heading
        # adding code group semantics will motivate this addition
        level = int(header.name[-1])
        if last_level > level:
            for l in range(level, last_level):
                last_level -= 1
                ol = ol.parent.parent
        elif last_level < level:
            for l in range(last_level, level):
                last_level += 1
                ol.append(li := toc.new_tag("li"))
                li.append(ol := toc.new_tag("ol"))
        ol.append(li := toc.new_tag("li"))
        li.append(a := toc.new_tag("a"))
        pilcrow = header.select_one(".pilcrow")
        text = header.text
        if pilcrow:
            text = text.rstrip(pilcrow.text)
        a.append(text)
        a.attrs.update(href=f"#{id}")
    return toc


def heading_links(html):
    """Convert headings into links"""
    for header in html.select(".cell :is(h1,h2,h3,h4,h5,h6):not([role])"):
        id = header.attrs.get("id")
        if not id:
            from slugify import slugify

            if header.text:
                id = slugify(header.text)
            else:
                continue

        
        a = html.new_tag("a")
        a.attrs["href"] = F"#{id}"
        a.extend(header.children)
        header.clear()
        header.attrs.update(id=id)
        header.append(a)


# * navigate links
# * navigate headers
# * navigate table
# * navigate landmarks


def count_cell_loc(cell):
    lines = 0
    for line in StringIO("".join(cell.source)):
        if not line:
            continue
        if line.strip():
            lines += 1
    return lines


def count_loc(nb):
    """Count total significant lines of code in the document"""
    return sum(map(count_cell_loc, nb.cells))


def count_outputs(nb):
    """Count total number of cell outputs"""
    return sum(map(len, (x.get("outputs", "") for x in nb.cells)))


def count_code_cells(nb):
    """Count total number of code cells"""
    return len([None for x in nb.cells if x["cell_type"] == "code"])


def is_ordered(nb) -> str:
    """Measure if the notebook is ordered"""
    start = 0
    for cell in nb.cells:
        if cell["cell_type"] == "code":
            if not count_cell_loc(cell):
                continue
            start += 1
            if start != cell["execution_count"] and start:
                return "executed out of order"
    if start:
        return "executed in order"
    return "unexecuted"
