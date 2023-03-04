# hooks for the mkdocs documentation

from os import system, environ
def on_pre_build(config):
    if environ.get("CI"):
        system("cd .. & python -m doit -n2 copy convert audit report")