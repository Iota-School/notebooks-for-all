from numpy import ndarray
import pandas, bs4, functools
from .outputs import get_type, repr_html, repr_semantic, repr_semantic_update


def load_ipython_extension(shell):
    repr_semantic_update()


def get_caption(df, ROW_INDEX=True, COL_INDEX=True):
    dl = new("dl", role="presentation")
    dl.append(new("dt", "rows")), dl.append(new("dd", str(len(df))))
    dl.append(new("dt", "columns")), dl.append(new("dd", str(len(df.columns))))
    dl.append(new("dt", "indexes")), dl.append(new("dd", indexes := new("dl", role="presentation")))
    indexes.append(new("dt", "rows")), indexes.append(new("dd", str(df.index.nlevels * ROW_INDEX)))
    indexes.append(new("dt", "columns")), indexes.append(
        new("dd", str(df.columns.nlevels * COL_INDEX))
    )
    return dl


def row_major_at_rows(df, COL_INDEX=True):
    return df.columns.nlevels * COL_INDEX + len(df)


def row_major_at_cols(df, ROW_INDEX=True):
    return df.index.nlevels * ROW_INDEX + int(any(df.columns.names)) + len(df.columns)


@repr_semantic.register(pandas.DataFrame)
@repr_semantic.register(ndarray)
def get_table(df, caption=None, ARIA=True, ROW_INDEX=True, COL_INDEX=True, SEMANTIC=True):
    soup = bs4.BeautifulSoup(features="lxml")
    WIDE = (df.shape[1] + 1) > pandas.options.display.max_columns
    LONG = (df.shape[0] + 1) > pandas.options.display.max_rows
    soup.append(
        table := new(
            "table",
            itemscope=None,
            itemtype=get_type(df),
        )
    )
    if isinstance(df, ndarray):
        ROW_INDEX = COL_INDEX = False
        df = pandas.DataFrame(df)

    table.attrs.update(
        colcount=row_major_at_cols(df, ROW_INDEX) if ARIA or WIDE else None,
        rowcount=row_major_at_rows(df, COL_INDEX) if ARIA or LONG else None,
    )
    col_ranges, row_ranges = get_ranges(df, WIDE, LONG)
    table.append(cap := new("caption", caption))
    if caption is None:
        cap.attrs["class"] = "nv"
    cap.append(get_caption(df, ROW_INDEX, COL_INDEX))
    if COL_INDEX:
        get_thead(df, table, col_ranges, WIDE, ARIA, LONG, ROW_INDEX)
    get_tbody(df, table, col_ranges, row_ranges, WIDE, ARIA, LONG, ROW_INDEX, COL_INDEX, SEMANTIC)
    return soup


def get_thead(df, table, col_ranges, WIDE=False, ARIA=False, LONG=False, ROW_INDEX=True):
    ROWS, COLS = any(df.index.names), any(df.columns.names)
    col_center = col_ranges[1].start - col_ranges[0].stop
    for col_level, col_name in enumerate(df.columns.names):
        table.append(tr := trow(rowindex=col_level + 1 if ARIA or LONG else None))
        if ROW_INDEX:
            if not col_level:
                # on the first pass write column or index names
                if ROWS or not COLS:
                    for row_level, row_name in enumerate(df.index.names):
                        tr.append(
                            th := theading(
                                str(
                                    row_name
                                    or ("index" if df.index.nlevels == 1 else f"index {row_level}")
                                ),
                                scope="col",
                                rowspan=df.columns.nlevels if df.columns.nlevels > 1 else None,
                                colindex=row_level + 1 if ARIA else None,
                            )
                        )
            if COLS:
                tr.append(
                    theading(
                        str(col_name or ("column" if len(df.index) == 1 else f"index {col_level}")),
                        scope="row",
                        colindex=df.index.nlevels + 1 if ARIA else None,
                    )
                )

        for col_part, col_range in enumerate(col_ranges):
            if col_part and col_range:
                tr.append(
                    theading(
                        HIDDEN,
                        colindex=(
                            col_index + 2 + df.index.nlevels + bool(LONG and WIDE) if ARIA else None
                        ),
                        **{"aria-colspan": col_center},
                    )
                )
            for col_index in col_range:
                col_value = df.columns.get_level_values(col_level)[col_index]
                tr.append(
                    theading(
                        str(col_value),
                        scope="col",
                        colindex=(
                            df.index.nlevels + int(ROWS and COLS) + col_index + 1
                            if ARIA or WIDE and col_part
                            else None
                        ),
                    )
                )


