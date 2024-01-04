/**
 * @jest-environment jsdom
 */

const fs = require('node:fs');
const { virtual } = require("@guidepup/virtual-screen-reader");


test("should match the snapshot of expected screen reader spoken phrases", async () => {
    document.body.innerHTML = fs.readFileSync("tests/exports/html/lorenz-executed-default.html", "utf-8");
    await virtual.start({ container: document.body })
    var phrases = [];
    while ((await virtual.lastSpokenPhrase()) !== "end of document") {
        await virtual.next();
        phrases.push({node: virtual.activeNode, phrases: await virtual.lastSpokenPhrase()})
    };
    console.log(phrases)
}, 60000);