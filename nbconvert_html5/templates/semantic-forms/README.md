# the `html5` template

an `nbconvert` template designed for an accessible experience when rendering notebooks as html webpages. more generally, it could serve as an accessible substrate to build computational literature with like documentation, research papers, or blog posts.

`jupyter nbconvert --to html5` features:

- [x] semantic html tags, roles, and aria for the notebook and its cells
- [x] efficient tab navigation including:
  - [x] skips links
  - [x] heading links with large hit areas
  - [x] cell source as `readonly` forms that take tab focus
  - [x] any other rich interactive content in the `output`
- [x] uses Atkinson Hyperlegible which is <q cite="https://fonts.google.com/specimen/Atkinson+Hyperlegible/about">specifically to increase legibility for readers with low vision, and to improve comprehension.</q> 
- [x] uses the `github-light-colorblind` `pygments code theme from the [accessible-pygments](https://github.com/Quansight-Labs/accessible-pygments) project based on [`a11y-syntax-highlighting`](https://github.com/ericwbailey/a11y-syntax-highlighting)
- [x] screen reader landmarks, headings (markdown & outputs), forms (cell inputs), and table navigation
- [x] operable when zoomed in
- [x] table of contents for code and narrative navigation
- [ ] configurable accessibility settings
  - [ ] persistent settings across sessions
- [ ] best practice auditting during conversion
- [ ] automated remediations
  - [ ] fix rendered pandas tables

### template scope

the template defines the majority of the web page from the `html` tag to the cell outputs. every element is defined using a meaningful tag or aria role. the cell outputs come from user land and our template can't control their content. if author's abide some [best practices]() then they can ensure an accessible experience when their notebook is exported to html.

### POUR-CAF principles

notebooks often harness data visualizations. their mission co-develops with accessible visualizations. this project goals beyond the standard <abbr title="web content accessibility guidelies">[WCAG]</abbr> <abbr title="percievable operable understable robust">POUR</abbr> principles and adds [Chartability]'s <abbr title="compromising assistive flexible">[CAF]</abbr> principles and heuristics to the design.

## a table of cells

this template represents a notebook as a html table where each notebook cell is a row in the html. the table pattern is a natural html pattern and adds a new dimension to screen readers navigating notebook documents.

## table of contents navigation

notebook documents can be long and navigating them need to be easier.

* <kbd>Esc</kbd> - minimizes the table of contents
* <kbd>Ctrl + Esc</kbd> - toggles the table of contents

## conclusion

the html version of notebooks is not the same interactive state as the editting experience, but it is still a highly interactive experience. overall, focusing on an accessible substrate to build sites from has improved the experience from abled and disabled people.

[Chartability]: https://chartability.fizz.studio/ "heuristics and principles for accessible data systems"
[WCAG]: https://en.wikipedia.org/wiki/Web_Content_Accessibility_Guidelines 
[CAF]: https://github.com/Chartability/POUR-CAF