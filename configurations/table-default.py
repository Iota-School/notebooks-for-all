"""export notebooks as  table of forms"""

c.CSSHTMLHeaderPreprocessor.style = "github-light-colorblind"
c.NbConvertApp.export_format = "html5"
c.CSSHTMLHeaderPreprocessor.style = "default"
c.TemplateExporter.template_file = "semantic-forms/table.html.j2"