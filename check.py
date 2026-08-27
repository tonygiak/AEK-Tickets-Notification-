"""
Diagnostic pass (Playwright): render the AEK ticketmaster.gr listing page
with a real headless browser and dump what we actually get back, so the
detection logic can be written against real markup instead of guesses.
"""
from playwright.sync_api import sync_playwright

URL = "https://www.ticketmaster.gr/aek/showProductList.html"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
            locale="el-GR",
            viewport={"width": 1280, "height": 900},
        )
        page = context.new_page()

        print("navigating to homepage...")
        page.goto("https://www.ticketmaster.gr/", wait_until="networkidle", timeout=45000)
        print("homepage title:", page.title())

        print("navigating to AEK listing page...")
        resp = page.goto(URL, wait_until="networkidle", timeout=45000)
        print("status:", resp.status if resp else None)
        page.wait_for_timeout(3000)  # let any client-side rendering settle

        html = page.content()
        text = page.inner_text("body")

        with open("page_dump.html", "w", encoding="utf-8") as f:
            f.write(html)
        with open("page_dump.txt", "w", encoding="utf-8") as f:
            f.write(text)

        print("title:", page.title())
        print("html length:", len(html))
        print("visible text length:", len(text))
        print("visible text (first 3000 chars):")
        print(text[:3000])

        lower = (html + text).lower()
        for needle in [
            "real madrid",
            "ρεαλ μαδριτ",
            "aek",
            "sold out",
            "εξαντλ",
            "no events",
            "δεν υπάρχ",
            "buy",
            "αγορ",
            "identity verified",
        ]:
            print(f"contains {needle!r}:", needle in lower)

        browser.close()


if __name__ == "__main__":
    main()