def get_tbody(
    df,
    table,
    col_ranges,
    row_ranges,
    WIDE=False,
    ARIA=False,
    LONG=False,
    ROW_INDEX=True,
    COL_INDEX=True,
    SEMANTIC=False,
):
    ROWS, COLS = any(df.index.names), any(df.columns.names)
    row_center = row_ranges[1].start - row_ranges[0].stop
    col_center = col_ranges[1].start - col_ranges[0].stop
    for row_part, row_range in enumerate(row_ranges):
        if row_part and row_range:
            # handle hidden data in between dataframe regions
            table.append(
                tr := trow(
                    rowindex=row_index + 2 + df.columns.nlevels * COL_INDEX,
                    **{"aria-rowspan": row_center},
                )
            )
            if ROW_INDEX:
                # shw the row headers
                for row_level in range(df.index.nlevels):
                    tr.append(theading(HIDDEN, colindex=row_level + 1))
                if ROWS and COLS:
                    tr.append(tdata(EMPTY, colindex=row_level + 2))
            else:
                row_level = 0

            for col_part, col_range in enumerate(col_ranges):
                # write the column values
                if col_part and col_range:
                    # write the hidden columns
                    tr.append(
                        tdata(
                            HIDDEN,
                            colindex=col_index
                            + 2
                            + df.index.nlevels * ROW_INDEX
                            + int(ROWS and COLS),
                            **{"aria-rowspan": row_center, "aria-colspan": col_center},
                        ),
                    )
                for col_index in col_range:
                    # write the column values
                    tr.append(
                        tdata(
                            HIDDEN,
                            colindex=col_index
                            + 1
                            + df.index.nlevels * ROW_INDEX
                            + int(ROWS and COLS),
                        )
                    )
        for row_index in row_range:
            table.append(tr := trow(rowindex=row_index + 1 + df.columns.nlevels * COL_INDEX))
            if ROW_INDEX:
                for row_level in range(df.index.nlevels):
                    tr.append(
                        theading(
                            str(df.index.get_level_values(row_level)[row_index]),
                            colindex=row_level + 1 if ARIA else None,
                            scope="row",
                        )
                    )
                if ROWS and COLS:
                    tr.append(tdata(EMPTY, colindex=row_level + 2))
            for col_part, col_range in enumerate(col_ranges):
                if col_part and col_range:
                    tr.append(
                        tdata(
                            HIDDEN,
                            colindex=col_index
                            + 2
                            + df.index.nlevels * ROW_INDEX
                            + int(ROWS and COLS),
                            **{"aria-colspan": col_center},
                        )
                    )
                for col_index in col_range:
                    tr.append(
                        tdata(
                            (SEMANTIC and repr_html or str)(df.iloc[row_index, col_index]),
                            colindex=col_index
                            + 1
                            + df.index.nlevels * ROW_INDEX
                            + int(ROWS and COLS),
                        )
                    )


def get_frame_bounds(df, WIDE=False, LONG=False):
    a, b, c, d = len(df.columns), len(df.columns), len(df), len(df)
    if WIDE:
        a = pandas.options.display.max_columns // 2
        b -= a
    if LONG:
        c = pandas.options.display.max_rows // 2
        d -= c
    return a, b, c, d


def get_ranges(df, WIDE=False, LONG=False):
    a, b, c, d = get_frame_bounds(df, WIDE=WIDE, LONG=LONG)
    return (range(a), range(b, df.shape[1])), (range(c), range(d, df.shape[0]))


def new(
    tag,
    string=None,
    rowindex=None,
    colindex=None,
    rowcount=None,
    colcount=None,
    rowspan=None,
    colspan=None,
    scope=None,
    *,
    soup=bs4.BeautifulSoup(features="lxml"),
    **attrs,
):
    """create a new beautiful soup with table and aria properties"""
    data = locals()
    attrs.update(
        {
            f"aria-{k}": data.get(k)
            for k in ["rowindex", "colindex", "rowcount", "colcount"]
            if data.get(k)
        }
    )
    attrs.update({k: data.get(k) for k in ["rowspan", "colspan", "scope"] if data.get(k)})
    tag = soup.new_tag(tag, attrs=attrs)
    if string:
        tag.append(string)
    return tag


trow = functools.partial(new, "tr")
theading = functools.partial(new, "th")
tdata = functools.partial(new, "td")

HIDDEN, EMPTY = "hidden", "empty"
