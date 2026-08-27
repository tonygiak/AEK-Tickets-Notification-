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
    "Accept-Language": "el-GR,el;q=0.9,en;q=0.8",
}


def main():
    resp = requests.get(URL, headers=HEADERS, timeout=30)
    print("status:", resp.status_code)
    print("final url:", resp.url)
    print("content-type:", resp.headers.get("content-type"))
    print("length:", len(resp.text))

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
