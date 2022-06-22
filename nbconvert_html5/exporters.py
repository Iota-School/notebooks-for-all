from pathlib import Path
from traitlets import default, List
from traitlets.config import Config
from nbconvert.exporters.html import HTMLExporter

DIR = Path(__file__).parent

class Html5(HTMLExporter):
    export_from_notebook = "html5"
    extra_template_paths = List([(DIR / "templates").absolute().__str__()])