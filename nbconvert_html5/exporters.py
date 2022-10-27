import os
import os.path
from pathlib import Path
from traitlets import default, List, Callable, CUnicode
from traitlets.config import Config
from nbconvert.exporters.html import HTMLExporter

DIR = Path(__file__).parent


class Html5(HTMLExporter):
    """an embellished HTMLExporter that allows modifications of exporting and the exported.
    
the `nbconvert` exporter has a lot machinery for converting notebook data into strings.
this class introduces a `post_process` trait that allows modifications after creating html content.
this method allows tools like `html.parser` and `bs4.BeautifulSoup` to make modifications at the end.

changes to the template and exporter machinery are foundational changes that take time.
post modifications make it possible to quick changes in manual testing scenarios or configure
A/B testing with out requiring `nbconvert` or notebook knowleldge.
"""
    export_from_notebook = "html5"
    extra_template_paths = List([(DIR / "templates").absolute().__str__()])
    post_process = Callable(lambda x, **kw: x).tag(config=True)
    code_cell_title = CUnicode("Code Cell").tag(config=True)
    markdown_cell_title = CUnicode("Markdown Cell").tag(config=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args **kwargs)
        self.environment.globals["code_title"] = self.code_cell_title
        self.environment.globals["markdown_title"] = self.markdown_cell_title

    def from_notebook_node(self, nb, **kw):
        result, meta = super().from_notebook_node(nb, **kw)
        result = self.post_process(result, **kw)
        return result, meta

    def _template_file_default(self):
        return 'html5-lab.j2'





