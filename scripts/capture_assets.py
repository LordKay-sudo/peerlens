"""
Capture PeerLens UI screenshots and demo GIF for docs/assets.
Requires: pip install playwright && playwright install chromium
Run with API + web servers already up (prefer production: npm run build && npm start).
"""
from __future__ import annotations

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

import os

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
FRAMES = ASSETS / "frames"
BASE_URL = os.environ.get("PEERLENS_WEB_URL", "http://localhost:3001")


async def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    FRAMES.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        page.set_default_timeout(60_000)

        await page.goto(BASE_URL, wait_until="networkidle")
        await page.wait_for_timeout(1200)
        await page.screenshot(path=ASSETS / "hero.png")

        await page.locator("#analyze").scroll_into_view_if_needed()
        await page.wait_for_timeout(600)
        await page.screenshot(path=ASSETS / "analyze-empty.png")

        input_box = page.get_by_placeholder("10.1038/nature12373")
        await input_box.fill("2301.07041")
        await page.screenshot(path=FRAMES / "01-input-filled.png")

        await page.get_by_role("button", name="Run", exact=True).click()
        await page.wait_for_timeout(600)
        await page.screenshot(path=FRAMES / "02-analyzing.png")

        await page.get_by_text("Quality report").wait_for(state="visible")
        await page.wait_for_timeout(1200)
        await page.screenshot(path=ASSETS / "report.png", full_page=True)

        await page.locator("#analyze").scroll_into_view_if_needed()
        await page.wait_for_timeout(400)
        await page.screenshot(path=FRAMES / "03-report-view.png")

        for index, offset in enumerate(range(4, 10), start=4):
            await page.mouse.wheel(0, 280)
            await page.wait_for_timeout(350)
            await page.screenshot(path=FRAMES / f"{index:02d}-scroll.png")

        await browser.close()

    print(f"Saved screenshots to {ASSETS}")


if __name__ == "__main__":
    asyncio.run(main())
