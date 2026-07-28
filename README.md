# Handoff: Laddha Constructions — marketing website

## Overview
A six-page marketing website for **Laddha Constructions**, a civil-construction firm based in Kota, Rajasthan (established 2008). The site presents the firm, separates ongoing from completed work, documents plant & machinery, and drives contact via WhatsApp and email. Project costs are deliberately **never shown** anywhere on the site (client requirement).

Pages: Home, About, Ongoing Projects, Completed Projects, Capability, Contact.

## About the Design Files
The files in this bundle are **design references authored in HTML** — working prototypes that show the intended look, typography, spacing, imagery and motion. They are **not production code to lift directly**.

Each page is a "Design Component" (`*.dc.html`): a small runtime (`support.js`) mounts the markup inside `<x-dc>` as a React tree and inline `style="…"` attributes are compiled to style objects. **Do not port that runtime.** The task is to **recreate these designs in the target codebase's own environment** (Next.js/React, Astro, Vue, plain static HTML — whatever the project uses) with its established patterns. If no codebase exists yet, this is a brochure site with no dynamic data: a static generator (Astro, Eleventy) or Next.js static export is the most appropriate choice.

Concretely, when recreating:
- Lift the markup structure, copy, spacing values, type sizes and imagery assignments verbatim.
- Convert the repeated header nav, footer, and floating contact widget into three shared components/partials (they are duplicated inline in all six prototype files by necessity, not by design).
- Replace inline styles with the codebase's styling approach (CSS modules, Tailwind, styled-components) while keeping the token values below.
- Keep the design-system stylesheet (`_ds/classical-…/styles.css`) as the token source, or transplant its `:root` variables into the project's own token layer.

## Fidelity
**High-fidelity.** Final colors, typography, spacing, imagery and animation timings. Recreate pixel-accurately. Note two intentional gaps: two project cards carry "Photograph to be provided" placeholders awaiting client photos (see *Assets*).

## Design system
The site is built on the **Classical** design system — an editorial, book-like style on a soft near-white ground: Cormorant Garamond headings over Lora body, justified body copy, hairline rules, colour applied as *stroke not fill* (outlined buttons, bordered unfilled cards), and photographs matted in a `.plate` wrapper like tipped-in book plates.

Hard rules inherited from that system — preserve them:
- Buttons are **outlined**, never solid-filled with the accent.
- No heavy drop shadows; elevation is a whisper.
- No sans-serif for emphasis — italics and weight do that job.
- Headings cap at semibold; the larger the type, the lighter the cut (display headings use weight 400).
- Body-size text in the accent must use `--color-accent-700`, not `--color-accent` (contrast).

### Design tokens (from `_ds/classical-…/styles.css`)

Colors
| Token | Value |
| --- | --- |
| `--color-bg` | `#f3f2f2` |
| `--color-surface` | `#eae9e9` |
| `--color-text` | `#201f1d` |
| `--color-accent` | `#b68235` |
| `--color-divider` | `color-mix(in srgb, #201f1d 16%, transparent)` |
| neutral 100→900 | `#f8f4f4 #eae7e7 #d7d3d3 #bab6b6 #9b9797 #7d7979 #605d5d #444141 #2d2b2b` |
| accent 100→900 | `#fff3e4 #ffe3bf #facb8d #e1ad66 #c28d41 #a06f24 #7d5411 #5a3b0a #3a270d` |

Custom colors used **outside** the token set (two only):
- `#1a1917` — footer and dark hero-copy ground (a shade below `--color-neutral-900`).
- `#f7f5f1` / `rgba(247,245,241,.82)` / `.66` / `.5` — paper-white text on those dark grounds.
- `#25D366` — WhatsApp brand green, used **only** as the fill of the WhatsApp glyph.
- Hero scrims: `linear-gradient(180deg, rgba(18,17,15,.62) 0%, rgba(18,17,15,.36) 42%, rgba(18,17,15,.88) 100%)` (home) and `linear-gradient(180deg, rgba(18,17,15,.44), rgba(18,17,15,.82))` (subpages).

