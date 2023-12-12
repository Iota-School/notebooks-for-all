"""an accessible nbconvert template"""

c.NbConvertApp.export_format = "a11y"
c.A11yExporter.include_axe = True
c.A11yExporter.include_sa11y = True
c.A11yExporter.include_settings = True
c.A11yExporter.include_help = True
c.A11yExporter.include_visibility = True
c.A11yExporter.include_upload = True
c.A11yExporter.wcag_priority = "AAA"