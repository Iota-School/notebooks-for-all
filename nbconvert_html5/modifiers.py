from functools import partial, wraps
from subprocess import call
from bs4 import BeautifulSoup, Tag
from .selectors import MAIN, CODE, MD, OUT, PROMPT

Soup = partial(BeautifulSoup, features="html.parser")


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
def set_cells(soup):
    for element in soup.select(CODE):
        set_code_cell(element)

    for element in soup.select(MD):
        set_md_cell(element)

@soup
def set_code_cell(element):
    element.name = "article"
    set_displays(element)
    return element

@soup
def set_md_cell(element):
    element.name = "article"
    return element


@soup
def set_displays(element):
    out = element.select_one(OUT)
    if out:
        out.name = "section"

@soup
def set_prompts(soup):
    for prompt in soup.select(PROMPT):
        prompt.name = "aside"
