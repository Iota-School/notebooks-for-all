import os
import os.path
from pathlib import Path
from traitlets import default, List
from traitlets.config import Config
from nbconvert.exporters.html import HTMLExporter

DIR = Path(__file__).parent

class Html5(HTMLExporter):
    export_from_notebook = "html5"
    extra_template_paths = List([(DIR / "templates").absolute().__str__()])


    def _file_extension_default(self):
        """
        Set the file extension of the exported notebook to .html5.
        """
        return '.html5'


    @property
    def template_paths(self):
        """
        We want to inherit from HTML template, and have template under
        ``./templates/`` so append it to the search path. (see next section)

        Note: nbconvert 6.0 changed ``template_path`` to ``template_paths``
        """


        return super()._template_paths() + [os.path.join(os.path.dirname(__file__), "templates")]
    

    def _template_file_default(self):
        """
        We want to use the new template we ship with our library.
        """
        return 'test_template.j2'





