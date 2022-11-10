# Results: Structure & Navigation in Rendered Notebooks

These results are from user interviews conducted in August 2022 with [the navigation test script](test-script.md) on [the STScI tutorial sample notebook](stsci_example_notebook.ipynb).

## What we tested

**Operating systems:** Mac OS Monterey, Windows 10

**Browsers:** Chrome, Firefox, Safari

**Assistive tech:** JAWS (screen reader), NVDA (screen reader), VoiceOver (screen reader), Mantis (braille reader), Mac OS Zoom (built-in screen magnifier), built-in browser zoom controls, built-in large cursor and pointer settings

**Interface:** Browser and [notebook](stsci_example_notebook.ipynb) in HTML form via nbconvert(hosted via GitHub pages)

**Sample size:** 6 participants

**Method:** Combination of qualitative usability testing and user interviews 

## How users navigated

The following sections describe the ways participants chose to navigate through a single notebook (one browser page). These methods are likely not notebook-specific, but they have only been noted in that context. They are not listed in any particular order.

### By headings

This navigation method appeared exclusively with participants using screen readers.

1. Have a screen reader active.
2. Using that [screen reader's Headings shortcut](https://dequeuniversity.com/screenreaders/), open the Headings list. This moves focus outside the notebook and browser.
3. Review and select heading to jump to.
4. Keyboard focus and page scroll jumps to that heading.

Because nbconvert for notebook to HTML properly captures Markdown cell headings as HTML headings, heading organization is technically available regardless of assistive tech or other settings. At the time of writing, though, there is no way for someone not using a screen reader to interact with the headings in the same way.

Non-screen reader using participants frequently requested a table of contents to jump to major content areas in the same way that we saw screen reader using participants do. Only one screen reader using participants made the request for a table of contents, and even then it was mentioned as a personal preference over headings and not as a blocking issue.  No screen reader using participants expressed trouble jumping between content areas, and they all used heading navigation at some point.

### By preset keys

This navigation method is not reliant on any assitive tech or setting. Because keys are configurable, keyboard language/region can be configured, and physical keyboards can be different, there is a lot of variation on how users might have preset keys to navigate. During our sessions, we saw

1. Have a keyboard with `end of page` and/or `top of page` keys configured.
2. When participants knew or expected the goal would be near one end of a page, or simply closer to shorten navigation, they would use the relevant key to jump to a different area.
3. Keyboard focus and page scroll jumps to that area.
3. If needed, participants navigate the rest of the way to goal using an additional navigation method.

Navigating by preset page navigation keys rarely took users exactly where they wanted to go on its own; it was used in combination with another method in any case where the goal was not singularly "go to the bottom of the document" (as in Task 4) or "go to the top of the document" (as in Task 5).

This was used by participants who used browser zoom, or in one case a screen reader. Participants expect this to work at a browser level, so it is not tied specifically to the notebook.

### By zooming and skimming

This navigation method appeared exclusively with participants using browser zoom/magnification. They are similar, but have been broken into different steps to preserve the nuances of each.

For a magnifier:

1. Magnify the left side of the notebook. Amount needed may vary per participant, but the magnification stays at a consistent amount at first. Content does not reflow.
2. Scroll along the left side of the notebook. What is visible depends on participants' magnifier settings; it could be that only a section of the browser window is visible on screen, that a single rectangular area is magnified while the rest of the window remains visible at 100% in the background, or things in between.
3. Find an area that appears to be realted to the goal. Stop scrolling and adjust magnification as desired.
4. Read the content while moving magnifier to the right to complete a line. 
5. At the end of each line, participants would move back to the left to start the next line unless they either found their goal or decided they would not complete their goal in the area.
6. When they need to navigate again, participants would start at step one again.

For browser zoom:

1. Zoom browser to about 150–250%. Content should reflow.
2. Scroll along the left side of the notebook. Only the start and far right of each cell and output are visible in the window.
3. Find an area that appears to be realted to the goal. Stop scrolling with it roughly centered on the page.
4. Increase browser zoom to 300–500%. Rescroll to desired point if necessary; the notebook did not hold scroll poisitons in the center so it was necessary for our tests, but participants noted this was not always their expectation.
5. Read the content scrolling to the right to complete a line. 
6. At the end of each line, participants would scroll back to the left to start the next line unless they either found their goal or decided they would not complete their goal in the area.
7. When they need to navigate again, participants would lower browser zoom to start at step one again.

When navigating with this method, participants emphasized how important the far left content was to them, whether zooming in a way that caused the content to reflow or not. Working with notebooks in English means that we did not have the opportunity to test where participants would go to skim content in a right-to-left language or in non-document formatting, but it is safe to conclude that skimming and reading content in full are two different modes for people who navigate this way.

Participants using this method also frequently brought up the utility of table of contents to hasten their navigation and lower the physical demands of reading as a result.

### With `find` controls

This navigation method appeared exclusively with participants using screen readers. It only came up once throughout sessions and test hosts were only able to get limited information on it. it may not be entirely accurate. Reference this section with that in mind. 

1. From anywhere on the page or in the browser, open the screen reader's built in `find` type of controls.
2. Input filtering criteria, review and select an option.
3. Keyboard focus and page scroll jump directly to the selected option.

This can be done with features like [NVDA's Search for a word or a phrase](https://dequeuniversity.com/screenreaders/nvda-keyboard-shortcuts) or [VoiceOver's rotor](https://dequeuniversity.com/screenreaders/voiceover-keyboard-shortcuts#vo-mac-the-rotor). It is similar to a browser's `find` features in that it filters the application content and allows users to navigate based on that.

This method was used by participants most frequently when other navigation and skimming methods failed to help them complete a task. For example, it was common for participants to use several navigation methods when completing Task 2 since many expressed the author's name was not where they expected it to be (it was at the bottom of the document rather than the top). 

There was one instance where a screen reader participant used this navigation method right away, and that was because they had found the content needed to complete the task when skimming in a prior task and did not remember what heading it was under. They noted this was feasible because they remembered the content and knew what to filter for.

### By tabbing through interactive areas

This navigation method is not reliant on any assitive tech or setting. While this technique is possible to anyone regardless of OS, browser, or assistive tech, the only participants we saw using this were screen reader users.

1. Use the `tab` key. The next interactive element in the focus order (ie. a link, a button, so on) will have keyboard focus.
2. Use the `tab` key repeatedly until reaching the desired area. Focus order does loop, so one may jump from the bottom of the notebook to the top of the browser, for example.

This navigation method was used infrequently, and it was used in combination with other navigation methods. Most frequently, tabbing was used as a fine-grain navigation once participants were in the general region they wanted to be. For example, a participant used a screen reader to jump to a content heading and then skip through cells via tabbing to skim for an area they were searching for.

## Common feedback

This is a list of the feedback that was most frequently or emphatically given. It is in no paritcular order.

- Requests for a table of contents. This was particularly important to participants not using screen readers.
- Notebooks need to be edited too, not just read. Participants that gave this feedback were aware of the scope of these tests and they wanted to emphasize that accessibility fixes also needed to happen for editable states.
- Notebook cells were of varying importance. How people want to understand and navigate the notebooks seemed to depend most on their expectations. Some participants talked in terms of cells or noted that they couldn't find non-visual cell sections (this was more common of participants who author notebooks, but not exclusive to them). Some participants talked in terms of content headings from the notebook cells. Some didn't mention either. This test did not allow us time to dive into why different participants had different mental models.

## Issues

Bugs, issues, and other specific feedback or discussions from this round of tests can be found throughout the repository in issues. Listed below, they are

- [Explore landmark options in rendered notebook](https://github.com/Iota-School/notebooks-for-all/issues/5)
- [Automatically add link to rendered notebook source](https://github.com/Iota-School/notebooks-for-all/issues/8)
- [Add a table of contents to rendered notebooks](https://github.com/Iota-School/notebooks-for-all/issues/9)
- [Page title and notebook title do not match](https://github.com/Iota-School/notebooks-for-all/issues/10)
- ["Top of Page" link in template footer bug](https://github.com/Iota-School/notebooks-for-all/issues/11)
- [Explore options for minimizing content on left side of rendered notebook](https://github.com/Iota-School/notebooks-for-all/issues/12)
- [Review/explore keyboard shortcuts in rendered notebooks](https://github.com/Iota-School/notebooks-for-all/issues/13)
- [Explore ARIA options in rendered notebook](https://github.com/Iota-School/notebooks-for-all/issues/14)
- [Code cells cut off content at high zoom in rendered notebook](https://github.com/Iota-School/notebooks-for-all/issues/15)
- [Vertical scroll jumping when adjusting browser zoom in rendered notebooks](https://github.com/Iota-School/notebooks-for-all/issues/17)
- [Table Reading with screenreaders](https://github.com/Iota-School/notebooks-for-all/issues/18)
- [Navigate to cells using keyboard commands](https://github.com/Iota-School/notebooks-for-all/issues/19)
- [Share Cell Content with screenreaders](https://github.com/Iota-School/notebooks-for-all/issues/20)
- [Move Metadata to the top](https://github.com/Iota-School/notebooks-for-all/issues/21)
- [Notebook Tutorial Link](https://github.com/Iota-School/notebooks-for-all/issues/22)
- [Markdown should be used only as intended](https://github.com/Iota-School/notebooks-for-all/issues/23)
- [Best Practice for Documenting Table Headers](https://github.com/Iota-School/notebooks-for-all/issues/24)

## Questions for future tests

At the end of each session, we noted questions we wanted to further explore. This is the cumulative list.

- For a screen reader reading a code block in a Markdown cell, it read the content line by line instead of as a whole block. This was different than inline code styling or a code cell. Some participants expressed confuison. This would be good to text for mixed content types in a single cell, or even in the same line, perhaps.
- How easy is it to navigate in/out, and between certain content types (ie. tables were mentioned as “if you’re in a table its a pain to jump to another part of the page and then back to the same part of the table”)?
- Should we explore UX for a table of contents? It is helpful for keeping context, but should be collapsible because of the space it can take up.
- Consider zooming in on content types as a task for future content-type tests.
- Should we let participants read the whole notebook first? Let them give first impressions and see how they decide to read the whole notebook.

## What we would do differently next time

Reflecting on these sessions as hosts, for future tests we would like to 

- Have a non-template notebook to work with. Multiple participants spent some of the tasks getting caught up figuring out why the notebook content switched topics often, expressed confusion that the notebook did not follow the narrative it expected when searching for information in multiple tasks, or found it difficult to summarize then notebook when asked in Task 5.
- Considering comparing some solutions side by side. As the first test, it is important to have a sense of the current state of nbconverted HTML notebooks but it doesn't always give us clarity on desired UX.
