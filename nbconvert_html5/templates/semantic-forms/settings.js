const SELECTORS = {
    "table": "table#cells",
    "body": "table#cells>tbody",
    "row": "table#cells>tbody>tr",
    "heading": "table#cells>tbody>tr>th",
    "cell": "table#cells>tbody>tr>td",
}, ROLES = {
    "list": {
        "table": "presentation",
        "body": "list",
        "row": "listitem",
        "header": "none",
        "cell": "none",
    }, "table": {
        "table": "table",
        "body": null,
        "row": null,
        "header": null,
        "cell": null,
    }, "landmark": {
        "table": "presentation",
        "body": "group",
        "row": "region",
        "header": "none",
        "cell": "none",
    }, "presentation": {
        "table": "presentation",
        "body": "none",
        "row": "none",
        "header": "none",
        "cell": "none",
    }
};

function toggleColorScheme() {
    let value = document.forms.settings.elements["color-scheme"].value;
    let opposite = value == "dark" ? "light" : "dark";
    document.getElementById(`nb-${value}-theme`).removeAttribute("disabled");
    document.getElementById(`nb-${opposite}-theme`).setAttribute("disabled", null);
    document.querySelector(`head > meta[name="color-scheme"]`).setAttribute("content", value);
    activityLog(`${value} mode activated`)
}
function toggleRole() {
    let value = document.forms.settings["table-role"].value;
    for (const [k, selector] of Object.entries(SELECTORS)) {
        document.querySelectorAll(selector).forEach(
            (x) => {
                if (ROLES[value][k] == null) {
                    x.removeAttribute("role")
                } else {
                    x.setAttribute("role", ROLES[value][k])
                }
            }
        );
    }
    activityLog(`notebook cell navigation set to ${event.target.value}.`);
}
document.forms.settings.elements["table-role"].forEach(
    (x) => { x.addEventListener("change", toggleRole) }
)
function changeFont() {
    let value = document.forms.settings["font-size"].value;
    document.getElementById("nb-font-size-style").textContent = `:root {--nb-font-size: ${value};}`
    activityLog(`font size change`)
}
function changeFontFamily() {
    let value = document.forms.settings["font-family"].value;
    document.getElementById("nb-font-family-style").textContent = `:root {font-family: ${value};}`;
    activityLog(`font family change`)
}
function activityLog(msg, silent = false, first = false) {
    document.querySelectorAll("details.log+table").forEach(
        (body, i) => {
            let tr = document.createElement("tr"),
                th = document.createElement("th"),
                time = document.createElement("time"),
                td = document.createElement("td"),
                out = document.createElement("output"),
                now = Date.now();
            out.textContent = msg;
            th.append(time);
            time.setAttribute("datetime", now);
            time.textContent = now;
            tr.append(th);
            tr.append(td);
            td.append(out);
            silent ? out.setAttribute("aria-hidden", true) : null;
            body.append(tr);
            if (!i && document.forms.settings.elements.speech.checked) {
                // a non-screen reader solution for audible activity.
                speechSynthesis.speak(new SpeechSynthesisUtterance(msg));
            }
        }
    )
};
function openDialog() {
    event.preventDefault();
    document.getElementById(event.target.getAttribute("aria-controls")).showModal();
};
const L = 37, U = 38, R = 39, D = 40;
document.addEventListener("load", () => {
    document.querySelectorAll("table[role=grid]").forEach(
        (x) => {
            x.addEventListener("keydown", (e) => {
                let target = document.activeElement;
                let i = Array.prototype.indexOf.call(target.parentElement.parentElement.childNodes, target.parentElement);
                switch (e.code) {
                    case L:
                        break
                    case U:
                        break
                    case R:
                        break
                    case D:
                        break
                };
            })
        }
    );
    document.forms.settings.elements["color-scheme"].forEach(
        (x) => { x.addEventListener("change", toggleColorScheme) }
    );
    document.forms.settings.elements["font-size"].addEventListener("change", changeFont);
    document.forms.settings.elements["font-family"].forEach(
        (x) => { x.addEventListener("change", changeFontFamily) }
    );
    document.forms.settings.elements.speech.addEventListener("change", (x) => {
        activityLog("speech on")
    });
})
