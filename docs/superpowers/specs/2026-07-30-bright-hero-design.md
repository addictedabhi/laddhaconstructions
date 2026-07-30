# Bright industrial hero — design

Date: 2026-07-30
Status: approved

## Problem

The homepage opens dark. Two causes compound:

1. `assets/photo-p6-1.jpg` is a night shot with **mean luminance 33.9** — the
   darkest asset in the project — and crushed blacks (10th percentile = 1, so
   there is no shadow detail to recover).
2. The `.hero--home` scrim then darkens it further, running to 88% black at the
   foot of the image.

A dark photograph under a dark overlay. No CSS adjustment rescues the source.

Measured across every asset:

| File | Mean luminance |
| --- | --- |
| photo-p6-1 (current hero) | **33.9** |
| photo-p9-1 | 70.2 |
| photo-p18-1 | 99.1 |
| photo-p11-1 | 108.1 |
| photo-p5-1 | 137.1 |
| **photo-p7-1** | **139.0** |
| photo-p4-1 | 139.8 |
| 1000514574 | 175.6 |

## Goal

A bright hero showing industrial structures and tall buildings, without
weakening text legibility and without introducing imagery the firm does not own.

## Decisions

### Image: `assets/photo-p7-1.jpg`

The Mangalam Cement plant — bright daylight, blue sky with cloud, tall silos and
conveyor towers against hills.

| | current | new |
| --- | --- | --- |
| Mean luminance | 33.9 | 139.0 (4.1×) |
| Dimensions | 1080×607 | 1264×500 |
| Watermark | none | none |
| Subject | night flyover | silos, conveyors, sky |

It is the firm's own completed work (M-35 coal-yard concrete, Mangalam Cement
Ltd., 2021–22), so the hero shows real delivered work rather than stock.

Two alternatives were examined and rejected:

- **photo-p11-1** — bright and well composed, but carries a `GOLDEN FI…`
  watermark from another company at top-right.
- **photo-p4-1** — bright and wide, but a CGI architectural rendering rather
  than a photograph, with a `MILESTONE TOWNSHIP` logo burned in at centre-bottom,
  exactly where hero text sits.

### Capability keeps the same image

`photo-p7-1.jpg` currently anchors `capability.html`, so it will appear on two
pages. Accepted deliberately: the alternatives were a watermarked rendering
(photo-p4-1) or a 640×347 image too small to hold a 52vh hero (photo-p5-1).
Both pages concern industrial capability, so the repetition reads as a signature
image rather than an oversight.

If the client later supplies a photograph of their own plant — excavators,
pavers, the bitumen plant, the inspection unit — that is the better Capability
hero and this decision should be revisited.

### Scrim: derived from measured contrast

The photograph carries its own top-to-bottom gradient:

| Band (top → bottom) | Mean luminance |
| --- | --- |
| 1/5 | 202.8 |
| 2/5 | 175.9 |
| 3/5 | 120.1 |
| 4/5 | 112.2 |
| 5/5 | 84.0 |

The hero copy occupies the bottom-left region, whose mean luminance is 108.2.
White text over that region measures **5.23:1 — passing WCAG AA before any
scrim is applied**. The scrim is therefore for robustness, not rescue, and can
be far lighter than the one it replaces.

```css
/* new */
linear-gradient(180deg,
  rgba(18,17,15,0.00)   0%,
  rgba(18,17,15,0.08)  40%,
  rgba(18,17,15,0.52) 100%)

/* previous */
linear-gradient(180deg,
  rgba(18,17,15,0.62)   0%,
  rgba(18,17,15,0.36)  42%,
  rgba(18,17,15,0.88) 100%)
```

Contrast of white text over the text zone at each scrim value:

| Scrim alpha | Effective bg | Contrast | Result |
| --- | --- | --- | --- |
| 0.00 | 108.2 | 5.23:1 | passes AA |
| 0.52 | 51.9 | 12.4:1 | passes AA comfortably |
| 0.88 (old) | 13.0 | 18.9:1 | passes, but image is invisible |

The sky is left fully clear at the top of the gradient. That is the entire point
of the change.

`filter: saturate(.82) contrast(1.03)` is removed from the home hero image. That
desaturation was tuned for the night photograph and would mute the blue sky.
Subpage heroes are untouched and keep their own treatment.

### Crop control

At 2.53:1 the source is far wider than a `100svh` hero, so `object-fit: cover`
crops the sides. Measured:

| Viewport | Aspect | Width retained |
| --- | --- | --- |
| Desktop 1440×900 | 1.60 | 63% |
| Laptop 1280×800 | 1.60 | 63% |
| Mobile 390×844 | 0.46 | **18%** |

At 18% the silos and conveyor gallery — the reason the photograph works — are
cropped out almost entirely, leaving a narrow centre strip.

Mitigation:

- `object-position` biased left of centre to hold the silo cluster in frame.
  The exact value is tuned against rendered screenshots, not chosen up front.
- Hero height reduced on narrow viewports so less aggressive cropping is needed.

This is the highest-risk part of the change and must be verified visually at
both desktop and mobile widths before it is considered done.

### Social preview

The homepage `og:image` and `twitter:image` move to `photo-p7-1.jpg`, with
`og:image:width` / `og:image:height` corrected to 1264×500. Other pages keep
their own contextual images.

Without this, a shared homepage link would preview the dark night photograph
while the page itself opens bright — a mismatch between preview and landing
page.

## Files changed

| File | Change |
| --- | --- |
| `assets/css/site.css` | `.hero--home` scrim, remove filter, `object-position`, mobile height |
| `index.html` | hero `<img src>` and `alt` |
| `tools-seo.py` | homepage OG image + dimensions; regenerate all pages |

`tools-seo.py` owns the block between `<!-- seo:start -->` and `<!-- seo:end -->`
on every page, so the OG change is made there and the script re-run — never by
hand-editing the generated block.

## Out of scope

- No new images sourced or licensed.
- No change to `capability.html`.
- No change to hero copy: kicker, `h1`, lede and buttons stay as written.
- No change to animation timings. `kb` at 38s and the `fadeUp` sequence are a
  client request ("slow", deliberately) and are preserved.

## Verification

1. Mean luminance of the rendered hero region increases substantially from the
   current dark state.
2. White hero text measures at least 4.5:1 against the scrimmed image.
3. Silos remain visible at 1440×900, 1280×800 and 390×844.
4. Markup stays balanced; all links and assets resolve.
5. JSON-LD still parses on all seven pages; OG dimensions match the real file.
6. No console errors.
