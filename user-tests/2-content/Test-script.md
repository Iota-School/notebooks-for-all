# Content Types in Rendered Notebooks

## Introduction

Hi, I’m ________ I‘ll be running this meeting today. This is ________, they are here to take notes. 

Thank you for taking the time to participate in this study. A few things I want to remind you about before we start:
- This is completely voluntary. Please let me know at any point if you wish to stop participating.
- You can ask questions at any time.
- We are not testing you, we are testing how Jupyter Notebooks behave with assistive tech. There are no correct or incorrect answers.
- You signed a recording consent form before this session. Would you like me to go over what we are recording and where it will be stored as a reminder?

## Participant Introduction

First, I want to ask a few things about you. If we’ve met before, I’d still like to confirm whether or not things have changed.

**What operating system and browser are you using today? (We use this info to reproduce errors and support you if needed.)**

**What assistive tech are you using during this session?**

During this study, we will be exploring a read only webpage that has been exported from a notebook focused on astronomy data analysis hosted by Space Telescope Science Institute.  That means all the code has been run. You can’t edit it like a traditional notebook. I will be giving you broad tasks to complete and ask follow up questions.
 
Throughout the session, please think out loud. Tell us if something unexpected happens, if something works well, if you think something could be improved, or if you’re confused. We do not expect all the tasks to be easy to complete with assistive tech and we invite you to complain!
 
**Before we start, do you have any questions?**

## Notebook Tasks

First, can you please share your screen. If using a screen reader, can you set it so that you share the sound or share the text with a “speech viewer” ex: In NVDA you can set it to hold the NVDA button (insert or caps) and hit N and then you get options, go down to tools, and select speech viewer.

### Task 1 - Opening the notebook

Now I’d like you to open today’s notebook. I’ll tell you how to do this part. 

1. Open your web browser of choice
2. Paste this link: https://eteq.github.io/notebooks-for-all/Imaging_Sky_Background_Estimation.html
3. tinyurl.com/37pncd8n  

**Can you tell me the title of this notebook?**

- Complex 2D Background [Y][N] or Imaging_Sky_Background_Estimation [Y][N]

### Task 2 - Markdown cell basics

First, we’re going to start by exploring the foundational units of a notebook: cells. 

**Are you familiar with notebook cells? If so, can you briefly describe them for me?**

Cells can hold different content types. When they are run, which they have been on this webpage, they may show additional information. We want to understand how you identify and interact with these different types of content.

Start by navigating to the beginning of the notebook. Take a few moments to read down to the Imports heading.

**What type of content did you find in the cell?**

- Markdown [Y][N]  | Writing [Y][N] | HTML [Y][N]

This is a Markdown cell. In an uneditable version of a notebook like this one, it is run and appears as text.

**Please tell me about the process you used when reading that section. Were you able to do everything you expected? Did anything surprise you?**

### Task 3 - Code cell basics

Please return to the end of the Imports section if you navigated elsewhere. You should be at the end of an unordered (bulleted) list. We’re going to explore the section directly below the unordered (bulleted) list.

**What type of content did you find in the cell?**

- Code [Y][N] 

This is a code cell. In this case, it is importing libraries for use later in the notebook. When code cells are run, they are numbered in the order they are run. They also will be labeled as an input (the code the author writes) and an output (the result of running the input). Sometimes additional messages appear when a code cell is run. 

**Can you tell me what number this cell was run as and if it is an input or output?? Cells are labeled visually, and we want to confirm you have access to that label.**

- In [1]: [Y][N]

**How did you find your experience of reading that section? Were you able to do everything you expected? Did anything surprise you?**

**This cell has an additional area of text below the input code block. It is labeled visually with an alternate background color, but may not be labeled non-visually. Please tell me what you think it is. What makes you think that?**

- This section is an error or warning message. [Y][N]

### Task 4 - repeat Task 3 in alternate notebook

Now I’d like you to open an alternate version of the notebook we just reviewed. This notebook has the same content, but different structure. We’ll be asking you to complete some of the same tasks, so don’t worry if you feel like you are giving the same answers. We’re curious to hear you compare the experiences and if you have any preferences.

