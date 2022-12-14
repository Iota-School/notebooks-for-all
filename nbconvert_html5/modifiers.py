from functools import partial, wraps
from subprocess import call
from bs4 import BeautifulSoup, Tag
from .selectors import MAIN, CODE, MD, OUT, PROMPT

Soup = partial(BeautifulSoup, features="html.parser")
from re import compile

PROMPT_RE = compile("(In|Out)(\s|&nbsp;){0,1}\[(?P<n>[0-9]+)\]")


def soup(callable):
    @wraps(callable)
    def soupify(object, **kwargs):
        if not isinstance(object, (BeautifulSoup, Tag)):
            object = Soup(object)

        callable(object)
        return object

    return soupify


@soup
def set_notebook(soup, **kwargs):
    set_main(soup)
    set_cells(soup)
    set_prompts(soup)


@soup
def set_main(soup):
    e = soup.select_one(MAIN)
    e.attrs.pop("tabindex", None)
    e.name = "main"


@soup
def set_tabindex(soup):
    soup.attrs["tabindex"] = 0


@soup
def set_cells(soup):
    for element in soup.select(CODE):
        set_code_cell(element)
        set_tabindex(element)

    for element in soup.select(MD):
        set_md_cell(element)
        set_tabindex(element)


@soup
def set_code_cell(element):
    element.name = "article"
    set_displays(element)
    prompt = element.select_one(PROMPT)
    m = PROMPT_RE.match(prompt.text)
    if m:
        set_cell_label(element, f"code input {m.group('n')}")
    else:
        set_cell_label(element, "code")
    return element


def set_cell_label(cell, label="cell"):
    heading = cell.select_one("h1,h2,h3,h4,h5,h6")
    key = "label"
    if heading:
        if "id" in heading.attrs:
            cell.attrs["aria-labelledby"] = heading.attrs["id"]
            return
    cell.attrs["aria-label"] = label


@soup
def set_md_cell(element):
    element.name = "article"
    set_cell_label(element, "markdown")
    return element


@soup
def set_displays(element):
    out = element.select_one(OUT)
    if out:
        out.name = "section"
        prompt = out.select_one(PROMPT)
        if prompt:
            m = PROMPT_RE.match(prompt.text)
            if m:
                out.attrs["aria-label"] = f"display {m.group('n')}"
                set_tabindex(out)
            else:
                out.attrs["aria-label"] = f"display"

        # there are different kinds of displays and there is going to take work
    # currently there is an ask for better errors/warnings and they share scoope


@soup
def set_prompts(soup):
    for prompt in soup.select(PROMPT):
        prompt.name = "aside"
