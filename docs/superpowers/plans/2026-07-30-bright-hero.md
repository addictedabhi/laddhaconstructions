# Bright Industrial Hero Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the dark night-shot homepage hero with a bright industrial photograph, and lighten the scrim so the image actually reads as bright.

**Architecture:** Three independent changes to a static site — the hero image and its alt text in `index.html`, the `.hero--home` scrim/filter/crop rules in `assets/css/site.css`, and the homepage Open Graph image in `tools-seo.py` (which regenerates the `<!-- seo:start -->` block on every page). Each is verified by a Python measurement script that reads real rendered pixels rather than by inspection.

**Tech Stack:** Static HTML/CSS. Python 3 with Pillow for image measurement, Playwright (Chromium) for rendered screenshots. `python -m http.server` for local serving. No build step, no framework.

## Global Constraints

- Design source of truth: `docs/superpowers/specs/2026-07-30-bright-hero-design.md`.
- New hero image is `assets/photo-p7-1.jpg` (1264×500, mean luminance 139.0). Do not source, download or generate any new image.
- New `.hero--home` scrim is exactly `linear-gradient(180deg, rgba(18,17,15,0) 0%, rgba(18,17,15,.08) 40%, rgba(18,17,15,.52) 100%)`.
- White hero text must measure at least 4.5:1 contrast against the scrimmed image (WCAG AA).
- Do NOT change `capability.html`. It keeps `photo-p7-1.jpg`; the repetition is a deliberate, documented decision.
- Do NOT change hero copy: the kicker, `h1`, lede and buttons stay exactly as written.
- Do NOT change animation timings. `kb 38s cubic-bezier(.4,0,.2,1) both` on the home hero and the `fadeUp` delay sequence are an explicit client request ("slow") and must be preserved verbatim.
- Do NOT change `.hero--sub` or `.hero--contact` rules. Only `.hero--home` selectors are in scope.
- The `<!-- seo:start -->`…`<!-- seo:end -->` block in every HTML file is generated. Never hand-edit it — change `tools-seo.py` and re-run it.
- Never use `New-Item -Force` on an existing file (truncates it). Use the Write/Edit tools.
- Commit after each task.

---

### Task 1: Per-page Open Graph image dimensions

`tools-seo.py` declares one global `OG_IMG_W, OG_IMG_H = 1080, 607` for every page, but the seven pages reference images of five different sizes. Five of seven pages currently declare wrong dimensions — `photo-p12-1.jpg` is really 297×170 but is declared 1080×607, a 3.6× misdeclaration that is also below Facebook's 200px minimum.

The spec requires the homepage's dimensions to be correct once its image changes. Fixing only the homepage would leave the identical bug on five pages, so dimensions are derived per-page from the actual file. This must land before Task 3 changes the homepage image.

**Files:**
- Create: `tools/check_og_dimensions.py`
- Modify: `tools-seo.py:17` (remove the `OG_IMG_W, OG_IMG_H` global), `tools-seo.py:267-268` (emit per-page values)
- Regenerates: all seven `*.html` files

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `image_size(repo_root: pathlib.Path, rel_path: str) -> tuple[int, int]` in `tools-seo.py`, returning the real `(width, height)` of an image under the repo root. Task 3 relies on this so that changing the homepage image automatically corrects its declared dimensions.

- [ ] **Step 1: Write the failing test**

Create `tools/check_og_dimensions.py`:

```python
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


def declared(html: str) -> tuple[str, int, int]:
    """Pull og:image url plus declared width and height out of a page."""
    url = re.search(r'<meta property="og:image" content="(.*?)"', html).group(1)
    w = int(re.search(r'<meta property="og:image:width" content="(\d+)"', html).group(1))
    h = int(re.search(r'<meta property="og:image:height" content="(\d+)"', html).group(1))
    return url, w, h


def main() -> int:
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python tools/check_og_dimensions.py`

Expected: exit code 1, `FAIL - 5 page(s) declare wrong og:image dimensions`, listing `about.html` (1280×720), `ongoing-projects.html` (685×911), `completed-projects.html` (1080×650), `capability.html` (1264×500) and `contact.html` (297×170).

- [ ] **Step 3: Write minimal implementation**

