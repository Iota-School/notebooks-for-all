"""accessibility auditing tools"""
from pathlib import Path
from contextlib import asynccontextmanager
import requests
import playwright.async_api
from typing import List
import traceback
async def _main(ids:list, headless:bool =True, tasks=[],  output: Path=Path("docs/data"), cache:bool=True):


        if cache:
            import requests_cache
            requests_cache.install_cache(__name__)

        for id in ids:
            async with playwright.async_api.async_playwright() as play:
                browser = await play.chromium.launch(
                    args=['--enable-blink-features="AccessibilityObjectModel"'],
                    headless=True,  channel="chrome-beta")

                page = await browser.new_page()
                await page.goto(Path(id).absolute().as_uri())
                for task in tasks:
                    await task(browser, page, output)

async def test_axe(browser, page, output, **config):
    from json import dumps

    config.setdefault("runOnly", "best-practice")
    config.setdefault("allowedOrigins", ["<same_origin>"])
    print(F"inject axe {page.url}")
    await page.evaluate(requests.get("https://unpkg.com/axe-core").text)
    print(F"running axe tests {page.url}")
    try:
        axe = await page.evaluate(F"window.axe.run(window.document, {dumps(config)})")
    except BaseException as e:
        # this is gonna mess with someone eventually
        
        print(F"AXE FAILED {page.url}")
        traceback.print_exception(type(e), e, e.__traceback__)

    else:
        print(F"writing axe violations for {page.url}")
        target = Path(page.url[len("file://"):])
        data = output / target.name
        data.parent.mkdir(exist_ok=True, parents=True)
        data = data.with_suffix(data.suffix + ".json")
        data.write_text(dumps(axe["violations"], sort_keys=True, indent=4))



def main(id: List[str]=["tests/notebooks/lorenz.ipynb"], output_dir: Path=Path("docs/data")):
    import asyncio
    asyncio.run(_main(ids=id, tasks=[test_axe], output=output_dir))
    

if __name__ == "__main__":
    import typer
    typer.run(main)