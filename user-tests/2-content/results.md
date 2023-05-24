# Results: Content Access in Rendered Notebooks

These results are from user interviews conducted in November 2022–January 2023 with [the content types test script](Test-script.md) on [the STScI Imaging Sky Background Estimation example notebook](Imaging_Sky_Background_Estimation.ipynb).

## What we tested

**Operating systems:** Mac OS Monterey, Windows 10, Windows 11

**Browsers:** Chrome, Firefox, Safari, Edge

**Assistive tech:** JAWS (screen reader), NVDA (screen reader), VoiceOver (screen reader), Mantis (braille reader), Mac OS Zoom (built-in screen magnifier), color inversion, built-in browser zoom controls, built-in large cursor and pointer settings

**Interface:** Browser and [notebook in HTML form](Imaging_Sky_Background_Estimation.html) hosted via GitHub pages

**Sample size:** 7 participants

**Method:** Combination of qualitative usability testing and user interviews

## Content types

This round of tests emphasized a notebook with a range of content types and tasks designed to have participants engage with them. The following sections describe the experience and feedback of participants sorted by content. They are not listed in any particular order.

### Cells

#### Markdown cells

Markdown cells continue to be approachable for all participants. Whether they are relying on the visuals of rich text rendering or the reliable HTML underpinning it, the consensus is that Markdown content read as expected and was easy to work with because of it. 

Cells continue to have unclear divisions, a fact made more unclear by Markdown cells’ lack of execution number or any other visual division. For the most part, this did not inhibit participants. It only became a factor when participants were trying to navigate by cell.

Participants did not display any major issues working with Markdown content. Some assistive tech, like the JAWS screen readers, handled technical language like inline code in a way that participants found confusing. Because others, like other screen readers and the Mantis Braille reader, handled it in a way that did not confuse their participants, we can only advise that notebook authors be aware; this does not appear to be an issue the notebook itself is responsible for.

#### Code cells

Just like other cells, code cells continue to have unclear divisions, though they do have the boon of execution numbers, borders, and shading that provide a hint. Formally, though, assistive tech did not present them as split sections. Only participants familiar with notebooks searched for these as a means of determining cell divisions. Because code often has syntax that is distinctive from non-code, some participants (the most code-savvy ones) clocked into code cells exclusively because they recognized the different words/commands/content. For the most part, this did not inhibit participants. It only became a factor when participants were trying to navigate by cell.

With structural changes made before this test, screen readers did pick up cells like code cells as an [HTML `article`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/article). Some screen readers allow users to navigate by article. The issue was that all code cells were referred to as “article” alone without any unique descriptions (including no mention of execution number) or mention of it being code at all. While it was good to find the change surfacing, it was not yet useful to users.

The way participants read code cells varied widely based on their set up (ie. operating systems, settings, assistive tech) and personal preference. Options included

* Reading code as any other default text, meaning word by word. This was done by participants using their vision and some screen reader users. With this option, it was possible to miss a switch between Markdown and other code cells, though most participants noticed within the first few seconds because their contents are typically distinct. 
    * Those using vision mentioned that reading code requires more active reading than recognizing word shapes because code often uses made up or conjoined words rather than familiar ones; modifying font/font choice becomes critical in allowing participants to manage the strain active reading puts on them.
* Reading code character by character. This was mentioned by participants using screen readers, though it seems probable that participants using their vision would do the same to identify unfamiliar words. For some participants this was their default screen reader setting when they know they are planning to code, for some this is a preset assigned to a list of applications, and for others this would be a setting they manually adjust to when they feel reading word by word is not serving their needs.
* Reading white space in addition to another setting. This means the white space character’s ( space, tab, etc.) name is read with each repetition. This was only mentioned by screen reader users. Participants that used this method said it can help them identify sections of code outright because the use and frequency of white space is so different than in non-code. This can also help them gain relevant information in code languages where white space is meaningful.
* Manually initiating a preset workflow to copy whole blocks of code—like notebook code cells—and paste them into another application that is more accessible to them. Here they may read, edit, and run code line by line. We did not discuss what they would do if they needed to get code back in the notebook. This was mentioned by the most code-savvy screen reader users, but the workflow is not done on a screen reader itself.
* Reading in chunks by a set number of characters, including white space characters. These chunks do not split at words or other divisions, it is purely by number of character. This was mentioned by Braille reader users—the number of characters per chunk is determined by the Braille reader’s display.