In `tools-seo.py`, delete this line (line 17):

```python
OG_IMG_W, OG_IMG_H = 1080, 607
```

and put this in its place:

```python
def image_size(repo_root, rel_path):
    """Real pixel size of an image in the repo.

    Open Graph dimensions were previously a single global, so pages whose
    image was not 1080x607 advertised a size the file did not have. Reading
    the file keeps the declaration honest when an image is swapped.
    """
    from PIL import Image

    with Image.open(repo_root / rel_path) as im:
        return im.size
```

Then in `build_block`, replace lines 267-268:

```python
    lines.append(f'<meta property="og:image:width" content="{OG_IMG_W}">')
    lines.append(f'<meta property="og:image:height" content="{OG_IMG_H}">')
```

with:

```python
    og_w, og_h = image_size(ROOT, cfg["img"])
    lines.append(f'<meta property="og:image:width" content="{og_w}">')
    lines.append(f'<meta property="og:image:height" content="{og_h}">')
```

- [ ] **Step 4: Regenerate the pages and run the test to verify it passes**

Run: `python tools-seo.py && python tools/check_og_dimensions.py`

Expected: `tools-seo.py` prints seven lines, then `PASS - every page declares its real og:image dimensions`, exit code 0.

- [ ] **Step 5: Commit**

```bash
git add tools-seo.py tools/check_og_dimensions.py index.html about.html ongoing-projects.html completed-projects.html capability.html contact.html coming-soon.html
git commit -m "fix(seo): derive og:image dimensions from the real file

A single global declared every page's og:image as 1080x607, so the five
pages using a different image advertised a size the file did not have -
contact.html declared 1080x607 for an image that is really 297x170.

Reading the file keeps the declaration correct when an image is swapped."
```

---

### Task 2: Lighten the home hero scrim and remove the night-shot filter

The `.hero--home` scrim runs to 88% black at the foot and starts at 62% over the sky. `filter: saturate(.82)` was tuned for the night photograph and would mute the new blue sky.

Measured on the incoming image: the bottom-left text zone has mean luminance 108.2, so white text is already 5.23:1 — passing AA before any scrim. The new gradient is therefore for robustness, not rescue.

This task changes CSS only. The homepage still shows the dark image until Task 3, so the visible result mid-task is the dark photo under a light scrim. That is expected.

**Files:**
- Create: `tools/check_hero_contrast.py`
- Modify: `assets/css/site.css:99-102` (filter), `assets/css/site.css:107-109` (scrim)

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `contrast_ratio(fg_luma: float, bg_luma: float) -> float` and `srgb_relative_luminance(value_0_255: float) -> float` in `tools/check_hero_contrast.py`. Task 4 imports both to check contrast against the rendered screenshot.

- [ ] **Step 1: Write the failing test**

Create `tools/check_hero_contrast.py`:

```python
"""Assert the home hero scrim is light and hero text still passes WCAG AA.

Composites the declared scrim over the real hero image and measures the
contrast of white text against the text zone.

Run from the repo root:  python tools/check_hero_contrast.py
Exits non-zero if the scrim is too heavy or contrast falls below AA.
"""
import pathlib
import re
import sys

from PIL import Image, ImageStat

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "css" / "site.css"
HERO = ROOT / "assets" / "photo-p7-1.jpg"

# WCAG 2.1 minimum for normal-size text.
AA_NORMAL = 4.5
# The top of the gradient must be effectively clear, or the sky is not bright.
MAX_TOP_ALPHA = 0.10
# Cap the foot of the gradient so the photograph stays visible.
MAX_BOTTOM_ALPHA = 0.60


def srgb_relative_luminance(value_0_255):
    """Relative luminance of a greyscale sRGB value, per WCAG 2.1."""
    c = value_0_255 / 255
    c = c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return c


def contrast_ratio(fg_luma, bg_luma):
    """WCAG contrast ratio between two relative luminances."""
    lighter, darker = max(fg_luma, bg_luma), min(fg_luma, bg_luma)
    return (lighter + 0.05) / (darker + 0.05)


def home_scrim_alphas():
    """The three rgba alphas of the .hero--home scrim, in gradient order."""
    css = CSS.read_text(encoding="utf-8")
    block = re.search(
        r"\.hero--home \.hero-scrim \{(.*?)\}", css, re.S
    ).group(1)
    return [float(a) for a in re.findall(r"rgba\(18,17,15,([\d.]+)\)", block)]


def main():
    alphas = home_scrim_alphas()
    print(f"scrim alphas (top -> bottom): {alphas}")
    if len(alphas) != 3:
        print(f"FAIL - expected 3 gradient stops, found {len(alphas)}")
        return 1

    top, mid, bottom = alphas
    failures = []
    if top > MAX_TOP_ALPHA:
        failures.append(f"top alpha {top} exceeds {MAX_TOP_ALPHA} - sky is dimmed")
    if bottom > MAX_BOTTOM_ALPHA:
        failures.append(
            f"bottom alpha {bottom} exceeds {MAX_BOTTOM_ALPHA} - photo is hidden"
        )

    # Hero copy sits bottom-left. Measure that region of the real image.
    img = Image.open(HERO).convert("L")
    w, h = img.size
    zone = img.crop((0, int(h * 0.55), int(w * 0.62), h))
    zone_mean = ImageStat.Stat(zone).mean[0]
    effective = zone_mean * (1 - bottom)
    ratio = contrast_ratio(
        srgb_relative_luminance(255), srgb_relative_luminance(effective)
    )
    print(f"text zone mean luminance: {zone_mean:.1f}")
    print(f"after {bottom} scrim:      {effective:.1f}")
    print(f"white text contrast:      {ratio:.2f}:1 (AA needs {AA_NORMAL})")

    if ratio < AA_NORMAL:
        failures.append(f"contrast {ratio:.2f}:1 is below AA ({AA_NORMAL})")

    css = CSS.read_text(encoding="utf-8")
    home_img_rule = re.search(
        r"\.hero--home \.hero-frame img \{(.*?)\}", css, re.S
    ).group(1)
    if "saturate" in home_img_rule:
        failures.append("home hero image still has a saturate() filter")
    if "kb 38s cubic-bezier(.4,0,.2,1) both" not in home_img_rule:
        failures.append("home hero animation timing was changed - must stay 38s")

    print()
    if failures:
        print("FAIL:")
        for f in failures:
            print(f"  {f}")
        return 1
    print("PASS - scrim is light, sky is clear, text passes AA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python tools/check_hero_contrast.py`

Expected: exit code 1, reporting `scrim alphas (top -> bottom): [0.62, 0.36, 0.88]`, `top alpha 0.62 exceeds 0.1 - sky is dimmed`, `bottom alpha 0.88 exceeds 0.6 - photo is hidden`, and `home hero image still has a saturate() filter`.

- [ ] **Step 3: Write minimal implementation**

In `assets/css/site.css`, replace lines 99-102:

```css
.hero--home .hero-frame img {
  filter: saturate(.82) contrast(1.03);
  animation: kb 38s cubic-bezier(.4,0,.2,1) both;
}
```

with:

```css
.hero--home .hero-frame img {
  /* No filter here. The saturate(.82) this replaces was tuned for the night
     photograph it used to carry and would mute the daylight sky. */
  animation: kb 38s cubic-bezier(.4,0,.2,1) both;
}
```

Then replace lines 107-109:

```css
.hero--home .hero-scrim {
  background: linear-gradient(180deg, rgba(18,17,15,.62) 0%, rgba(18,17,15,.36) 42%, rgba(18,17,15,.88) 100%);
}
```

with:

```css
/* The hero photograph carries its own gradient - sky about 203, foreground
   about 84 - so white copy over the bottom-left text zone already measures
   5.2:1 unaided. This scrim is insurance against a future image, not a
   rescue: clear across the sky, gentle only behind the copy. */
.hero--home .hero-scrim {
  background: linear-gradient(180deg, rgba(18,17,15,0) 0%, rgba(18,17,15,.08) 40%, rgba(18,17,15,.52) 100%);
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python tools/check_hero_contrast.py`

Expected: exit code 0, `scrim alphas (top -> bottom): [0.0, 0.08, 0.52]`, `white text contrast: 12.42:1`, then `PASS - scrim is light, sky is clear, text passes AA`.

