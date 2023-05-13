"""export notebooks as an unordered list of forms"""

c.CSSHTMLHeaderPreprocessor.style = "github-light-colorblind"
c.NbConvertApp.export_format = "html5"
c.CSSHTMLHeaderPreprocessor.style = "default"
c.TemplateExporter.template_file = "semantic-forms/ul.html.j2"