Spacing — **the scale is sparse and skips 5, 7, 9+**. Only these exist:
`--space-1: 4.6px · --space-2: 9.2px · --space-3: 13.8px · --space-4: 18.4px · --space-6: 27.6px · --space-8: 36.8px`
Larger steps in the prototypes are expressed as `calc(var(--space-8) * 1.1 | 1.25 | 1.6 | 2)` and `calc(var(--space-4) * 1.25)`. When re-tokenising, define a complete scale rather than reproducing the calc() workaround.

Type
- `--font-heading: "Cormorant Garamond"` (400, 600) · `--font-body: "Lora"` (400, 600), both from Google Fonts.
- Display h1: `clamp(2.7rem, 7vw, 6rem)` / line-height 1.03 / letter-spacing -.012em / weight 400.
- Subpage h1: `clamp(2.2rem, 5vw, 4rem)` / 1.06 / weight 400.
- Section h2: `clamp(1.9rem, 3.4vw, 3rem)` / 1.12 / weight 400.
- Project title: `2rem` / 1.12 / weight 400. Card title: `1.45rem` / 1.2 / weight 500.
- Body: `1.02rem` / line-height 1.85, `text-align: justify` in prose columns.
- Kicker/eyebrow: `.74–.78rem`, `letter-spacing .2–.28em`, uppercase, `--color-accent-700` on light or `--color-accent-300` on dark.
- Nav: `.8rem`, `letter-spacing .1em`, uppercase.
- Every numeral that stands as a figure (years, phone, quantities, kickers) sets `font-feature-settings: 'tnum'`. Running prose does **not**.

Radius: `--radius-sm 2px · --radius-md 4px · --radius-lg 7px`; floating pills use `999px`.
Shadows: `--shadow-sm: 0 1px 2px …14%` · `--shadow-md: 0 3px 10px …16%` · `--shadow-lg: 0 12px 32px …22%`.

## Global chrome (on all six pages)

### Header
`position: fixed; top/left/right: 0; z-index: 40`, `display:flex; align-items:baseline; justify-content:space-between; gap: var(--space-6)`, padding `var(--space-4) var(--space-8)`, background `color-mix(in oklch, var(--color-bg) 84%, transparent)` with `backdrop-filter: blur(10px)`, `border-bottom: 1px solid var(--color-divider)`.
- Brand: "Laddha" in `--color-text` + "Constructions" in `--color-accent-700`, Cormorant 1.3rem, letter-spacing .04em, links to Home.
- Nav items: Home · About · Ongoing · Completed · Capability · Contact. Inactive `--color-neutral-700`, hover `--color-accent-700`. **Active page** is `--color-accent-700` with `border-bottom: 1px solid var(--color-accent)`.
- On the home page only, the header fades in: `fadeIn 2s ease 2.4s both` (it arrives after the hero copy has settled).

### Footer
Ground `#1a1917`, text `#f7f5f1`, padding `calc(var(--space-8)*1.6) var(--space-8) var(--space-8)`. Three columns via `grid-template-columns: repeat(auto-fit, minmax(220px, 1fr))`, gap `calc(var(--space-8)*1.1)`, max-width 1180px centred:
1. Brand (Cormorant 1.4rem) + address "A-491 Indra Vihar, Kota, Rajasthan".
2. "Pages" — links to the five sibling pages.
3. "Reach us" — phone (`tel:+919829354600`) with a Lucide phone glyph, email with a Lucide mail glyph.
Bottom bar: `border-top: 1px solid rgba(247,245,241,.14)`, padding-top `calc(var(--space-4)*1.25)`, .8rem at `rgba(247,245,241,.5)`: "Laddha Constructions · Civil construction services since 2008" (home page also shows "Kota, Rajasthan, India" right-aligned).

