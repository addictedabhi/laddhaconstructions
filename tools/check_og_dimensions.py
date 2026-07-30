"""Assert every page's declared og:image dimensions match the real file.

Run from the repo root:  python tools/check_og_dimensions.py
Exits non-zero on any mismatch.
"""
import pathlib
import re
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = [
    "index.html",
    "about.html",
    "ongoing-projects.html",
    "completed-projects.html",
    "capability.html",
    "contact.html",
    "coming-soon.html",
]


def declared(html):
    """Pull og:image url plus declared width and height out of a page."""
    url = re.search(r'<meta property="og:image" content="(.*?)"', html).group(1)
    w = int(re.search(r'<meta property="og:image:width" content="(\d+)"', html).group(1))
    h = int(re.search(r'<meta property="og:image:height" content="(\d+)"', html).group(1))
    return url, w, h


def main():
    failures = []
    for page in PAGES:
        html = (ROOT / page).read_text(encoding="utf-8")
        url, dw, dh = declared(html)
        rel = url.split("laddhaconstructions.com/", 1)[1]
        real = Image.open(ROOT / rel).size
        status = "ok" if real == (dw, dh) else "MISMATCH"
        if real != (dw, dh):
            failures.append(f"{page}: {rel} is {real}, declared ({dw}, {dh})")
        print(f"{page:26} {rel:28} real={str(real):12} declared=({dw}, {dh}) {status}")

    print()
    if failures:
        print(f"FAIL - {len(failures)} page(s) declare wrong og:image dimensions:")
        for f in failures:
            print(f"  {f}")
        return 1
    print("PASS - every page declares its real og:image dimensions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
