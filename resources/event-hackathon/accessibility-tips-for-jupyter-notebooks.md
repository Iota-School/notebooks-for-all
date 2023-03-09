# Accessibility Tips for Creating & Publishing Jupyter Notebooks

By the [Notebooks for all](https://github.com/Iota-School/notebooks-for-all) team

Draft 2: February 21, 2023

---

The accessibility of Jupyter Notebooks is determined by many factors, many not in the direct control of notebook authors. For example, specific libraries may create outputs that are not accessible to screen readers, and default export options may create outputs that have issues related to contrast or keyboard navigation. Further, it is important to note that, currently, editing Jupyter Notebooks is largely not accessible for screen reader users.

Despite these serious challenges, there are ways that notebook authors can create notebooks that are more accessible for users with disabilities. This document will give context on accessibility in Jupyter Notebooks and provide some tips and best practices for authoring and publishing accessible notebooks.

## Notebook Formats

 Depending on the export method and content, notebooks can allow for different levels of accessibility for people using assistive technology. Users encounter notebooks in a variety of formats:

- [The editable notebook format](https://jupyter.org/try-jupyter/lab?path=notebooks%2FIntro.ipynb) — This format is designed to be opened directly in the Jupyter environment for editing and take the form of `.ipynb` files. This format is currently **inaccessible** to screen reader users and has many obstacles to navigating the UI and editing cells
- [Uneditable notebooks exported to HTML](https://iota-school.github.io/notebooks-for-all/exports/Imaging_Sky_Background_Estimation-tab-to-content-nav-high-contrast.html) — These `.html` files created through the `nb-convert` exporter are designed to be opened in a browser and are often shared on the web. This format is **somewhat accessible** because HTML is built for web accessibility. While there are issues, people tend to succeed in accessing a majority of notebooks exported in this format.

The interactive notebook format still does not play well with assistive technology, particularly in navigating the UI and editing cells. The exported “read only” notebooks can be read fairly well, but still have some issues. If you want your content to be 100% accessible, Jupyter notebooks are currently not the best way to publish your content (though they can be converted to HTML for a better read-only accessibility experience). Consider if there is an alternate format that could work just as well, or publish a “read only” export alongside the editable one so at least the content is readable by everyone. That said, things will not be truly accessible until we provide access to content creation, not just knowledge consumption.

There is work to be done to improve the way Jupyter Notebooks are exported to HTML, and we are running tests with affected users to figure out what changes would best improve accessibility in this area. Eventually, we hope to push changes and improvements upstream. This is a slow process with not enough people working on it. We have several [open issues](https://github.com/Iota-School/notebooks-for-all) and hopefully our team and others will make improvements in the next few years. But that does not solve the problem right now.

Since editable notebooks published as `.ipynb` files currently have serious issues related to accessibility, there is little that notebook authors can do to help people with disabilities access this format. However, the accessibility of HTML notebooks can be significantly improved by using specific best practices. By following the below tips, you can act to make a difference in the accessibility of your notebooks.

## Future Plans and Next Steps

* We will be publishing a best practice document for authoring Jupyter Notebooks
* Attend the accessible notebook hackathon we are running to practice the tips included below on a notebook you intend to publish (March 10th 10-12:30 EST)
* We will publish a read only notebook format (correct word?)  available on github that has improved navigation, color contrast, etc which you can apply to your static NB viewer notebooks before publishing

## Authoring Tips (Draft)

### Use well-formatted Markdown

Use content headings. There is only one H1. Do not skip heading levels.

### All text in the document needs to appear as plain text

* If there’s text in an image, in a chart, in a video, in an audio recording, or other relatively inaccessible formats, it should also be in plain text somewhere. There are multiple ways you can handle this depending on content and context.
* Options for providing information in plain text alongside other formats include: adding a description, including a caption, or describing everything fully in surrounding paragraphs.

### Visualization Accessibility

* Include titles in visualizations, such as the outputs from libraries such as Matplotlib. Both in plot and as a property.
* Label visualization axes, include keys/legends 
* They should have good contrast (the relative difference in tonal hues). Be cautious of low opacity and thin lines, or color choices that are too similar, such as light gray on white. Try https://github.com/Quansight-Labs/accessible-pygments 
* Consider plotting in only black and white. You can always add color later.
* Don’t rely only on color to convey information. Include labels. Consider using a mix of color and patterns to differentiate values.

### Descriptive text for visual areas

* When using an image with an .img tag in the HTML, alt text may be used normally
* When creating a plot or graph, some libraries allow alt text and others don’t. Captions and titles should be used to fill in information that alt text would normally contain when there is no option for it. 
* Legends, Axis labels, numbered tic-marks, and other text in generated graphs cannot currently be read by a screen reader and may be too small for low vision people to find with magnification. 
* When writing alt text for a plot, Include: 
    * Type of Plot (bar chart, image, scatter-plot,etc)
    * Title of graph
    * Axis labels and range
    * Key / legend
    * General explanation of graph and what it is communicating
* It can be very helpful to link to a file containing the original data, or if possible include a data table near the plot so it can be accessed in a non visual way
* Include a sonification for a plot. You can use [Astronify](https://astronify.readthedocs.io/en/latest/) to do this for time series and spectral astronomy data.

### Organization

To help people orient themselves in the notebook and understand what to expect, give some context at the beginning. We recommend:
* Give the document a title. This should be the one H1 you use, and it should be at the top.
* Include a summary of the document under the title.
* Add a table of contents as an ordered list (even if it cannot contain links)
* Add the author and affiliation, where relevant
* Include information such as the date and time first published and the date and time last edited.
* Link to the notebook source, where it can be used in editable form

### Color contrast

* Color Contrast for in[] out[] can be templated to be higher contrast, standard does not read well for low vision
* Use a syntax highlighting theme that considers accessible contrast (examples at ericwbailey/a11y-syntax-highlighting)

### Use “plain language”

* Define acronyms the first time you use them and use them sparingly
* Only use field-specific terms when needed. Use approachable language when the terms aren’t critical to understanding the rest of the document or related literature.
* More general tips on stylistic choices with accessibility considerations can be found on Google’s developer documentation style guide.

### Use descriptive link names!

* Do not: Click here!
* Do: Learn more at Space Telescope

### Lead into your code cells (where relevant)

* Make sure they are under other content headings (ie. an imports cell can be preceded by a markdown cell with a header “Imports”)
* Tell what the cell should do before it is done. Usually this is in a markdown cell before, but it also could be a comment in the code cell.
* Do not list several different ways someone could complete the task unless that is the point of the notebook. Focus on what you are doing first, and mention alternates later if needed.

### Comment on your code (where relevant)
* This is especially important for long stretches of code or where more specificity is needed. 
