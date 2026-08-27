"""
Diagnostic pass: fetch the AEK ticketmaster.gr listing page and dump what we
actually get back, so the detection logic can be written against real
markup instead of guesses. Run via the 'diagnose' workflow_dispatch input.
"""
import os

import requests

URL = "https://www.ticketmaster.gr/aek/showProductList.html"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "el-GR,el;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.ticketmaster.gr/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Upgrade-Insecure-Requests": "1",
}


def main():
    session = requests.Session()
    session.headers.update(HEADERS)
    home = session.get("https://www.ticketmaster.gr/", timeout=30)
    print("homepage status:", home.status_code, "len:", len(home.text))

    resp = session.get(URL, timeout=30)
    print("status:", resp.status_code)
    print("final url:", resp.url)
    print("content-type:", resp.headers.get("content-type"))
    print("length:", len(resp.text))
    print("headers:", dict(resp.headers))
    print("body:", repr(resp.text))

    html = resp.text
    with open("page_dump.html", "w", encoding="utf-8") as f:
        f.write(html)

    lower = html.lower()
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
    ]:
        print(f"contains {needle!r}:", needle in lower)


if __name__ == "__main__":
    main()
