# Content types

This round of tests emphasized a notebook with a range of content types and tasks designed to have participants engage with them. The following sections describe the experience and feedback of participants sorted by content. They are not listed in any particular order.

## Cells

### Markdown cells

Markdown cells were an approachable format for all participants. Whether they are relying on the visuals of rich text rendering or the reliable HTML underpinning it, the consensus is that Markdown content read as expected and was easy to work with because of it. 

Cells continue to have unclear divisions, a fact made more unclear by Markdown cells’ lack of execution number or any other visual division. For the most part, this did not inhibit participants. It only became a factor when participants were trying to navigate by cell.

Participants did not display any major issues working with Markdown content. Some assistive tech, like the JAWS screen readers, handled technical language like inline code in a way that participants found confusing. Because other reading methods, like non-JAWS screen readers and the Mantis Braille reader, handled it in a way that did not confuse their participants, we can only advise that notebook authors be aware; this does not appear to be an issue the notebook itself is responsible for.

### Code cells

Like other cells, code cells continue to have unclear divisions, though they do have the boon of execution numbers, borders, and shading that provide visual hints. Formally, though, assistive tech did not present them as separate sections. Only participants familiar with notebooks searched for these as a means of determining cell divisions. Because code often has syntax that is distinctive from non-code, the most code-savy participants recognized code cells exclusively because they were familiar with the different words/commands/content. For the most part, this did not inhibit participants. It only became a factor when participants were trying to navigate by cell.

With structural changes made to the notebook before this test, screen readers did pick up cells like code cells as an [HTML `article`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/article). Some screen readers allow users to navigate by article. The issue was that all code cells were referred to as “article” alone without any unique descriptions (including no mention of execution number) or mention of it being code at all. While it was good to find the change surfacing, it was not yet useful to users.

The way participants read code cells varied widely based on their set up (ie. operating systems, settings, assistive tech) and personal preference. Options included

* Reading code as any other default text, meaning word by word.
	* This was done by participants using their vision and some screen reader users. With this option, it was possible to miss a switch between Markdown and other code cells, though most participants noticed within the first few seconds because their contents are typically distinct. 
	* Those using vision mentioned that **reading code requires more active reading than recognizing word shapes because code often uses made-up or conjoined words rather than familiar ones;** modifying font/font choice becomes critical in allowing participants to manage the strain active reading puts on them.
* Reading code character by character.
	* This was mentioned by participants using screen readers, though it seems probable that participants using their vision would do the same to identify unfamiliar words.
 	* Some participants switch to this screen reader setting when they code, others assign this as a preset to a list of applications, and others manually adjust this setting when they feel reading word by word is not serving their needs.
* Reading white space in addition to another setting.
	* This means the white space character’s ( space, tab, etc.) name is read with each repetition.
 	* This was only mentioned by screen reader users.
  	* Participants that used this method said it can help them identify sections of code outright because the use and frequency of white space is so different than in non-code. This can also help them gain relevant information in code languages where white space is meaningful.
* Manually initiating a preset workflow to copy whole blocks of code—like notebook code cells—and paste them into another application that is more accessible to them.
	* Here they may read, edit, and run code line by line.
 	* We did not discuss what they would do if they needed to get code back in the notebook.
  	* This was mentioned by the most code-savvy screen reader users, but the workflow is not done on a screen reader itself.
* Reading in chunks by a set number of characters, including white space characters.
	* These chunks do not split at words or other divisions; it is purely by number of characters.
 	* This was mentioned by Braille reader users—the number of characters per chunk is determined by the Braille reader’s display.

### Output errors and warnings

Error and warning information appears as additional cell outputs in Jupyter notebooks, they are grouped separately from an intended run cell output. For brevity, we’ll refer to both errors and warnings simply as errors for the rest of this section. 

Finding and identifying errors was a challenge for most participants and extremely difficult for those not using vision. Error information is almost entirely visual. Other than the error text itself, errors are differianted with padding: a visual break between the section above and below, and low-contrast color coding: a light red or orange background. The color coding was not discernable for those using color inversion or screenreaders. Errors syntax melds directly with the outputs above and below them, so they can be obscured by having a standard text output and error text back to back. Participants using vision, like those with screen magnifiers or high zoom, usually noticed the visual break and thus found errors quickly. Participants with screen readers consistently heard the error message read, but since there was no syntactic break between the error and the other code cells, it was frequently missed. Screen readers read them as one long paragraph rather than as separate text sections. 

Most participants recognized errors because of their familiarity with the message; they were forced to rely on the content rather than organizational structure, a much slower reading experience. Because words like “error” or “warning” often appear in the middle of the message rather than the start, this meant a delay in recognition. This recognition relied on user expertise and prior familiarity with the notebook itself, biasing readability against users newer to the field and those with different cognitive abilities. Some participants with more notebook experience used their knowledge of notebook layout, errors appear after the cell, to search in depth.

This comment from a screen reader user summarizes the inaccessible error design's impact: my sighted colleagues can find errors and similar unexpected feedback quickly, but I have to be vigilant and intentionally search to make sure I receive necessary and important information.

Participants handled the challenge in a few ways:

* Reading all text very carefully and stopping over any area they recognized a keyword (“error,” “warning,” or a specific name of an error if they knew the code language).
* Rereading cells and their outputs when they noticed elsewhere that something was amiss in the notebook.
* Using the browser find tool to search the notebook’s contents, usually with keywords like “error” or “warning.” They navigated using the keyboard.
* Using a screen reader’s feature to read aloud the background color of a region. This only helps when users first suspect an area is worth investigating. It is not a passive feature and must be intentionally activated by the user.
