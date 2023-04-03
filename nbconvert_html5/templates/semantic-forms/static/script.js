// 

const mediumScreen = window.matchMedia('(min-width: 768px)')

function setTocFocus() {
    var id = window.location.hash;
    if (id.startsWith("#/cells")) {
        document.querySelector("#nb-cells-slider-widget").focus();
    } else {
        document.querySelector(`main >  header a[href="${window.location.hash}"]`).focus();
    }
}

function getParentRow(element) {
    console.log(element);
    return element.tagName == "TR" ? element : getParentRow(element.parentElement)
}

function setHeadingLinkFocus() {
    var tag = window.location.hash.startsWith("#/cells") ? "texarea" : "a";
    document.getElementById(window.location.hash.substring(1)).querySelector(tag).focus();
}

window.addEventListener('load', function () {
    var widget = document.getElementById("nb-cells-slider-widget");
    // add a quicky key to open the table of contents
    var toc = document.getElementById("nb-toc");

    document.addEventListener("keydown", (key) => {
        if (key.key == "?") {
            document.querySelector("#nb-toc").toggleAttribute("open");
        }
    });

    // escape the table of contents
    toc.addEventListener("keydown", (key) => {
        key.key == "Escape" ? toc.toggleAttribute("open") : null;
    });

    // toggling the toc sets focus on the document or the table of contents
    toc.addEventListener("toggle", () => {
        toc.open ? setTocFocus() : setHeadingLinkFocus()
    });

    // click handlers for the table of contents navigation
    document.querySelectorAll("#nb-toc a").forEach((x) => {
        x.addEventListener("click", (event) => {
            event.preventDefault();
            // the link in the document
            var a = document.getElementById(event.target.href.split("#", 2).at(-1));
            history.replaceState({}, `${x.textContent}`, event.target.href);
            mediumScreen.matches ? a.scrollIntoView() : toc.toggleAttribute("open");

            // update the widget with the parent cell
            var row = getParentRow(a);
            widget.value = row.getAttribute("aria-posinset");
            widget.dispatchEvent(new Event("input"));
        })
    });


    // update the url location when headers are passed.
    document.querySelectorAll("table :where(h1, h2, h3, h4, h5, h6) > a").forEach((x) => {
        x.addEventListener("focus", (event) => {
            widget.value = getParentRow(event.target).getAttribute("aria-posinset");
            this.setTimeout(
                () => history.replaceState({}, `${event.target.textContent}`, event.target.href), 800
            );
        })
    });

    // link the cells text area to the cell anchor and update it on tabbing
    document.querySelectorAll("tr.code.cell td.source textarea, td.outputs").forEach((x) => {
        x.addEventListener("focus", (event) => {
            var number = getParentRow(event.target).getAttribute("aria-posinset");
            widget.value = number;
            history.replaceState({}, `Code cell ${number}`, `#/cells/${widget.value}`);
        })
    })

    var slider = document.getElementById("nb-cells-slider-widget");
    // define the cell slider input triggers we scroll a cell into view
    slider.addEventListener("input", (event) => {
        var id = `#/cells/${event.target.value}`;
        event.target.nextElementSibling.value = event.target.value;
        document.getElementById(id.substring(1)).scrollIntoView();
    });

    // the cell slider updates the page history
    slider.addEventListener("change", (event) => {
        var id = `#/cells/${event.target.value}`;
        history.replaceState({}, `Cell ${event.target.value}`, id);
    })

    // update the cell slider when the page loads
    slider.dispatchEvent(new Event("input"));
});