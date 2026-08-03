# Laddha Constructions — logo files

Mark **1c "The Courses"**: the letter L built from laid courses, each block stepping wider as it
descends — pavement layers (sub-base, WMM, macadam, wearing coat) or bawari steps. The gold block
is the finished surface; the gold hairline above is formation level.

## Colors
| Role | Light ground | Dark ground |
| --- | --- | --- |
| Mark body | `#201f1d` | `#f7f5f1` |
| Accent block + rule | `#b68235` | `#facb8d` |
| Ground | `#f3f2f2` | `#1a1917` |

Wordmark: Cormorant Garamond 400, letter-spacing .05em. Descriptor: Lora, uppercase,
letter-spacing .34em, `#7d5411` on light / `#facb8d` on dark.

## Files

`svg/` — vector masters, use these wherever possible
- `laddha-mark.svg` — full mark incl. the formation hairline
- `laddha-mark-reversed.svg` — for dark grounds
- `laddha-favicon.svg` — simplified (no hairline), for use below ~48px

`mark/` — transparent PNG, 256 / 512 / 1024 px, plus reversed at 512 / 1024

`lockup/` — mark + wordmark, PNG at 2x
- `laddha-lockup-horizontal.png` — default; use in headers and letterheads
- `laddha-lockup-stacked.png` — for square/centred placements
- `laddha-lockup-reversed.png` — on the dark ground

`jpg/` — the same lockups plus the mark, flattened for anything that won't take PNG
(WhatsApp Business, print vendors, Google Business Profile)

`favicon/` — 16 / 32 / 48 / 192 / 512 px + `apple-touch-icon-180.png`

## Web usage
```html
<link rel="icon" href="/favicon/laddha-favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/favicon/apple-touch-icon-180.png">
```

## Rules
- Clear space on all four sides = the height of one course block (14% of the mark's height).
- Minimum size: 26px on screen, 12mm in print. Below that drop the wordmark and use the mark alone;
  below 48px use the simplified favicon artwork (the hairline fills in and muddies).
- Never recolor the gold block to anything but the two accents above, never add a shadow or
  gradient, never stretch, and never set the wordmark in a sans-serif.
