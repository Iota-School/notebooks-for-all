from pathlib import Path

from traitlets.config import Config
from nbconvert.exporters.html import HTMLExporter

DIR = Path(__file__).parent

class MyExporter(HTMLExporter):
    export_from_notebook = "html5"

    @property
    def template_paths(self):
        """
        We want to inherit from HTML template, and have template under
        ``./templates/`` so append it to the search path. (see next section)

        Note: nbconvert 6.0 changed ``template_path`` to ``template_paths``
        """
        return super().template_paths + (DIR / "templates").iterdir()

    def _template_file_default(self):
        """
        We want to use the new template we ship with our library.
        """
        return 'html' # full