- [ ] **Step 5: Commit**

```bash
git add assets/css/site.css tools/check_hero_contrast.py
git commit -m "style(hero): lighten the home scrim and drop the night-shot filter

The scrim ran to 88% black at the foot and 62% over the sky, so a bright
image would still read dark. The photograph carries its own gradient and
white copy measures 5.2:1 over the text zone unaided, so the scrim only
needs to be insurance: clear at the top, .52 behind the copy (12.4:1).

Also drops saturate(.82), which was tuned for the night photograph and
would mute a daylight sky."
```

---

### Task 3: Swap the hero image and fix the mobile crop

The source is 2.53:1 but the home hero is `100svh`. Measured `object-fit: cover` behaviour: desktop 1440×900 keeps 63% of the width, but mobile 390×844 keeps only **18%** — a narrow centre strip that crops out the silos and conveyor gallery entirely.

`object-position` biased left of centre holds the silo cluster in frame, and a shorter hero on narrow viewports reduces how hard the crop bites.

**Files:**
- Modify: `index.html:142` (hero `img` src and alt), `assets/css/site.css:99-102` (add `object-position`), `assets/css/site.css:533` (mobile hero height), `tools-seo.py:41-42` (homepage OG image)
- Regenerates: all seven `*.html` files

**Interfaces:**
- Consumes: `image_size()` from Task 1, which makes the OG dimensions follow the new image automatically. The scrim from Task 2 is what makes the swapped image read as bright.
- Produces: nothing consumed by later tasks.

- [ ] **Step 1: Write the failing test**

Create `tools/check_hero_image.py`:

```python
"""Assert the homepage hero uses the bright image, everywhere it should.

Checks the visible <img>, the Open Graph image, and that the CSS carries an
object-position so the silos survive the mobile crop.

Run from the repo root:  python tools/check_hero_image.py
Exits non-zero on any mismatch.
"""
import pathlib
import re
import sys

from PIL import Image, ImageStat

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXPECTED = "assets/photo-p7-1.jpg"
# The old night shot measured 33.9. Anything this dark is not a bright hero.
MIN_MEAN_LUMINANCE = 100.0


def main():
    failures = []
    html = (ROOT / "index.html").read_text(encoding="utf-8")

    hero = re.search(
        r'<section class="hero hero--home">.*?<img src="(.*?)" alt="(.*?)"',
        html,
        re.S,
    )
    if hero is None:
        print("FAIL - could not find the home hero <img>")
        return 1
    src, alt = hero.group(1), hero.group(2)
    print(f"hero src: {src}")
    print(f"hero alt: {alt}")
    if src != EXPECTED:
        failures.append(f"hero src is {src}, expected {EXPECTED}")
    if "night" in alt.lower():
        failures.append(f"alt text still describes a night scene: {alt!r}")

    img = Image.open(ROOT / src).convert("L")
    mean = ImageStat.Stat(img).mean[0]
    print(f"hero image mean luminance: {mean:.1f} (needs >= {MIN_MEAN_LUMINANCE})")
    if mean < MIN_MEAN_LUMINANCE:
        failures.append(f"hero image mean luminance {mean:.1f} is too dark")

    og = re.search(r'<meta property="og:image" content="(.*?)"', html).group(1)
    print(f"og:image: {og}")
    if not og.endswith(EXPECTED.split("/")[-1]):
        failures.append(f"og:image is {og}, expected it to end with {EXPECTED}")

    css = (ROOT / "assets" / "css" / "site.css").read_text(encoding="utf-8")
    home_img_rule = re.search(
        r"\.hero--home \.hero-frame img \{(.*?)\}", css, re.S
    ).group(1)
    if "object-position" not in home_img_rule:
        failures.append(
            "no object-position on the home hero - at 390px wide only 18% of "
            "the image width survives the crop and the silos are lost"
        )

    print()
    if failures:
        print("FAIL:")
        for f in failures:
            print(f"  {f}")
        return 1
    print("PASS - homepage hero is the bright industrial image")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python tools/check_hero_image.py`

Expected: exit code 1, showing `hero src: assets/photo-p6-1.jpg`, `hero image mean luminance: 33.9`, and failures for the wrong src, the night alt text, the too-dark image, the wrong og:image and the missing object-position.