#### Output errors and warnings

Error and warning information appears as additional cell outputs in Jupyter notebooks—additional because they are a grouped separate from an intended run cell output. For brevity, we’ll refer to both errors and warnings simply as errors for the rest of this section. 

Errors provided a challenge for most participants; those not using vision were impacted most severely. That’s because error  information in notebooks is almost entirely visual. Other than the error text, they rely exclusively on low contrast color coding: a light red or orange background. They also appear directly against other output types, so they can be obscured by having a standard text output and and error text back to back. Participants using vision, like those with screen magnifiers or high zoom, were usually able to notice that errors were a separate group and thus find an error quickly. Participants with screen readers consistently had their screen readers pick up and share the error message, but as there was no break between the initial input text, the error message, and any following text it was frequently missed. Screen readers read them as one long paragraph rather than as the separate text areas they appear visually. In summary, assistive tech could completely access errors, but it was communicated ineffectively to its users. 

Most participants recognized errors because of their familiarity with the message; this means that they were relying on the contents of the message rather than message or notebook structure. As useful as this was, it also meant a delay in recognition because words like “error” or “warning” often appear in the middle of the message rather than the start. This recognition also relies on user expertise and prior familiarity with the notebook itself, something that users newer to the field might not have or that might be downright inaccessible to people with different cognitive abilities. Some participants with more comfort in notebooks also used their expectations that an error would appear after the cell to search in depth.

Perhaps the most damning was the comment from a screen reader user: their sighted colleagues can find errors and similar unexpected feedback quicky, but they have to be vigilant and intentionally search to make sure they are receiving necessary and important information.

Participants handled the challenge in a few ways

* Reading all text very carefully and stopping over any area they recognized a key word (usually “error,” “warning,” or a specific name of an error if they knew the code language).
* Rereading cells and their outputs when they noticed elsewhere that something was amiss in the notebook.
* Using the browser find tool to search the notebook’s contents, usually with key words like “error” or “warning.” They would navigate through the option using the keyboard.
* Using a screen reader’s feature to read aloud the background color of a region. This only helps when users first suspect an area is worth investigating. It is not a passive feature.

While participants using their vision did have a comparatively easier time locating and identifying errors, they often could not see the low contrast background color. Participants using inverted colors did not see the background colors at all.

### Images

#### PNG images

PNG images proved an obstacle for most participants. Fortunately, most of the obstacles were created by notebook authoring choices where there is clear room for improvement.

The primary issue with images is that they provide information in an inflexible way. Participants using their vision can magnify or otherwise zoom into an image (though browser zoom does not apply), but that is the only control participants were able to exercise over images. If these same participants cannot get information because the image has areas that are too low contrast, there is nothing they can do; any theme changes or color inversions they may apply elsewhere will not apply to an image. Because of this, low contrast is an extreme blocker for participants to complete tasks related to images.

This provides absolutely zero support for participants not using vision, like screen reader or Braille reader users. Because the images in this notebook had no alt text or other image descriptions, were not described in surrounding context, and provided no ways to access the source information, screen reader and Braille reader users could not complete any image-related tasks in these tests. At most, participants would try and guess based on the information that it was an image and that image file’s name—the only information their assistive tech could access. 

To manage this poor experience, all participants

* Would read before and after the image to try and glean the image’s surrounding context.
* Would search for any links that might send them to an image source, related data, or provide other context.

Participants using their vision also

* Tried to magnify or zoom in on the image. Which methods of magnification or zoom they tired first depended on their personal preference and amount needed. Remember that browser zoom does not zoom the image in a rendered notebook.
* Would adjust their display settings, like using a high contrast mode or inverting colors. These did not successfully impact images.