1. Open your web browser of choice
2. Paste this link: https://iota-school.github.io/notebooks-for-all/user-tests/2-imnotsurewhat/Imaging_Sky_Background_Estimation.html.html5.html
- tinyurl.com/4m9cxeyu 

**Can you read me the title of this notebook?**

- Complex 2D Background [Y][N]

Please navigate to the start of the Imports section and skim-read to the next cell.

**What type of content did you find in this section?**

- Markdown (Writing, HTML) and Code [Y][N] 

**Can you find the number this cell was run as and if this was an input or output? **

- In [1]: [Y][N]

**How was the process of navigating to this cell compared to the experience from the last web page? Do you have a preference?**

### Task 5 - Single chart PNG

Now that we’ve covered the basics of cells, we’re going to explore other types of outputs in this notebook.

Please navigate to Out [7]:, or the output of code cell 7. 

- More support needed? [Y][N]
    - In the “Create the nasty sky background” heading level 3.
    - Above the “Look at it with noise added and then smoothed a bit” heading level 3.
    - Below the table.

**Please tell me what kind of output you think this is. What makes you think that?**

- This is a chart/graph/plot. [Y][N]

**What can you tell me about this chart? What information does this output give you? Does this meet your expectations?**

**Please read us the tics on the Y-axis **

- 0, 200, 400, 600, 800 [Y][N]

**What would you do if you needed to find more information about this output?**

**Please navigate to In [7]:, or the input of code cell 7.**

- More support needed? [Y][N]
    - This is directly above where we ended our last question.

**How did you identify the cell’s input? What information told you these sections were related? What do you wish it told you?**

Please navigate to the “Look at it with noise added and then smoothed a bit” section (heading level 3). Go to the first code cell in this section.
Facilitator note: this is cell In [13]:. Please navigate to this code cell’s output.

**Is there anything different from this image output compared to the previous png you observed? How can you tell?**

### Task 6 - Iframe, video, and errors

**Please navigate to the video on this page.**
- Can they easily search for a video without hint [Y][N]
- Hint: this is cell Out [19]: This is also in the Video1: section (heading level 2).

Please press the play button to activate the video. You may stop/pause it immediately after.

**Walk me through what you needed to do to complete this task.**

**What can you tell me about this video output? What information does this output give you? Does this meet your expectations?**

**What would you do if you needed to find more information about this video output?**

Please navigate to the input code cell for this video.
- Facilitator note: this is cell In [19]:

**Tell me what you find in the input code cell. Is there any information here you wish was in the output as well?**

### Task 7 - Different single chart SVG

Please navigate back to your original browser tab.

Please navigate to Out [54]:, or the output of code cell 54. 
- If more support is needed to navigate, this is in the “Routines to facilitate looking at the RMS of the residual background as a function of scale” heading level 2.
- This chart is the very bottom of the page (excluding footer logo).

**Please tell me what kind of output you think this is. What makes you think that?**

- This is a chart/graph/plot. [Y][N]
- What type of chart?

**Please read us the tics on the Y-axis** 

- BKG2, BKG3, BKG4, BKG5, Perfect [Y][N]

**What can you tell me about this chart? What information does this output give you? Does this meet your expectations?**

**This is a different kind of chart than the prior ones we explored. Are you able to tell what types of charts these are?**

**What information would better help you understand the charts?**

## Follow Up Questions

Now that you’ve explored the notebook, I’d like to ask you to reflect on how that experience went and any other feedback you might have.

**Was there a difference in how you experienced the first version of the notebook we linked you compared with the second one?**

**Please complain – was there anything frustrating about reading content in the Jupyter notebook with your assistive tech?**

**Did you feel confident that you were given all the information available?**

**If you felt information was missing, how would you have preferred that information to be communicated to you?** 

**Do you have any other impressions or feedback that you would like to share?**

**Do you have any questions for me?**

---

## Interview Debrief

After each ethnographic interview you complete, take a few minutes to perform an interview debrief while the session is fresh in your mind. This ensures that key learnings and observations are not lost in the scramble of many interviews or long timelines.

**What are our action items based on this feedback?**

**Any more details on issues we already discovered?**

**Are there any new questions I should explore in a further script?**

**What are some key quotes that I heard?**
