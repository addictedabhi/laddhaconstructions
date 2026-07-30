"""Measure the real rendered homepage hero at desktop and mobile widths.

Serves the site, screenshots the hero, and asserts it is actually bright and
that hero text still passes AA against the pixels behind it.

Run from the repo root:  python tools/check_hero_rendered.py
Exits non-zero if the rendered hero is too dark or contrast fails.
"""
import http.server
import pathlib
import re
import socketserver
import sys
import threading

from PIL import Image, ImageStat
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from check_hero_contrast import contrast_ratio, srgb_relative_luminance

ROOT = pathlib.Path(__file__).resolve().parent.parent
PORT = 8771
SHOTS = ROOT / "docs" / "superpowers" / "plans" / "hero-shots"

# The old hero rendered far darker than this. A bright hero must clear it.
MIN_RENDERED_MEAN = 90.0
AA_NORMAL = 4.5
VIEWPORTS = [("desktop", 1440, 900), ("mobile", 390, 844)]

# The header is fixed and the home hero pins its copy to the bottom, so a short
# window used to slide the kicker underneath it. These heights are deliberately
# cramped - they are where that regression showed up.
OVERLAP_VIEWPORTS = [
    ("desktop-short", 1440, 620),
    ("laptop-short", 1280, 560),
    ("mobile-short", 390, 560),
    ("small", 360, 480),
]


def serve():
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(ROOT), **k
    )
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main():
    SHOTS.mkdir(parents=True, exist_ok=True)
    httpd = serve()
    failures = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for name, w, h in VIEWPORTS:
                page = browser.new_page(viewport={"width": w, "height": h})
                errors = []
                page.on(
                    "console",
                    lambda m: errors.append(m.text) if m.type == "error" else None,
                )
                page.goto(f"http://127.0.0.1:{PORT}/", wait_until="load")
                # Let the slow hero animation and reveal settle.
                page.wait_for_timeout(4000)

                shot = SHOTS / f"hero-{name}.png"
                page.locator("section.hero--home").screenshot(path=str(shot))

                img = Image.open(shot).convert("L")
                iw, ih = img.size
                mean = ImageStat.Stat(img).mean[0]

                # Top third: the sky. This is what should read bright.
                sky = ImageStat.Stat(img.crop((0, 0, iw, ih // 3))).mean[0]
                # Bottom-left: where the hero copy sits.
                text_zone = img.crop((0, int(ih * 0.55), int(iw * 0.62), ih))
                tz = ImageStat.Stat(text_zone).mean[0]
                ratio = contrast_ratio(
                    srgb_relative_luminance(255), srgb_relative_luminance(tz)
                )

                print(f"[{name} {w}x{h}]")
                print(
                    f"  overall mean luminance : {mean:6.1f} (needs >= {MIN_RENDERED_MEAN})"
                )
                print(f"  sky (top third)        : {sky:6.1f}")
                print(f"  text zone              : {tz:6.1f}")
                print(
                    f"  white text contrast    : {ratio:6.2f}:1 (AA needs {AA_NORMAL})"
                )
                print(f"  screenshot             : {shot.relative_to(ROOT)}")

                # The kicker is small accent-coloured text high in the frame,
                # over sky rather than the dark foreground the h1 sits on. The
                # overall numbers pass while it is unreadable, so it needs its
                # own guard: either a real scrim or a shadow behind the glyphs.
                css = (ROOT / "assets" / "css" / "site.css").read_text(
                    encoding="utf-8"
                )
                kicker_rule = re.search(
                    r"\n\.hero-kicker \{(.*?)\}", css, re.S
                ).group(1)
                if "text-shadow" not in kicker_rule:
                    failures.append(
                        "hero kicker has no text-shadow - accent-300 measures "
                        "2.6:1 over the bright sky and no tint in the ramp "
                        "clears AA on that ground"
                    )

                if mean < MIN_RENDERED_MEAN:
                    failures.append(
                        f"{name}: rendered mean {mean:.1f} below {MIN_RENDERED_MEAN}"
                    )
                if ratio < AA_NORMAL:
                    failures.append(
                        f"{name}: hero text contrast {ratio:.2f}:1 below AA"
                    )
                if errors:
                    failures.append(f"{name}: console errors {errors}")
                page.close()

            # Squeeze the viewport and check the hero copy still clears the
            # fixed header. Brightness and contrast both pass while the kicker
            # is hidden behind it, so this needs its own geometry check.
            print()
            for name, w, h in OVERLAP_VIEWPORTS:
                page = browser.new_page(viewport={"width": w, "height": h})
                page.goto(f"http://127.0.0.1:{PORT}/", wait_until="load")
                page.wait_for_timeout(3600)
                header_bottom = page.evaluate(
                    "document.querySelector('.site-header')"
                    ".getBoundingClientRect().bottom"
                )
                kicker_top = page.evaluate(
                    "document.querySelector('.hero-kicker')"
                    ".getBoundingClientRect().top"
                )
                gap = kicker_top - header_bottom
                print(
                    f"[{name} {w}x{h}] header/kicker gap: {gap:6.0f}px "
                    f"{'ok' if gap >= 0 else 'OVERLAP'}"
                )
                if gap < 0:
                    failures.append(
                        f"{name}: hero kicker sits {abs(gap):.0f}px under the "
                        f"fixed header"
                    )
                page.close()

            browser.close()
    finally:
        httpd.shutdown()

    print()
    if failures:
        print("FAIL:")
        for f in failures:
            print(f"  {f}")
        return 1
    print("PASS - hero renders bright at every viewport and text passes AA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
