c.NbConvertApp.export_format = "html5"

from bs4 import BeautifulSoup

ASIDE = ".jp-InputArea-prompt, .prompt, .jp-OutputArea-prompt"

def asides(object, resources):
    soup = BeautifulSoup(object, features="html")
    for node in soup.select(ASIDE):
        node.name = "aside"
    return str(soup)
    
c.TemplateExporter.post_process = asides