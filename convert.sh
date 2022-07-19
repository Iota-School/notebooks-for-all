#!/bin/bash

pip install .

# --template test_template

jupyter nbconvert --to html5 -TemplateExporter.extra_template_basedirs=/home/patrick/projects/notebooks-for-all/nbconvert_html5/templates tests/test_nbconvert_html5.ipynb 