### Floating contact widget — required feature
`position: fixed; right: calc(var(--space-4)*1.25); bottom: calc(var(--space-4)*1.25); z-index: 50; display: grid; gap: var(--space-3); justify-items: end`. Two stacked pills, both `border-radius: 999px`, `padding: 10px 16px 10px 12px`, `display:flex; align-items:center; gap: var(--space-3)`, `.9rem`:
1. **WhatsApp** — `href="https://wa.me/919829354600"`, `target="_blank" rel="noopener"`, label "98293 54600" (tnum), background `#1a1917`, text `#f7f5f1`, `border: 1px solid var(--color-accent-700)`, `--shadow-md`; 22×22 WhatsApp glyph filled `#25D366`. Hover: background `--color-accent-700`, text `#fff`.
2. **Email** — `href="mailto:laddha.ankit1986@gmail.com"`, label "Email us", background `--color-bg`, text `--color-text`, `border: 1px solid var(--color-accent-300)`, `--shadow-sm`; 22×22 Lucide mail glyph stroked `--color-accent-700`. Hover: border and text to `--color-accent-700`.
Both carry `title` attributes with the full number / address. Give both a 44px minimum hit height on touch.

⚠️ Regression watch: this widget's offsets originally used the **non-existent** `--space-5`, which resolved to `auto` and un-pinned the widget entirely. Any token you introduce here must exist.

## Motion

The home hero animation was an explicit client request: **slow**. Keep the long durations — they read as deliberate, not sluggish.

| Name | Keyframes | Applied to |
| --- | --- | --- |
| `kb` | `scale(1.05)` → `scale(1.20) translateY(-2%)` | Home hero image, `38s cubic-bezier(.4,0,.2,1) both` |
| `kbs` | `scale(1.04)` → `scale(1.14)` | Subpage hero images, `30s ease-out both` |
| `fadeUp` | opacity 0 + `translateY(28px)` → settled | Home hero kicker `1.8s .5s`, h1 `2.2s .9s`, paragraph `2s 2.1s`, buttons `2s 2.5s`; all `cubic-bezier(.22,.61,.36,1)`. Subpage kicker `1.4s .2s`, h1 `1.8s .45s` |
| `lineGrow` | `scaleX(0)` → `scaleX(1)`, `transform-origin: left` | Home hero 1px accent rule (max-width 420px), `2.6s 1.8s` |
| `fadeIn` | opacity 0 → 1 | Header `2s 2.4s`, "Scroll" cue `2s 3s` |
| `drift` | opacity 0 + `translateY(16px)` → settled | Every `[data-reveal]` element on scroll, `1.3–1.4s cubic-bezier(.22,.61,.36,1) forwards` |

Scroll reveal: `[data-reveal] { opacity: 0 }`; an IntersectionObserver (`threshold: 0.1`, `rootMargin: '0px 0px -6% 0px'`) adds `.is-in` once and unobserves. Sibling groups stagger via `animation-delay` of `.08s`–`.5s`. Fall back to immediately-visible if IntersectionObserver is absent.

`prefers-reduced-motion: reduce` → `[data-reveal] { opacity: 1; animation: none !important }` and `* { animation-duration: .01ms !important }`. `html { scroll-behavior: smooth }`.

## Screens

Shared page geometry: content sections are `max-width: 1180px; margin: 0 auto`, horizontal padding `var(--space-8)`, vertical rhythm `calc(var(--space-8)*1.6)` to `calc(var(--space-8)*2)`. Section breaks are `border-top: 1px solid var(--color-divider)`, never a filled band except the two tinted sections noted below (`--color-neutral-100` with divider borders top and bottom).

