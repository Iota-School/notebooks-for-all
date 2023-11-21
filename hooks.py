# hooks for the mkdocs documentation

from os import environ


def on_pre_build(config):
    if environ.get("CI"):
        pass  # system("cd .. & python -m doit -n2 copy convert audit report")
