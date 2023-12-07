"""configuration with a high contrast theme for the code editor [jupyterlab-pygments](https://pypi.org/project/jupyterlab-pygments/)"""

c.NbConvertApp.export_format = "html5_test"
c.CSSHTMLHeaderPreprocessor.style = "a11y-high-contrast-light"
c.Html5.notebook_is_main = True # transform notebook div to main
c.Html5.notebook_code_cell_is_article = True # transform code cell div to article
c.Html5.notebook_md_cell_is_article = True # transform mardown cell div to article
c.Html5.cell_output_is_section = True # transform output div to section
c.Html5.tab_to_code_cell = True # add tabindex to code cells for navigation
c.Html5.tab_to_md_cell = False # add tabindex to md cells for navigation
c.Html5.tab_to_code_cell_display = False # add tabindex to cell displays for navigation
c.Html5.code_cell_label = True # add aria-label to code cells
c.Html5.md_cell_label = False # add aria-label to md cell
c.Html5.cell_display_label = False # add aria-label to cell
c.Html5.cell_contenteditable = False # make cell code inputs contenteditable
c.Html5.cell_contenteditable_label = False # aria-label on contenteditable cells
c.Html5.prompt_is_label = True   # add the cell input number to the aria label
c.Html5.cell_describedby_heading = False # set aria-describedby when heading found in markdown cell
c.Html5.increase_prompt_visibility = True # decrease prompt transparency for better color contrast
c.Html5.cell_focus_style = "outline: 1px dashed;" # the focus style to apply to tabble cells.
c.Html5.h_is_link = True # headings get anchors so they may be tabbed to.