Participants using screen readers of Braille readers also

* Would explore more aggressively when searching for image information and often noted there was no other recourse. They were effectively locked out from the information in an undescribed image.

#### SVG images

With a default—meaning not manually tagged or otherwise modified—SVG image, participants noted no differences between the experience of the PNG plots versus the SVG plots in this notebook.

#### Chart/visualization feedback

In the notebook used for these tests, a majority of the images were charts or other kinds of visualizations. We received the following feedback on charts used during the test.

* Missing chart information is confusing at best and misleading at worst. Participants often struggled to make sense of what the charts were trying to explain to them because several were missing titles or axis labels. These may seem like the basics to expert chart makers, but neglecting them has clear a negative impact.
* In most cases, summarizing or including a description of the information a chart is meant to convey can help participants dive into the information faster and more deeply. If it is done as a text description, this may also serve as support for screen reader and Braille users as well.
* Plots with default styling made some of the biggest contrast obstacles for participants engaging with the notebook visually. Because they are images, colors and lines and text are not customizable or restylable even for participants who wanted to try. In this case, the default styling often had low contrast color choices representing the data, thin and low opacity lines for trend lines and axes, and small and thin text.
* Use grid lines in charts. When using high magnification, zoom, or otherwise handling a limited field of vision, participants using their vision often could not see both the axes and the data at the same time. Without gridlines, they had nothing to follow to orient that data point in relation to the axes.
* Tables as an alternative for complex content like charts were often responded to as being unpleasant but reliable. This was the same answer whether tables were suggested in the notebook already or if users would have to generate one themselves. For the more confident participants, having access to the source notebook and data was consistently preferable.

### Videos

For the most part, the [`iframe`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe) linked video in our test notebook was usable by participants. Participants were able to complete tasks relating to the video more often than not. When asked to reflect on the experience participants credited the fact that the video and its interface were easier for them to use because it followed video patterns they expected and experienced elsewhere on the internet. 

Video feedback included

* The video did not immediately appear to be a video. For participants using vision, they noted they mistook it for an image because the video player around it does not appear until a user interacts with it. For participants using screen readers, they commented that the video did not have any kind of labeling that told them it was a video; they figured it out when they found the familiar play button (though it did not tell them whether that would be audio or video). This is likely a result of the `iframe` and no additional labeling.
* Participants would like closed caption and/or transcription options.
* The area the video took up was unclear. This became an issue for participants using their vision when they were trying to figure out where they could click to pause and play the video. When magnified or zoomed in, it could also become difficult to tell which parts were video and which parts were notebook background. 
* Because the video player does not appear around the video until the video is played, its controls are unclear. The initial play button that appears as an overlay of the video thumbnail does not seem to be labeled as a play button; screen reader users were guessing when they activated the button.

### Content types not covered

While we aimed to cover a breadth of commonly used content types in these tests, we did not (and could not) cover everything that could possibly be put in a notebook’s cells. For this round of tests, we intentionally did not focus on

* External links
* Tables
* Iframes
* Interactive Widgets

The decision to not focus these was motivated by constraints like the length of a testing session (one hour per participant), the STScI notebooks available to us, the content types most commonly found in public-facing STScI notebooks, prioritizing content types that had received no feedback in prior sessions, and interactivity limits in a rendered notebook.

## Navigation: more feedback

Our [prior tests were centered around notebook structure and subsequent navigation](Test-script.md). Because we addressed some feedback between test sessions and exploring content types does first require navigating to that content, we found further feedback on navigation in this round.

Two visibly identical notebooks with different underlying structure were used during these tests. Feedback is sorted by notebook.

### Labeled cells: notebook structure 1

This notebook structure directly addressed some of the feedback from previous rounds of tests. [Headings](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements) automatically became links. Execution numbers became their own grouping rather than a portion of the tags encapsulating all content for that cell. [`div` tags](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/div)  were removed wherever possible. Participants reported the following.

