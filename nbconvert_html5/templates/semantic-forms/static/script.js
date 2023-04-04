function setTocFocus() {
    var id = window.location.hash;
    document.querySelector(id.startsWith("#/cells") ? "#nb-nav-cells-widget" : `main >  header a[href="${window.location.hash}"]`).focus();
}

function getParentRow(element) {
    return element.tagName == "TR" ? element : getParentRow(element.parentElement)
}

function setHeadingLinkFocus() {
    document.getElementById(window.location.hash.substring(1)).querySelector(
        window.location.hash.startsWith("#/cells") ? "textarea" : "a"
    ).focus();
}

window.addEventListener('load', function () {
    var widget = document.getElementById("nb-nav-cells-widget");
    // add a quicky key to open the table of contents
    var toc = document.getElementById("nb-nav");

    document.addEventListener("keydown", (key) => {
        if (key.key == "Escape") {
            // this event shouldnt happen in an interactive element.  
            toc.toggleAttribute("open", key.ctrlKey ? undefined : false);
        }
    });

    // toggling the toc sets focus on the document or the table of contents
    toc.addEventListener("toggle", () => {
        toc.open ? setTocFocus() : setHeadingLinkFocus()
    });

    // click handlers for the table of contents navigation
    toc.querySelectorAll("#nb-nav a").forEach((x) => {
        x.addEventListener("click", () => {
            toc.toggleAttribute("open");
        })
    });


    // update the url location when headers are passed.
    document.querySelectorAll("table :where(h1, h2, h3, h4, h5, h6) > a").forEach((x) => {
        x.addEventListener("focus", (event) => {
            widget.value = getParentRow(event.target).getAttribute("aria-posinset");
            history.replaceState({}, `${event.target.textContent}`, event.target.href);
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

    var slider = document.getElementById("nb-nav-cells-widget");

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