### 1. Home — `Laddha Constructions.dc.html`
Purpose: establish the firm and route to the two project pages.
- **Hero** — `height: 100vh; min-height: 620px`, `display: grid; align-items: end`. Image `extracted/photo-p6-1.jpg` (night flyover), `object-fit: cover`, `filter: saturate(.82) contrast(1.03)`, animating `kb`. Scrim over it. Copy block padded `0 var(--space-8) calc(var(--space-8)*1.4)`, max-width 1180px.
  - Kicker: "Kota, Rajasthan · Established 2008"
  - h1: "Roads, townships / and the ground / beneath them." (explicit `<br>`s, `text-wrap: balance`)
  - 1px accent rule, then paragraph (max-width 46ch): "Civil construction across the Hadoti region — highways and township roads, industrial infrastructure, and the restoration of Rajasthan's historic stepwells."
  - Buttons: "Ongoing projects" (`.btn .btn-primary`, border `--color-accent-300`, text `#f7f5f1`) → Ongoing; "Get in touch" (`.btn .btn-ghost`, `rgba(247,245,241,.82)`) → Contact.
  - Right edge, bottom: vertical "Scroll" — `writing-mode: vertical-rl`, .7rem, letter-spacing .3em.
- **The firm** — two columns `minmax(0,1fr) minmax(0,1.35fr)`, gap `calc(var(--space-8)*1.25)`, `align-items: start`. Left: kicker "The firm" + h2 "Eighteen years of building in the Hadoti region." Right: the intro paragraph (see About for the copy), an "About the firm" link underlined in accent, then a 3-up stat row above a divider — **2008** Established · **36** Years of leadership · **5** Works in progress (Cormorant 2.5rem, `--color-accent-700`, tnum; labels .78rem uppercase `--color-neutral-600`).
- **What we build** — 4 `.card`s in `repeat(auto-fit, minmax(240px, 1fr))`, gap `var(--space-6)`, staggered .12s: Roads & highways · Township infrastructure · Industrial & electrical · Heritage restoration.
- **Work on the ground** — full-bleed band, `height: 58vh; min-height: 400px`, image `extracted/photo-p11-1.jpg`, scrim `rgba(18,17,15,.24)→.74`; h2 + "Ongoing" / "Completed" buttons pinned bottom-left.
- **Quality quote** — centred, max-width 900px, Cormorant `clamp(1.5rem, 3vw, 2.3rem)` italic: "Material checked at our own inspection unit, work delivered to the client's specification, and every service completed on time." Caption "Our quality commitment".

### 2. About — `About.dc.html`
Hero band `52vh / min 340px`, image `extracted/photo-p9-1.jpg`, kicker "About", h1 "The firm and the people behind it".
- **Intro** — two columns `1fr / 1.4fr`. Left h2 "Civil construction, delivered to specification." + 64px accent rule. Right, three justified paragraphs covering: the Kota base and client list (PWD, UIT, Nagar Nigam, Marketing Board, RIICO); the scope (full road train — excavation, GSB, WMM, bituminous macadam, concrete surfacing — plus township drainage, masonry, hume pipe, industrial site infrastructure with electrical scope, stepwell conservation); and the in-house inspection unit.
- **Leadership** — `.plate` image `extracted/photo-p11-1.jpg` (aspect 4/3) beside kicker "Leadership", h3 "Mr. Ashok Laddha", a paragraph on his thirty-six years in civil engineering services and the permanent site team, and three `.tag.tag-outline` chips: Planning · Execution · Quality control.
- **Clients & authorities** — tinted band, 13 `.tag.tag-outline` chips in a `flex-wrap` row, gap `var(--space-3)`: PWD, UIT Kota, Nagar Nigam, Marketing Board, RIICO, Mangalam Cement Ltd., Bhatia Colonizer, Shubham Group, Suwalka & Suwalka, Multimetal Ltd., Orilite Life Space LLP, Urbana Techno Park LLP, Golcha Group. Chips are overridden to `padding: 5px 12px; white-space: nowrap; color: var(--color-accent-700); border-color: var(--color-accent-300)`.