- [ ] **Step 3: Write minimal implementation**

In `index.html` line 142, replace:

```html
      <img src="assets/photo-p6-1.jpg" alt="Night view of a flyover corridor at Kota">
```

with:

```html
      <img src="assets/photo-p7-1.jpg" alt="Cement plant at Kota with silos and conveyor gallery under a bright sky">
```

In `tools-seo.py`, in the `"index.html"` entry (lines 41-42), replace:

```python
        img="assets/photo-p6-1.jpg",
        img_alt="Night view of a flyover corridor at Kota, Rajasthan",
```

with:

```python
        img="assets/photo-p7-1.jpg",
        img_alt="Cement plant at Kota with silos and conveyor gallery under a bright sky",
```

In `assets/css/site.css`, replace the `.hero--home .hero-frame img` rule from Task 2 with:

```css
.hero--home .hero-frame img {
  /* No filter here. The saturate(.82) this replaces was tuned for the night
     photograph it used to carry and would mute the daylight sky. */
  /* The source is 2.53:1 against a 100svh hero, so cover() crops the sides
     hard - at 390px wide only 18% of the width survives. Biasing left of
     centre keeps the silo cluster in frame instead of a blank middle strip. */
  object-position: 38% center;
  animation: kb 38s cubic-bezier(.4,0,.2,1) both;
}
```

In `assets/css/site.css` line 533, inside the `@media (max-width: 860px)` block, replace:

```css
  .hero--home { min-height: 540px; }
```

with:

```css
  /* A shorter hero on narrow screens means a less punishing side crop. */
  .hero--home { height: 72svh; min-height: 460px; }
```

- [ ] **Step 4: Regenerate the pages and run the test to verify it passes**

Run: `python tools-seo.py && python tools/check_hero_image.py && python tools/check_og_dimensions.py`

Expected: `check_hero_image.py` prints `hero src: assets/photo-p7-1.jpg`, `hero image mean luminance: 139.0`, then `PASS - homepage hero is the bright industrial image`. `check_og_dimensions.py` still passes, with `index.html` now declaring 1264×500.

- [ ] **Step 5: Commit**

```bash
git add index.html assets/css/site.css tools-seo.py tools/check_hero_image.py about.html ongoing-projects.html completed-projects.html capability.html contact.html coming-soon.html
git commit -m "feat(hero): use the bright cement-plant photo on the homepage

The homepage opened on a night shot with mean luminance 33.9 and crushed
blacks. Swaps in the Mangalam Cement plant - mean 139.0, blue sky, silos
and conveyor towers - which is also the firm's own completed work.

The source is 2.53:1 against a 100svh hero, so cover() keeps only 18% of
the width at 390px. object-position: 38% holds the silos in frame and the
hero is shorter on narrow screens. The homepage og:image follows, so a
shared link no longer previews a dark image the page does not show."
```

---

### Task 4: Verify the rendered result at desktop and mobile

The preceding tasks assert on source files. This one asserts on what a browser actually paints — the measurement that matters, and the one the spec flagged as highest-risk. `object-position: 38%` from Task 3 is a starting value, to be tuned here against real screenshots.

**Files:**
- Create: `tools/check_hero_rendered.py`
- Possibly modify: `assets/css/site.css` (only the `object-position` value, if the screenshots show the silos are out of frame)

**Interfaces:**
- Consumes: `srgb_relative_luminance()` and `contrast_ratio()` from `tools/check_hero_contrast.py` (Task 2).
- Produces: nothing.

- [ ] **Step 1: Write the failing test**

Create `tools/check_hero_rendered.py`:

