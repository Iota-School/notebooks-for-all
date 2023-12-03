"""an accessible nbconvert template"""

c.NbConvertApp.export_format = "a11y"
c.A11yExporter.template_file = "a11y/section.html.j2"
c.A11yExporter.include_axe = True
c.A11yExporter.wcag_priority = "AAA"