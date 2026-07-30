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
