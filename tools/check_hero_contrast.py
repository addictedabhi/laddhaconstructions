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
    block = re.search(r"\.hero--home \.hero-scrim \{(.*?)\}", css, re.S).group(1)
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
    # Look at every .hero--home rule, not one selector. The Ken Burns drift sits
    # on .hero-frame and the fade on the slides, so pinning the assertion to a
    # single rule made it fail the moment the hero became a rotator.
    home_rules = "\n".join(
        m.group(0)
        for m in re.finditer(r"\.hero--home[^{]*\{[^}]*\}", css, re.S)
    )
    # Strip comments: the rules document why the filter was removed, and the
    # word "saturate" inside that prose is not a live declaration.
    home_decls = re.sub(r"/\*.*?\*/", "", home_rules, flags=re.S)
    if "saturate" in home_decls:
        failures.append("home hero image still has a saturate() filter")
    if "kb 38s cubic-bezier(.4,0,.2,1) both" not in home_decls:
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
