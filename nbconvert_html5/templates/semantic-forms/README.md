when we are designing for screen reader, or the colorless experience.
we must program for a machine so it treats the human kindly;
our primary effort is teach the machine to be nice.
through this effort we can use rdfa to improve the context.
https://www.w3.org/TR/rdfa-lite/

# the semantic forms template

this template is designed is optimize the [screen reader] experience of static jupyter notebooks.
it describes the notebook format in semantic html that extend natural affordances to the screen reader.


* it extends what nbconver already does


<q>a screen reader is not a browser</q>

## notebook cell are table cells

## browse mode elements navigation

### landmark navigation

### table navigation

navigate to the first table, which is the notebook. then it is possible skip through cells with arrow keys.

### form navigation

in this template, we design the semantic so that they may mature into an interactive state.
so we interpret static code cells and interactive widgets in the document.
they

### other navigation

this work defines the outer semantic representation of a notebook.
the notebook's content varies from document to document.
author's can include other forms a structural navigation markers like headings, links, lists, graphics in markdown cells and code cell outputs.



[screen reader]: https://dequeuniversity.com/screenreaders/
[orca]: https://dequeuniversity.com/screenreaders/