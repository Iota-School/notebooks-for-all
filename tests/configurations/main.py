"""export notebooks as a main region with cell landmarks"""

c.CSSHTMLHeaderPreprocessor.style = "github-light-colorblind"
c.NbConvertApp.export_format = "html5"
c.CSSHTMLHeaderPreprocessor.style = "default"
c.TemplateExporter.template_file = "semantic-forms/main.html.j2"