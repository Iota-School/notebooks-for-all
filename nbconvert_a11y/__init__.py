"""nbconvert_soup organically added tooling to the nbconvert library.

nbconvert is a community convention for converting ipynb files to
other formats like html, pdf, epub, tex. the goal of this work is to
test accessibility remediations made to the html version of notebooks.
nbconvert suits our needs, and  it is well integrated into the jupyter command line for reuse.

we found that nbconvert's configuration system was valuable for recording
the state of manual testing sessions.

we called this library `nbconvert_a11y` because we hope discover html5 patterns
that offer a POUR notebook reading experience for assistive tech.
"""
