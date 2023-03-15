# Notebook authoring accessibility checklist

Whether a Jupyter notebook is usable for disabled people can vary widely—it depends on how the document is set up and presented. Notebook authors can use writing and publishing techniques to ensure their notebooks' content is more accessible.

Use this checklist to review notebooks and get a better sense of if their content is accessible. Editing your notebook for accessibility is an excellent step you can take to make our communities more inclusive!

This checklist is based on the [draft authoring tips from the Notebooks For All team](accessibility-tips-for-jupyter-notebooks.md).

<details open>
<summary>Table of contents</summary>
<nav>

- [Notebook authoring accessibility checklist](#notebook-authoring-accessibility-checklist)
  - [Structure](#structure)
    - [The First Cell](#the-first-cell)
    - [The Rest of the Cells](#the-rest-of-the-cells)
  - [Text](#text)
  - [Code](#code)
  - [Media](#media)
    - [Images](#images)
    - [Visualizations](#visualizations)
    - [Videos](#videos)
    - [Audio and Sonifications](#audio-and-sonifications)
    - [Interactive Widgets](#interactive-widgets)
  - [Related resources](#related-resources)

</nav>
</details>

<details markdown>
<summary>About this document <i>last updated on <time datetime="2023-03-15">March 15, 2023</time>
</i></summary>

Authors:
* Isabela Presedo-Floyd <a rel="author" href="https://github.com/isabela-pf">@isabela-pf</a>
* Jenn Kotler <a rel="author" href="https://github.com/jenneh">@jenneh</a>
* Patrick Smyth <a rel="author" href="https://github.com/smythp">@smythp</a>
* Tony Fast <a rel="author" href="https://github.com/tonyfast">@tonyfast</a>
* Erik Tollerud <a rel="author" href="https://github.com/eteq">@eteq</a>


Originally published on <time datetime="2023-02-28">February 28, 2023</time>

</details>

## Structure

Author should be aware of [information, structure, and relationships][1.3.1] in their authored works. 

### The First Cell

- [ ] The title of the notebook in a first-level heading (eg. `<h1>` or `# in markdown`).
- [ ] A brief description of the notebook.
- [ ] The date first published.
- [ ] The date last edited (if relevant).
- [ ] A link to the notebook's source(s) (if relevant).
- [ ] The author(s) and affiliation(s) (if relevant).
- [ ] A table of contents in an ordered list (`1., 2.,` etc. in Markdown).<!-- i'd love to discuss this one further. i don't think authors should do this, their documentation or ide tools should. it is easy to screw this up manually.-->

### The Rest of the Cells

- [ ] There is only one H1 (`#` in Markdown) used in the notebook.
- [ ] The notebook uses other heading tags in order (meaning it does not skip numbers). The rendered content should satisfy WCAG [1.3.1].

## Text

- [ ] All link text is descriptive. It tells users where they will be taken if they open the link.
- [ ] Use plain language wherever possible.
- [ ] All acronyms are defined at least the first time they are used. 
- [ ] Field-specific/specialized terms are used when needed, but not excessively.
- [ ] Text is broken into paragraphs and/or cells where relevant.
- [ ] Text is in complete sentences where relevant.

## Code

- [ ] Code sections are introduced and explained before they appear in the notebook. This can be fulfilled with a heading in a prior Markdown cell, a sentence preceding it, or a code comment in the code section.
- [ ] Code has explanatory comments (if relevant). This is most important for long sections of code.
- [ ] If the author has control over the syntax highlighting theme in the notebook, that theme has enough color contrast to be legible.
- [ ] Code and code explanations focus on one task at a time. Unless comparison is the point of the notebook, only one method for completing the task is described at a time.

## Media

This list is not exhaustive. If you are reviewing a notebook with content that you do not think fits any of these categories, keep in mind

- Text is flexible. Whether it is in the document or linked out, text can be read visually, be read audibly, be magnified, or be translated to another language. Having a text alternative is a good back up plan.
- Having enough color contrast is required on almost all visual content.


### Images

- [ ] All images (jpg, png, svgs) have an image description. This could be
    - [ ] Alt text (an `alt` attribute) 
    - [ ] Empty alt text for decorative images/images meant to be skipped (an `alt` attribute with no value)
    - [ ] Captions
    - [ ] If no other options will work, the image is decribed in surrounding paragraphs.

- [ ] Any text present in images exists in a text form outside of the image (this can be alt text, captions, or surrounding text.)

### Visualizations

<details>
<summary>Expand the visualizations checklist</summary>

- [ ] All visualizations have an image description. Review the previous section, Images, for more information on how to add it.
- [ ] Visualization descriptions include
    - [ ] The type of visualization (like bar chart, scatter plot, etc.)
    - [ ] Title
    - [ ] Axis labels and range
    - [ ] Key or legend
    - [ ] An explanation of the visualization's significance to the notebook (like the trend, an outlier in the data, what the author learned from it, etc.)

- [ ] All visualizations have the following labels
    - [ ] Title
    - [ ] Labels on all axes
    - [ ] Key or legend (if relevant)

- [ ] All visualizations and their parts have enough color contrast to be legible. Remember that transparent colors have lower contrast than their opaque versions.
- [ ] All visualizations convey information with more visual cues than color coding. Use text labels, patterns, or icons alongside color to achieve this.
- [ ] All visualizations have an additional way for notebook readers to access the information. Linking to the original data, including a table of the data in the same notebook, or sonifying the plot are all options.

</details>

### Videos

<details>
<summary>Expand the videos checklist</summary>


- [ ] All videos have titles in the player or in the text before them.
- [ ] All videos have captions/subtitles. This can include visual information descriptions if relevant.
- [ ] All videos have transcripts. This can include visual information descriptions if relevant.
- [ ] All video players have buttons with labels. This can be a persistent label or appear when hovered.
- [ ] All video players have buttons with enough color contrast.
- [ ] No videos have flashing images at more than three frames per second.

</details>


### Audio and Sonifications

<details>
<summary>Expand the visualizations checklist</summary>

- [ ] Sonifications include a key explaining the mapping of data to sound. A written description can be used to convey this information.
- [ ] Sonification outputs reference the method that generated the sonification. This can be done in a code cell or with a link to the file used to generate the sonification.
- [ ] Audio players include basic listening controls for starting, pausing, volume, and speed.
- [ ] All audio players have buttons with labels. This can be a persistent label or appear when hovered.
- [ ] All audio players have buttons with enough color contrast.

</details>


### Interactive Widgets 

<details>
<summary>Expand the visualizations checklist</summary>


The accessibility of interactive widgets varies greatly depending how they are included in the notebook. Review beyond this checklist may be needed.

- [ ] All interactive widgets with visual controls have labels. This can be a persistent label or appear when hovered.
- [ ]  All interactive widgets with visual controls have enough color contrast.
- [ ] All interactive widgets have a summary of what they are and what they do in the surrounding text.
- [ ] If an interactive widget's contents are needed to understand the rest of the notebook, the widget either needs to be tested further or have that content fully represented not as a widget elsewhere in the notebook.

</details>

---

## Related resources

Resources are for information purposes only, no endorsement implied.

[1.3.1]: https://www.w3.org/WAI/WCAG20/quickref/20160105/#content-structure-separation-programmatic