### 3. Ongoing Projects — `Ongoing-Projects.dc.html`
Hero `52vh`, image `uploads/1000514574.jpg` (Urbana gate), kicker "Projects · In progress", h1 "Ongoing projects".
Five `<article>` spreads, gap `calc(var(--space-8)*2)`, alternating column order `1.1fr/1fr` ↔ `1fr/1.1fr`, `align-items: center`. Each: `.plate` image at aspect 4/3, then kicker "Place · Client", h2, justified paragraph, and outlined scope chips.
1. **Urbana Techno Park** — Mandana · Urbana Techno Park LLP. Industrial township end to end: internal roads and civil works, water-supply infrastructure, complete electrical scope — overhead power line, 32 kV GSS, 33 kV feeder. Chips: Roads · Water supply · 33 kV feeder. Image `uploads/1000514574.jpg`.
2. **Ummedganj–Kaithun road** — Kota · UIT, Kota. 8 km of new road, full train from formation and GSB to WMM and bituminous surfacing. Chips: 8 km · Government work. Image `extracted/photo-p9-1.jpg`.
3. **Industrial township, Bhilwara** — Bhilwara · Golcha Group. Site infrastructure and internal roads — earthwork, formation, surfacing. Chips: Industrial roads · Site infrastructure. **Image: placeholder.**
4. **Gardenia township** — Kota · Orilite Life Space LLP. Internal road network, landscaped gardens, and the villas. Chips: Roads · Gardens · Villas. Image `extracted/photo-p13-1.jpg`.
5. **Bawari restoration, Jaipur** — Jaipur · Heritage restoration. Stone repair, reconstruction of steps and galleries, water management. Chips: Stone conservation · Heritage. Image `extracted/photo-p17-1.jpg`.
Closing tinted band: "Looking at a project of your own?" + "Talk to us" → Contact.

### 4. Completed Projects — `Completed-Projects.dc.html`
Hero `52vh`, image `extracted/photo-p11-1.jpg`, kicker "Projects · Handed over", h1 "Completed projects", then a 62ch lead paragraph.
Ten cards in `repeat(auto-fit, minmax(300px, 1fr))`, gap `calc(var(--space-8)*1.1)`, staggered .08s. Card = `.card` with `padding: 0; overflow: hidden`; image at aspect 3/2 `object-fit: cover` flush to the top edge; body padded `var(--space-6)` with kicker (year · client, tnum), h2 1.45rem/500, and a .98rem paragraph.
| Project | Kicker | Image |
| --- | --- | --- |
| Indira Gandhi flyover | 2021–23 · Vijay M Mistry Construction | photo-p6-1 |
| Danbari–Keshavpura flyover | 2020–22 · Vijay M Mistry Construction | photo-p11-1 |
| Aerodrome underpass | 2021–22 · Vijay M Mistry Construction | photo-p9-1 |
| Landmark City | Kota · Township roads | photo-p5-1 |
| Milestone Township | Kota · Township roads | photo-p4-1 |
| Coral Park | Kota · Coaching hub | photo-p12-1 |
| Coal-yard concrete, M-35 | 2021–22 · Mangalam Cement Ltd. | photo-p7-1 |
| Royal Villa, Baran Road | 2022–24 · Royal Prime Ltd. | photo-p13-1 |
| Bawari restoration, Bundi & Hadoti | 2024–25 · Nagar Nigam · UIT | photo-p18-1 |
| Roads at Talwandi & Jawahar Nagar | 2021–23 · UIT, Kota | **placeholder** |
Quantities quoted in the copy (keep exact): Landmark City — 22,675 cum excavation, 38,265 cum GSB, 15,675 cum WMM and concrete, masonry, PCC, hume pipe, 34,250 ferro covers. Milestone — 9,900 cum excavation, 12,000 cum GSB, 22,500 sqm primer and tack coat, 1,125 cum bituminous macadam. Royal Villa — 25 row houses.
Closing tinted band: "See what we have under way now" + "Ongoing projects".

