# `nbconvert-a11y` reference templates

the primary intent is to provide reference implementations of accessible computational notebooks. the reference implementations are designed from aria first and second principles to develop semantic html5 representations of notebooks and their components. the templates try to use as much native styling as possible, their views are quite plain. they MAY be used as actual templates for accessible documentation, but style is not a priority and `nbconvert-a11y` relies strongly on native style. it is possible for template users to further customize their styling with custom css.

## goals

a popular resource for accessibility developers are the ARIA practicing guides that provide. these resources do have known issues, but that does not detract from the idea that a reference implementation is valuable for developing accessible applications. this work intends to provide a reference for computational notebooks.

varied applications of notebooks make it difficult to choose a single reference implementation. this library provides multiple reference implementations that representation minimal, standards-compliant templates.

* a well formed accessibility tree / object model
* aaa priority compliance that gracefully degrades into aa and a
* a _hull_ of multiple reference implementations
* test experiences on assistive technologies


### non-goals

* extra css styling
* replace existing templates
* advanced interactive applications

there are several accessible variants of notebooks that are implemented in this repository, and some more could exist like shadow down templates.

## first principle templates

<blockquote cite="https://www.w3.org/TR/using-aria/#firstrule">
If you can use a native HTML element or attribute with the semantics and behavior you require already built in, instead of re-purposing an element and adding an ARIA role, state or property to make it accessible, then do so.
</blockquote>

first principle reference templates use semantically meaningful dom tags.

- [x] cells are `section` landmarks with implicit `role=region`
- [x] cells are `li` ordered list items
- [x] cells are `tr` rows in a `table`

## second principle templates

having multiple first principle reference templates indicates the variety of potential applications. each of the first order templates expose different navigation techniques to assistive technology users, and choosing a single technique may not be possible. to embrace the pluralism, we use the `table` as a flexible interface for providing different assistive technology navigation techniques by transforming tables into lists or tables.

there is a single second principle implementation that projects the structured data into a table representation. learn more in that template.


## shadow dom templates

it is important for these reference implementations to exist to guide decisions in other products. reference implementations and expected patterns can be valuable in guiding decisions in other products like JupyterLab.

there have been, and will be, discussions about web components in computational notebook applications. there are plenty of reports about accessibility challenges with web components.

* https://nolanlawson.com/2022/11/28/shadow-dom-and-accessibility-the-trouble-with-aria/
* https://marcysutton.com/accessibility-and-the-shadow-dom

having a reference implementation using the `template` and `slot` tags to inspect the shadow dom accessibility implications based on current reference implementations. we'd benefit to learn how the assistive experience may suffer if a first or second principle shadow do approaches were used. 


## web content accessibility guidelines as a user interaction

the intent of these templates is too begin with priority aaa compliant substrates for content in computational notebooks. "should we target priority aaa? couldn't we make an easier goal." is a common sentiment in retrofitting accessibility. our approach targets priority aaa compliance with the ability to remove constraints for those that would prefer less strict accessibility conditions. priority AAA will often benefit low vision and ambulatory conditions, but they may be too much for an abled user.

some examples of progressive accessibility changes:

* using native representation of source code to always satisfy AAA priority versus pygments highlighting when priority AA is preferred.
* target size has AAA and AA guidelines. target sizes are expected to be larger with AAA compliance and smaller with AA compliance.