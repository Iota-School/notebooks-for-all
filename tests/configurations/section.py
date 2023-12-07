"""an accessible nbconvert template"""

c.NbConvertApp.export_format = "a11y-landmark"
c.A11yExporter.include_settings = True
c.A11yExporter.wcag_priority = "AA"