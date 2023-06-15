# Images

## PNG images

PNG images proved an obstacle for most participants. Different notebook authoring choices can be employed to fix many of these issues.

The primary issue with images is that they provide information in an inflexible way. Participants using vision can magnify or zoom into an image (though browser zoom does not apply), but that is the only control participants were able to exercise over images. If these same participants cannot get information because the image has areas that are too low contrast, there is nothing they can do; any theme changes or color inversions they may apply elsewhere will not apply to an image. Because of this, low contrast is an extreme blocker for participants to complete tasks related to images.

This notebook provides absolutely no support for participants not using vision. Because the images in this notebook had no alt text or image descriptions, were not described in surrounding context, and provided no ways to access the source information, screen reader and Braille reader users could not complete any image-related tasks in these tests. At most, participants would take a guess based on the image file’s name—the only information their assistive tech could access. 

To manage this poor experience, all participants:

* Would read before and after the image to try and glean the image’s surrounding context.
* Would search for any links that might send them to an image source, related data, or provide other context.

Participants using their vision also:

* Tried to magnify or zoom in on the image. Which methods of magnification or zoom they tired first depended on their personal preference and amount of zoom needed. Remember that browser zoom does not zoom the image in a rendered notebook.
* Would adjust their display settings, like using a high contrast mode or inverting colors. These did not successfully impact images.

Participants using screen readers or Braille readers also:

* Would explore more aggressively when searching for image information and often noted there was no other recourse. They were locked out from the information in an undescribed image.

## SVG images

With a default—meaning not manually tagged or otherwise modified—SVG image, participants noted no differences between the experience of the PNG plots versus the SVG plots in this notebook.

## Chart/visualization feedback

In the notebook used for these tests, a majority of the images were charts or other kinds of visualizations. We received the following feedback on charts used during the test:

* Missing chart information is confusing at best and misleading at worst. Participants often struggled to make sense of what the charts were trying to explain to them because several were missing titles or axis labels. Not including these fundamental aspects has direct negative impact on readability.
* In most cases, summarizing or including a description of the information a chart is meant to convey can help participants dive into the information faster and more deeply. If done as a text description, this may also serve as support for screen reader and Braille users.
* Default styling of plots were some of the biggest contrast obstacles for participants engaging with the notebook visually. The default styling often had low contrast color choices representing the data, thin and low opacity lines for trend-lines and axes, and small and thin text. Because they are images, colors and lines and text are not customizable or restylable even for participants who wanted to try editing them using developer tools. 
* Use grid lines in charts. When using high magnification, zoom, or otherwise handling a limited field of vision, participants using their vision often could not see both the axes and the data at the same time. Without gridlines, they had nothing to follow to orient that data point in relation to the axes.
* Including the tables of data used to create complex charts was an unpleasant but reliable way of accessing the information in the plot. This was the same answer whether tables were included in the notebook already or if users would have to generate one themselves. For participants more experienced with data analysis, having access to the source notebook and data was consistently preferable.

## Videos

The [`iframe`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe) linked video in our test notebook was mostly usable by participants who completed tasks relating to the video more often than not. When asked to reflect on the experience participants credited the fact that the video and its interface were easier to use because it followed video patterns they expected and experienced elsewhere on the internet. 

Video feedback included:

* The video did not immediately appear to be a video.
	* Participants using vision mistook it for an image because the video player around it does not appear until a user interacts with it.
 	* Participants using screen readers commented that the video did not have any kind of labeling that told them it was a video; they figured it out when they found the familiar play button (though it did not tell them whether that would be audio or video). This is likely a result of the `iframe` and no additional labeling.
* Participants would like closed caption and/or transcription options.
* The area the video took up was unclear.
	* This became an issue for participants using their vision when they were trying to figure out where they could click to pause and play the video.
 	* When magnified or zoomed in, it could also become difficult to tell which parts were video and which parts were notebook background. 
* Because the video player does not appear around the video until the video is played, its controls are unclear. The initial play button that appears as an overlay of the video thumbnail does not seem to be labeled as a play button; screen reader users were guessing when they activated the button.

## Content types not covered

While we aimed to cover a breadth of commonly used content types in these tests, we could not cover everything that could possibly be put in a notebook’s cells. For this round of tests, we intentionally did not focus on

* External links
* Tables
* Iframes
* Interactive Widgets

The decision to not focus these was motivated by constraints like the length of a testing session (one hour per participant), the STScI notebooks available to us, the content types most commonly found in public-facing STScI notebooks, prioritizing content types that had received no feedback in prior sessions, and interactivity limits in a rendered notebook.