### 5. Capability — `Capability.dc.html`
Hero `52vh`, image `extracted/photo-p7-1.jpg`, kicker "Capability", h1 "Services, plant and machinery".
- **Services** — 6 `.card`s, `minmax(240px, 1fr)`, staggered .1s: Roads & highways · Township infrastructure · Industrial & electrical · Buildings · Industrial concrete · Heritage restoration.
- **Plant & machinery** — tinted band, 3 columns `minmax(260px, 1fr)`, gap `calc(var(--space-8)*1.15)`. Each: h2 1.5rem/500, a 48px accent rule, a paragraph, then a `<ul>` at `line-height: 2`, `--color-neutral-700`.
  - *Earthmoving*: 3 × Poclain excavator · 2 × JCB · 1 × grader · 3 × tractor, 5 × dumper.
  - *Compaction & paving*: 2 × paver finisher · 1 × vibratory roller · 1 × tandem roller · 3 × static roller.
  - *Bituminous & concrete*: bitumen plant 60 TPH · bitumen plant 55 TPH · 2 × tar boiler, 1 × compressor · 3 × Ajax Fiori self-loading mixer.
- **Quality** — `.plate` `extracted/photo-p5-1.jpg` beside h2 "Quality, checked before it reaches the site.", a paragraph on testing aggregate/bitumen/concrete in-house and signing off each layer, and a "Discuss a project" button.

### 6. Contact — `Contact.dc.html`
Hero `46vh / min 300px`, image `extracted/photo-p12-1.jpg`, kicker "Contact", h1 "Let's discuss your project".
Two columns `repeat(auto-fit, minmax(280px, 1fr))`, `align-items: start`. Left: h2 "Tell us what you are building." + a paragraph inviting a scope, drawing set or site note, noting WhatsApp is quickest. Right: three divider-topped blocks —
- **Office**: A-491 Indra Vihar, Kota, Rajasthan, India
- **WhatsApp & phone**: 98293 54600 → `https://wa.me/919829354600`, 24px WhatsApp glyph, 1.15rem, tnum
- **Email**: laddha.ankit1986@gmail.com → `mailto:`, 24px Lucide mail glyph, `word-break: break-all`
Then two buttons: "Message on WhatsApp" (`.btn-primary`) and "Send an email" (`.btn-secondary`).
**There is no contact form** — deliberately. All contact is direct-channel. If a form is added later it needs a backend decision (the prototype has none).

## Interactions & behavior
- Navigation is plain page-to-page `<a href>`; no client-side router, no JS-driven state. The prototypes link to `Laddha%20Constructions.dc.html` etc. — in the real build these become `/`, `/about`, `/projects/ongoing`, `/projects/completed`, `/capability`, `/contact`.
- Hover: nav `--color-neutral-700` → `--color-accent-700`; buttons and cards take the design system's built-in accent-ramp hover; the two floating pills as described above.
- Focus: the system ships `:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px }` — keep it, never the browser default.
- Scroll reveal as described in *Motion*.
- No loading, empty or error states — the site is static.

## State management
None. No state variables, no data fetching, no forms. Project content is hard-coded copy; if the client later wants to edit it, model each project as `{ title, place, client, period, status: 'ongoing' | 'completed', body, chips[], image }` in a content collection (Astro content collections / MDX / a small JSON file) and drive both project pages plus the home teaser band from it.

## Responsive behavior
The prototypes are desktop-first and rely on `auto-fit` grids, `clamp()` type and `minmax()` columns, so most sections collapse gracefully. **Not yet done — needed for production:**
- The fixed two-column spreads (`minmax(0,1.1fr) minmax(0,1fr)` on Ongoing, `1fr / 1.35fr` and `1fr / 1.4fr` on Home and About) must stack to one column below ~860px, with the image first in each pair.
- The header nav needs a mobile treatment (the six uppercase items will not fit); a hamburger or a wrapped two-line bar.
- On mobile, collapse the floating pills to icon-only circles (~52px) so they don't span the viewport.
- Reduce `100vh` hero to `min(100vh, 680px)` or use `100svh` to avoid mobile browser-chrome jump.
- Drop `text-align: justify` below ~600px (justification at narrow measures opens rivers).

