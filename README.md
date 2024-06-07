# `nbconvert-a11y`

`nbconvert-a11y` contains templates for accessible notebook representations and accessibility tests for Jupyter notebook products.

```bash
pip install nbconvert-a11y
```

`nbconvert-a11y` can be used with the [`nbconvert` command line tool](https://nbconvert.readthedocs.io/en/latest/usage.html).
it provides the `a11y` exporter with several variants that can be used. the default theme uses a flexible table representation

```bash
jupyter nbconvert --to a11y Untitled.ipynb           # flexible table navigation
jupyter nbconvert --to a11y-table Untitled.ipynb     # a11y is an alias for a11y-table
jupyter nbconvert --to a11y-landmark Untitled.ipynb  # cells are section landmarks
jupyter nbconvert --to a11y-list Untitled.ipynb      # cells are list items
```

```python
from nbconvert_a11y.exporter import A11y, Table, Section, List
```

A an example of the canonical Lorenz differential differential equations can be viewed @ https://deathbeds.github.io/nbconvert-a11y/exports/html/lorenz-executed-a11y.html

## History

the `nbconvert-a11y` project is forked from initial development in the [`notebook-for-all`]() repository. 
this collaboration between [Space Telescope Science Institute](https://www.stsci.edu/), [Iota School](https://iotaschool.com/) and [Quansight Labs](https://www.quansight.com/labs)
brought input from blind and visual impaired notebook users as to what their most assistive experiences could be.

## License
Licensed under a [3-Clause BSD license](LICENSE).