```python
"""Measure the real rendered homepage hero at desktop and mobile widths.

Serves the site, screenshots the hero, and asserts it is actually bright and
that hero text still passes AA against the pixels behind it.

Run from the repo root:  python tools/check_hero_rendered.py
Exits non-zero if the rendered hero is too dark or contrast fails.
"""
import http.server
import pathlib
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


def serve():
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(ROOT), **k
    )
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
                text_zone = img.crop(
                    (0, int(ih * 0.55), int(iw * 0.62), ih)
                )
                tz = ImageStat.Stat(text_zone).mean[0]
                ratio = contrast_ratio(
                    srgb_relative_luminance(255), srgb_relative_luminance(tz)
                )

                print(f"[{name} {w}x{h}]")
                print(f"  overall mean luminance : {mean:6.1f} (needs >= {MIN_RENDERED_MEAN})")
                print(f"  sky (top third)        : {sky:6.1f}")
                print(f"  text zone              : {tz:6.1f}")
                print(f"  white text contrast    : {ratio:6.2f}:1 (AA needs {AA_NORMAL})")
                print(f"  screenshot             : {shot.relative_to(ROOT)}")

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
```

- [ ] **Step 2: Run the test and read the numbers**

Run: `python tools/check_hero_rendered.py`

Expected: it should PASS, since Tasks 2 and 3 already changed the image and scrim. The point of this step is the numbers and the two screenshots, not the exit code. If it fails, the most likely cause is the mobile crop.

- [ ] **Step 3: Look at the screenshots and tune the crop**

Open `docs/superpowers/plans/hero-shots/hero-desktop.png` and `hero-mobile.png` with the Read tool. Judge one thing: **are the silos and conveyor towers visible, or has the crop left a bland strip of sky and ground?**

If the silos are missing or badly clipped on mobile, adjust only the `object-position` percentage in the `.hero--home .hero-frame img` rule in `assets/css/site.css` and re-run Step 2. Lower percentages pan left, higher pan right. Try `30%`, then `45%`, and keep whichever framing shows the plant best at both viewports.

Change nothing else. If the numbers pass and the silos are visible, leave the value as it is.

- [ ] **Step 4: Run the full verification suite**

Run:

```bash
python tools/check_og_dimensions.py && python tools/check_hero_contrast.py && python tools/check_hero_image.py && python tools/check_hero_rendered.py
```

Expected: all four print PASS and exit 0.

Then confirm nothing else regressed:

```bash
python -c "
from html.parser import HTMLParser
import json, re, pathlib
VOID={'area','base','br','col','embed','hr','img','input','link','meta','source','track','wbr'}
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.st=[]; s.err=[]
    def handle_starttag(s,t,a):
        if t not in VOID: s.st.append(t)
    def handle_endtag(s,t):
        if t in VOID: return
        if not s.st or s.st[-1]!=t: s.err.append(t)
        else: s.st.pop()
for f in ['index.html','about.html','ongoing-projects.html','completed-projects.html','capability.html','contact.html','coming-soon.html']:
    s=pathlib.Path(f).read_text(encoding='utf-8')
    p=P(); p.feed(s)
    lds=[json.loads(b) for b in re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>',s,re.S)]
    print(f'{f:26} markup={\"OK\" if not(p.err or p.st) else \"ERR\"} ld={len(lds)} parsed')
"
```

Expected: seven lines, every one `markup=OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/check_hero_rendered.py docs/superpowers/plans/hero-shots assets/css/site.css
git commit -m "test(hero): verify the rendered hero is bright at both viewports

Screenshots the hero from a real browser at 1440x900 and 390x844 and
asserts the rendered pixels are bright and hero text still clears AA.
The source checks cannot catch a bad crop; this one can, which matters
because cover() keeps only 18% of the image width at 390px."
```

---

## Verification against the spec

| Spec requirement | Task |
| --- | --- |
| Hero image becomes `photo-p7-1.jpg` | 3 |
| Rendered hero substantially brighter than the current dark state | 3, 4 |
| Scrim exactly `0 / .08 / .52` | 2 |
| `saturate(.82) contrast(1.03)` removed from home hero | 2 |
| White hero text at least 4.5:1 | 2, 4 |
| Silos visible at 1440×900, 1280×800 and 390×844 | 3, 4 |
| Homepage `og:image` becomes the bright image | 3 |
| `og:image` dimensions correct (1264×500) | 1, 3 |
| Markup balanced, JSON-LD parses on all seven pages | 4 |
| No console errors | 4 |
| `capability.html` unchanged | Global constraint; Task 3 touches only `index.html` and shared files |
| Hero copy unchanged | Global constraint |
| Animation timings unchanged | Global constraint; asserted in Task 2's check |
