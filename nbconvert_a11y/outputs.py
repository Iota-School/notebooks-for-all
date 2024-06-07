"""semantic html representations for common python values.
requires complementary css to be included."""

from gc import get_referrers
from pathlib import Path
import bs4
from types import FunctionType, ModuleType
import functools
import bs4
import json
from IPython import get_ipython
from numpy import float_, int_

HERE = Path(__file__).parent
CSS = HERE / "outputs.css"
BeautifulSoup = functools.partial(bs4.BeautifulSoup, features="lxml")


def new(tag, *children, soup=BeautifulSoup(), **attrs):
    """create a new beautiful soup tag"""
    element = soup.new_tag(tag, attrs=attrs)
    element.extend(children)
    return element


def _recursion(value):
    """handling of recursive values"""
    return new("a", repr_default(value), href=f"#{id(value)}")


def load_ipython_extension(shell):
    from IPython.display import display

    # shell.display_formatter.formatters["text/html"].for_type(bs4.Tag, bs4.Tag.prettify)
    # shell.display_formatter.formatters["text/html"].for_type(
    #     bs4.BeautifulSoup, bs4.BeautifulSoup.prettify
    # )
    repr_semantic_update(shell)
    display({"text/html": f"<style>{CSS.read_text()}</style>"}, raw=True)


def _prettify(func):
    def wrapped(*args, **kwargs):
        return str(func(*args, **kwargs))

    return wrapped


def repr_semantic_update(shell=None):
    # this dispatches on the type of the value, including value types.
    # the mimebundle and ipython display are hit first then the display formatters.
    # which these formatters installed we'll never hit the text/plain formatter
    # and every display will be included in the output.

    (shell or get_ipython()).display_formatter.formatters["text/html"].type_printers.update(
        {k: _prettify(v) for k, v in repr_semantic.registry.items() if k is not object}
    )


def get_type(value):
    "construct a URI or URN for the type"
    return get_id(type(value))


def get_id(value):
    "construct a URI or URN for the value"
    if isinstance(value, ModuleType):
        return value.__name__
    elif isinstance(value, (FunctionType, type)):
        return f"{value.__module__}:{value.__qualname__}"
    return str(id(value))


def get_from_garbage(object):
    get_referrers(object)


def repr_html(value, caption=None):
    html = repr_semantic(value)
    if caption is not None:
        figure = new("figure", html)
        figure.append(new("figcaption", caption))
        return figure
    return html


def get_markdown(value):
    import mistune

    return mistune.markdown(value)


def repr_default(value, **attrs):
    return new(
        "samp",
        new("kbd", object.__repr__(value), itemscope=None, itemtype=get_type(value), **attrs),
    )


@functools.singledispatch
def repr_semantic(value, level=0, maxlevels=6, context=None):
    """default representation"""
    from IPython.display import display

    if f := getattr(value, "_repr_markdown_", None):
        return BeautifulSoup(f(value))
    if f := getattr(value, "_repr_html_", None):
        return BeautifulSoup(f(value))
    return repr_default(value)


@repr_semantic.register(str)
def repr_string(value, level=0, maxlevels=6, context=None):
    pre, sep, rest = value.partition(":")
    if rest.startswith(("//",)):
        if pre in {"file", "http", "https"}:
            return new("a", value, href=value)
    elif pre in {"data"}:
        "handle data uri"
    return new(
        "samp", value, itemscope=None, itemtype=get_type(value), **{"class": "s2"}
    )  # s1 is single quote


@repr_semantic.register(bool)
@repr_semantic.register(type(None))
def repr_const(value, level=0, maxlevels=6, context=None):
    return new("data", str(value), value=json.dumps(value), **{"class": "kc"})


@repr_semantic.register(int)
@repr_semantic.register(int_)
@repr_semantic.register(float_)
@repr_semantic.register(float)
def repr_number(value, level=0, maxlevels=6, context=None):
    return new(
        "data",
        str(value),
        itemscope=None,
        itemtype=get_type(value),
        style=f"--val: {value};",
        **{"class": "m" + "if"[isinstance(value, float)]},
    )


@repr_semantic.register(bytes)
def repr_bytes(value, level=0, maxlevels=6, context=None):
    return new("samp", object.__repr__(value)[2:-1], itemscope=None, itemtype=get_type(value))


@repr_semantic.register(list)
@repr_semantic.register(tuple)
def repr_list(value, level=0, maxlevels=6, context=None, tag="ol"):
    context = set() if context is None else context
    if maxlevels and level >= maxlevels:
        return new("span", "collapsed")
    ID = id(value)
    if ID in context:
        return _recursion(value)
    list = new(tag, id=ID, itemscope=None, itemtype=get_type(value))
    context.add(ID)
    level and list.attrs.update(role="presentation")
    level += 1
    for item in value:
        list.append(new("li", repr_semantic(item, level, maxlevels, context)))
    return list


@repr_semantic.register(set)
def repr_tuple(value, level=0, maxlevels=6, context=None):
    return repr_list(value, level, maxlevels, context, tag="ul")


@repr_semantic.register(dict)
def repr_dict(value, level=0, maxlevels=6, context=None):
    context = set() if context is None else context
    if maxlevels and level >= maxlevels:
        return new("span", "collapsed")
    ID = id(value)
    if ID in context:
        return _recursion(value)
    context.add(ID)
    dl = new("dl", itemscope=None, itemtype=get_type(value), id=get_id(value))
    level and dl.attrs.update(role="presentation")
    level += 1
    for k, v in value.items():
        dl.append(new("dt", repr_semantic(k, level, maxlevels)))
        if id(v) in context:
            dl.append(new("dd", _recursion(v)))
        else:
            dl.append(new("dd", repr_semantic(v)))
    context.remove(ID)
    return dl