* This version of the notebook provided some ease in navigation for most participants. Having headings as links allowed non-screen reader users to take advantage of headings. Having headings as links also supplied a different way for screen reader users or other keyboard navigators to explore the notebook structure since this added headings to the list of interactive elements on the page and made them appear with the tab key.
* Requests for a table of contents continued.
* This version received less feedback overall; it was noted as relatively similar to previous tests.


### Tabable cells: notebook structure 2

This notebook structure labeled each cell as an `article` and leveraged other [HTML content categories](https://developer.mozilla.org/en-US/docs/Web/HTML/Content_categories) to provide a more standard HTML structure for assistive tech to hook into. It also made adjustment to some low contrast areas. Participants reported the following.

* This version of the notebook received consistently neutral to unfavorable feedback. Non-screen reader users responded neutrally and seemed almost unimpacted. Screen reader users were most impacted by these changes and gave negative feedback.
* Participants using their vision did give positive feedback on increased color contrast in the execution number and code comments.
* Participants using a screen reader generally needed to be prompted to discover the notebook’s structural changes; this was because the ways it was planned to support them using were not the main ways these participants were interested in interacting.
* Participants were able to successfully use the tab key to navigate through cells (to “tab through cells”).  However, populating the tab list with every cell on top of all interactive areas in the notebook created an “overhead of tabs.” One participant described it as “you don’t know where you are going or what you are looking for. Could be five tabs. Could be fifty” before they can complete the task. This was not considered a positive change.
	* To clarify, the tab key is by default a coarse navigation tool that allows users to jump to and from areas where they can perform some kind of interaction. Without this change in notebook structure, that already included all inline links, headings (because they are also links), the video play button, and all browser-level navigation. Making cells tabable adds an additional type of content to filter through in this list, and in this over-fifty cell notebook adds another fifty-plus items to the list.

## Additional notes

On top of what we discovered on a content type and navigation level, we also found many larger patterns worth noting. They are listed in no particular order.

* There were issues searching and navigating by content type (ie. cell, image, video, so on), but there was a high rate of eventual success. Most tasks were able to be completed by most participants.
* A common sentiment in tests: “annoying but normal.” Participants expressing this sentiment would first encounter an obstacle they knew how to overcome. They would then report that this obstacle was an everyday occurrence for them across the internet and that the notebook was behaving within the current standard for that user experience. Unfortunately, this was one of the most positive types of feedback we received. It tells us we have a lot of room to grow in making enjoyable and equitable user experiences in both Jupyter and in wider digital spaces.
* Unlike in the first set of tests for navigation, participants were more likely to miss information or not be able to access it at all. Interestingly, very few participants expressed that they noticed they were missing information; most remained confident they had access to the whole notebook. The few who did observe that they could not access information were because they found familiar failures—especially images lacking descriptions. 
* Many issues and fixes (requested by participants or found in review) are what might be considered accessibility “basics.” Alt text/image descriptions, labeling, and contrast issues came up frequently. These are very fixable issues, and they need to be done both in the interface and when authoring individual notebook files.
* Participants who are more comfortable and/or familiar with Jupyter notebooks expressed more interest in working with the source notebook when encountering obstacles or when trying to find information that wasn’t immediately findable. For these participants filtering through the non-editable version of the notebook was comparatively not worth the effort.
* Text-based contents regularly gave participants less issues when compared to non-text contents like images or videos. While no content type was without issue, inaccessible images and videos were more likely to completely block participants.
* Participants using screen magnifiers are especially impacted by the lack of maximum width for notebooks in this form. Because magnifying limits how much information fits on a screen and horizontal scrolling is typically more awkward than vertical scrolling, the full-window line length of notebook content came up as a serious pain point and contributor to fatigue. It also increased the risk of screen magnifier users in missing information, especially on the right side (for a notebook in English, a left to right language).
* As in the previous test, some participants would complete or describe completing tasks using an ability that fatigued or even hurt them. For example, if participants with low vision strained to use their vision for completing a task that their assistive tech was unable to work with (due to poor infrastructure or tagging on Jupyter’s part). While there are many ways that inaccessible Jupyter notebooks negatively impact people, this is another way that it harms the people who are determined to work in fields that rely heavily on notebooks.
* Jupyter notebooks often bring together many types of content, and this content can bring its own accessibility issues with it. Notebooks have the capacity to inherit accessibility problems from everything that makes them up—from Jupyter-maintained tools to any other package. For these tests, we ran into issues like lack of image description support for plotting packages, a lack of labeling in the embedded video player and its buttons, and low contrast syntax highlighting themes. On the Jupyter side we can also make choices about what packages to support or how we handle these inaccessible defaults, but the fact that notebooks can surface inaccessibility from anywhere remains a fact.
* Authors will continue to have a large amount of power to determine the accessibility of an individual document. This is part of why we are [drafting authoring recommendations](https://iota-school.github.io/notebooks-for-all/exports/resources/event-hackathon/notebook-authoring-checklist/).
* Participants search for familiarity to anchor their experience. What was familiar to each participant varied depending on their field of expertise, accessibility accommodations used, and what other software they were familiar with, and Jupyter notebook experience specifically. Examples include:
    * Participants who are familiar with Jupyter notebooks would more often talk about cells and try and find ways to distinguish between them. They also were the only participants who called out insufficient divisions and information to find cells.
    * Participants using screen readers were more likely to expect content headings to be more robust. These participants were also more likely to explain their mental model of cells (or other divides) in the notebook by the idea of headings. 
    * Participants used to working with editable versions of notebooks or other source code forms were more likely to compare behaviors to an editable document and asked to have those experiences carry over. For example, some participants wanted to be able to navigate content by editable versus non-editable areas to tell the difference between cell inputs and outputs.
    * Error and warning outputs—a (often unexpected) cell output that reports to users when something in the code run is not functioning as expected—were only findable because there were participants who knew to expect one. Many participants missed the text-only transition to an error message in the test notebook because it had no other indicators. As it was a common error, some participants clocked into it immediately and without host support, but they reported it was only because they have heard that exact sentence many times before.

## Issues

Bugs, issues, and other specific feedback or discussions from this round of tests can be found throughout the repository in issues. Listed below, they are
* [Additional comment on Page title and notebook title do not match](https://github.com/Iota-School/notebooks-for-all/issues/10#issuecomment-1540950862)
* [Additional comment on Explore landmark options in rendered notebook](https://github.com/Iota-School/notebooks-for-all/issues/5#issuecomment-1540967184)
* [Syntax highlighting feedback](https://github.com/Iota-School/notebooks-for-all/issues/54)
* [Improve color contrast in rendered notebook](https://github.com/Iota-School/notebooks-for-all/issues/57)
* [Improve errow/warning cell outputs](https://github.com/Iota-School/notebooks-for-all/issues/58)
* [Improve video output experiences](https://github.com/Iota-School/notebooks-for-all/issues/60)
* [Cell navigation feedback](https://github.com/Iota-School/notebooks-for-all/issues/61)

## Questions for future tests

Based on each session and the conversations we had with the development team, we’ve come up with a list of questions we’d like to explore further.

* What is the most expected or desirable cell navigation experience? Could there be more than one? What are the different possibilities and how could we best compare them?
* Should keyboard shortcuts be a part of the rendered notebook experience? Or should we make better use of the browser defaults?
* How might we increase the discoverability of varied navigation methods in the notebook?
* What are the limits on cell output types and/or content in notebooks converted to HTML? How does the default accessibility on each type stack up?

## What we would do differently next time

Reflecting on these sessions as hosts, for future tests we would like to
* Explore a standard notebook with the STScI computer science channels to further discuss ideas for landmarks or other structural options in notebooks.
* Experiment with asynchronous test sessions for shorter tasks. This might enable an increased number of and more iterative A/B testing in the long term.
