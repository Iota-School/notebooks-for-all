# Notebook authoring accessibility checklist

How usable Jupyter notebooks are for disabled people can vary greatly depending on how they are set up and presented. Writing notebook content more accessibly is a great place for notebook authors to start making changes now!

Use this checklist to review notebooks and as a prompt to ask more questions about how a notebook's content can be accessed.

This checklist is based on the [draft authoring tips from the Notebooks For All team](accessibility-tips-for-jupyter-notebooks.md).

**By the Notebooks for All team** - Erik Tollerud, Isabela Presedo-Floyd, Jenn Kotler, Patrick Smyth, Tony Fast

Published February 28, 2023

**Table of contents**
1. Organization
2. Images
    1. Visualizations
3. Text
4. Code
5. Other content
    1. Videos
    2. Sonifications
    3. Interactive Widgets
6. Related Resources

## Organization

At the beginning, a notebook has

- [ ] A title in the form of a H1 (`#` in Markdown).
- [ ] A brief summary of the notebook.
- [ ] A table of contents in an ordered list (`1., 2.,` etc. in Markdown).
- [ ] The author(s) and affiliation(s) (if relevant).
- [ ] The date first published.
- [ ] The date last edited (if relevant).
- [ ] A link to the notebook's source(s) (if relevant).

Throughout the notebook

- [ ] There is only one H1 (`#` in Markdown) used in the notebook.
- [ ] The notebook uses other heading tags in order (meaning it does not skip numbers).

## Images

- [ ] All images (jpg, png, svgs) have an image description. This could be
    - [ ] Alt text (an `alt` attribute) 
    - [ ] Empty alt text for decorative images/images meant to be skipped (an `alt` attribute with no value) or
    - [ ] Captions or
    - [ ] If no other options will work, the image is decribed in surrounding paragraphs.

- [ ] Any text present in images exists in a text form outside of the image (this can be alt text, captions, or surrounding text.)

### Visualizations

- [ ] All visualizations have an image description. Review the previous section, Images, for more information on how to add it.
- [ ] Visualization descriptions include
    - [ ]  The type of visualization (like bar chart, scatter plot, etc.)
    - [ ] Title
    - [ ] Axis labels and range
    - [ ] Key or legend
    - [ ] An explanation of the visualization's significance to the notebook (like the trend, an outlier in the data, what the author learned from it, etc.)

- [ ] All visualizations have the following labels
    - [ ] Title
    - [ ] Labels on all axes
    - [ ] Key or legend (if relevant)

- [ ] All visualizations and their parts have enough color contrast to be legible. Remember that transparent colors have lower contrast than their opaque versions.
- [ ] All visualizations convey information with more than color-coding. Color may also be mixed with text labels, patterns, or icons to fulfill this.
- [ ] All visualizations have an additional way for notebook readers to access the information. Linking to the original data, including a table of the data in the same notebook, or sonifying the plot are all options.

## Text

- [ ] All link text is descriptive. It tells users where they will be taken if they open the link.
- [ ] Use plain language wherever possible.
- [ ] All acronyms are defined at least the first time they are used. 
- [ ] Field-specific/specialized terms are used when needed, but not excessively.
- [ ] Text is broken into paragraphs and/or cells where relevant.
- [ ] Text is in complete sentences where relevant.

## Code

- [ ] Code sections are introduced/explained before they appear in the notebook. This could be a heading in a prior Markdown cell, a sentence preceding it, or a code comment in the code section.
- [ ] Code has explanatory comments (if relevant). This is most important for long sections of code.
- [ ] If the author has control over the syntax highlighting theme in the notebook, that theme has enough color contrast to be legible.
- [ ] Code and code explanations focus on one task at a time. Unless comparison is the point of the notebook, only one way to complete the task is described at a time.

## Other content

This list is not exhaustive. If you are reviewing a notebook with content that you do not think fits any of these categories, keep in mind

- Text is flexible. Whether it is in the document or linked out, text can be read visually, be read audibly, be magnified, or be translated to another language. Having a text alternative is a good back up plan.
- Having enough color contrast is required on almost all visual content.

### Videos

- [ ] All videos have titles in the player or in the text before them.
- [ ] All videos have captions/subtitles. This can include visual information descriptions if relevant.
- [ ] All videos have transcripts. This can include visual information descriptions if relevant.
- [ ] All video players have buttons with labels. This can be a persistent label or appear when hovered.
- [ ] All video players have buttons with enough color contrast.
- [ ] No videos have flashing images at more than three frames per second.

### Sonifications

- [ ] All audio players have buttons with labels. This can be a persistent label or appear when hovered.
- [ ] All audio players have buttons with enough color contrast.

### Interactive Widgets 

The accessibility of interactive widgets varies greatly depending how they are included in the notebook. Review beyond this checklist may be needed.

- [ ] All interactive widgets with visual controls have labels. This can be a persistent label or appear when hovered.
- [ ]  All interactive widgets with visual controls have enough color contrast.
- [ ] All interactive widgets have a summary of what they are and what they do in a surrounding text area.
- [ ] If an interactive widget's contents are needed to understand the rest of the notebook, the widget either needs to be tested further or have that content fully represented not as a widget elsewhere in the notebook.

---

## Related resources