## Assets
All imagery is the client's own, extracted from their company-profile PDF, plus one photo they supplied directly. They live in `assets/` in this bundle (originals were `extracted/` and `uploads/`).
| File | Subject | Used on |
| --- | --- | --- |
| `photo-p6-1.jpg` | Night flyover corridor, Kota | Home hero, Indira Gandhi flyover card |
| `photo-p11-1.jpg` | Aerial flyover through Kota | Home band, About leadership, Completed hero + Keshavpura card |
| `photo-p9-1.jpg` | Aerial road interchange | About hero, Ummedganj–Kaithun, Aerodrome underpass |
| `photo-p5-1.jpg` | Completed township housing + roads | Landmark City, Capability quality |
| `photo-p4-1.jpg` | Milestone Township gate | Milestone Township |
| `photo-p12-1.jpg` | Lit township gateway | Coral Park, Contact hero |
| `photo-p7-1.jpg` | Cement works, silos and conveyor | Capability hero, coal-yard concrete |
| `photo-p13-1.jpg` | Row houses / villas | Gardenia township, Royal Villa |
| `photo-p17-1.jpg` | Historic stepwell | Bawari restoration, Jaipur |
| `photo-p18-1.jpg` | Restored stepwell, carved pillars | Bawari restoration, Bundi & Hadoti |
| `1000514574.jpg` | Urbana Techno Park entrance gate | Ongoing hero + Urbana spread |

Every image has a written `alt` in the prototypes — carry them over. Photographs inside content go through `.plate`: `filter: sepia(0.22) saturate(0.82) contrast(1.05); border: 6px solid var(--color-surface); outline: 1px solid var(--color-divider)`. Hero images are **not** plated.

Icons: **Lucide** (mail, phone). The WhatsApp mark is a brand glyph inlined as SVG (Lucide has no brand icons) — keep it `#25D366` on the dark pill.

**Open items awaiting the client:**
1. Photograph for *Industrial township, Bhilwara* (Golcha Group).
2. Photograph for *Roads at Talwandi & Jawahar Nagar*.
3. Client name and project year for *Bawari restoration, Jaipur*.
Placeholder treatment meanwhile: a dashed-border `.plate` (or a `--color-neutral-100` block with a bottom divider inside a card) at the image's aspect ratio, centring the uppercase caption "Photograph to be provided" in `--color-neutral-600`. Remove the placeholder styling entirely once a photo lands — do not ship the dashed box.

## Content rules (client-mandated)
1. **No project costs, contract values or order-book figures anywhere.** The source company profile carries them; the website must not.
2. The trading name on the website is **Laddha Constructions** (the company profile/deck uses "Laddha Enterprises" — do not mix them).
3. Ongoing and completed work stay on **separate pages**; do not merge into one filterable list.
4. Physical quantities (cum, sqm, km, unit counts) are fine to show and are accurate — keep them exact.

## Files in this bundle
- `Laddha Constructions.dc.html` — Home
- `About.dc.html`
- `Ongoing-Projects.dc.html`
- `Completed-Projects.dc.html`
- `Capability.dc.html`
- `Contact.dc.html`
- `ds/styles.css` — the Classical design-system stylesheet (token source of truth)
- `ds/readme.md` — the design system's own guide: direction, do's and don'ts, component list
- `assets/` — all photographs listed above

To view a prototype as authored, the `.dc.html` files need their runtime and the design-system bundle at the original relative paths; the reliable way to see them is in the original project preview. For implementation, read them as markup — the structure and inline styles are all legible as plain HTML.
