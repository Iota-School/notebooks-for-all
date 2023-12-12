"""accessibility auditing tools."""
import asyncio
import os
import traceback
from contextlib import AsyncExitStack, asynccontextmanager
from json import dumps
from logging import getLogger
from pathlib import Path
from typing import List, Optional

import playwright.async_api
import requests

logger = getLogger("a11y-tasks")

ENV_CHROMIUM_CHANNEL = "NBA11Y_CHROMIUM_CHANNEL"
DEFAULT_CHROMIUM_CHANNEL = "chrome-beta"


async def _main(
    ids: list,
    headless: bool = True,
    tasks=None,
    output: Path = Path("docs/data"),
    cache: bool = True,
):
    if tasks is None:
        tasks = []
    if cache:
        import requests_cache

        requests_cache.install_cache(__name__)

    for id in ids:
        async with playwright.async_api.async_playwright() as play:
            browser = await play.chromium.launch(
                args=['--enable-blink-features="AccessibilityObjectModel"'],
                headless=True,
                channel=get_chrome_channel(),
            )

            page = await browser.new_page()
            await page.goto(Path(id).absolute().as_uri())
            for task in tasks:
                await task(browser, page, output)


def get_chrome_channel():
    return os.environ.get(ENV_CHROMIUM_CHANNEL, DEFAULT_CHROMIUM_CHANNEL)


@asynccontextmanager
async def get_browser():
    async with playwright.async_api.async_playwright() as play:
        yield await play.chromium.launch(
            args=['--enable-blink-features="AccessibilityObjectModel"'],
            headless=True,
            channel=get_chrome_channel(),
        )


@asynccontextmanager
async def get_page(browser, id):
    page = await browser.new_page()
    await page.goto(Path(id).absolute().as_uri())
    yield page


async def test_axe_one(file: Path, browser=None, **config):
    async with AsyncExitStack() as stack:
        if browser is None:
            browser = stack.enter_async_context(get_browser())
        async with get_page(browser, file) as page:
            config.setdefault("runOnly", ["best-practice", "wcag22aa", "wcag2aaa"])
            config.setdefault("allowedOrigins", ["<same_origin>"])
            logger.info(f"inject axe {page.url}")
            await page.evaluate(requests.get("https://cdn.jsdelivr.net/npm/axe-core").text)
            logger.info(f"running axe tests {page.url}")
            try:
                return await page.evaluate(f"window.axe.run(window.document, {dumps(config)})")
            except BaseException as e:
                # this is gonna mess with someone eventually

                logger.error(f"AXE FAILED {page.url}")
                traceback.print_exception(type(e), e, e.__traceback__)


async def _audit_one(file: Path, browser=None, output=None, **config):
    async with AsyncExitStack() as stack:
        if browser is None:
            browser = await stack.enter_async_context(get_browser())
        results = await test_axe_one(file, browser)
        if output is None:
            output = file.parent / "audit" / file.name
        _write_json(output, results)


def audit_one(file, output=None):
    return asyncio.run(_audit_one(file, output=output))


def _write_json(file: Path, data):
    logger.info(f"writing data to {file}")
    file.parent.mkdir(parents=True, exist_ok=True)
    file.with_suffix(".json").write_text(dumps(data, indent=2))


async def _main(ids: list, headless: bool = True, output: Path = "audit", cache: bool = True):
    if cache:
        import requests_cache

        requests_cache.install_cache(__name__)

    async with get_browser() as browser:
        for id in ids:
            await _audit_one(Path(id), browser)


def main(file: Optional[List[str]] = None, dir: Path = "audit"):
    """Audit notebooks."""
    import asyncio

    if file is None:
        file = ["tests/notebooks/lorenz.ipynb"]
    asyncio.run(_main(ids=file, output=dir))


if __name__ == "__main__":
    import typer

    typer.run(main)
