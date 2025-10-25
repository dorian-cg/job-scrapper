import argparse
import asyncio
import json
from playwright.async_api import async_playwright


def clean_str(s: str) -> str:
    return s.strip()


async def get_microsoft_job_details(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state("networkidle")

        title = await page.locator(".SearchJobDetailsCard h1").first.text_content()

        location = await page.locator(
            ".SearchJobDetailsCard > div:nth-child(3)"
        ).first.text_content()

        date_posted = await page.locator(
            ".SearchJobDetailsCard > div:nth-child(5) > div > div > div:nth-child(2)"
        ).first.text_content()

        overview = await page.locator(
            ".SearchJobDetailsCard > div:nth-child(7) > div:nth-child(1) > div > div"
        ).first.text_content()

        required_qualifications = []
        required_qualifications_list = await page.locator(
            ".SearchJobDetailsCard > div:nth-child(7) > div:nth-child(2) > div > div > ul:last-of-type > li"
        ).all()
        for item in required_qualifications_list:
            required_qualifications.append(await item.text_content())

        preferred_qualifications = []
        preferred_qualifications_list = await page.locator(
            ".SearchJobDetailsCard > div:nth-child(7) > div:nth-child(2) > div > div > ul:first-of-type > li"
        ).all()
        for item in preferred_qualifications_list:
            preferred_qualifications.append(await item.text_content())

        responsibilities = []
        responsibilities_list = await page.locator(
            ".SearchJobDetailsCard > div:nth-child(7) > div:nth-child(3) ul > li"
        ).all()
        for item in responsibilities_list:
            responsibilities.append(await item.text_content())

        result = {
            "title": clean_str(title),
            "location": clean_str(location),
            "date_posted": clean_str(date_posted),
            "overview": clean_str(overview),
            "required_qualifications": [clean_str(q) for q in required_qualifications],
            "preferred_qualifications": [
                clean_str(q) for q in preferred_qualifications
            ],
            "responsibilities": [clean_str(r) for r in responsibilities],
        }

        await browser.close()

        return result


async def main(args):
    job_details = await get_microsoft_job_details(args.url)
    print(json.dumps(job_details, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Microsoft Job Details Scraper")
    parser.add_argument(
        "--url", type=str, required=True, help="The URL of the job listing."
    )
    asyncio.run(main(parser.parse_args()))
