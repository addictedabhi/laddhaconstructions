"""Inject SEO head tags into the Laddha Constructions static pages.

One-shot generator: rewrites the <head> of each page between the viewport meta
and the first stylesheet link. Re-runnable — it replaces any block it wrote
before, so editing this file and running again is safe.
"""
import re
import pathlib

ROOT = pathlib.Path(r"d:\1. My Projects\Personal Github\laddhaconstructions")

# ── the one value to change when the real domain is confirmed ───────────────
SITE = "https://laddhaconstructions.com"   # no trailing slash
BRAND = "Laddha Constructions"
PHONE = "+91-98293-54600"
EMAIL = "laddha.ankit1986@gmail.com"


def image_size(repo_root, rel_path):
    """Real pixel size of an image in the repo.

    Open Graph dimensions were previously a single global, so pages whose
    image was not 1080x607 advertised a size the file did not have. Reading
    the file keeps the declaration honest when an image is swapped.
    """
    from PIL import Image

    with Image.open(repo_root / rel_path) as im:
        return im.size

# Canonical Google Maps place URL for the Kota office. Preferred over a
# share.google short link: short links can expire or be rotated, and they
# redirect through an interstitial.
MAPS_URL = (
    "https://www.google.com/maps/place/Laddha+Constructions/"
    "@25.1433019,75.843112,17z/data=!4m6!3m5"
    "!1s0x396f850041659251:0x3937f217c7374e6b"
    "!8m2!3d25.1433019!4d75.843112!16s%2Fg%2F11ntks3732"
)

START = "<!-- seo:start -->"
END = "<!-- seo:end -->"

# Every page: canonical path, title, description, OG image, indexability.
PAGES = {
    "index.html": dict(
        path="/",
        title=f"{BRAND} — Civil Contractors in Kota, Rajasthan",
        desc=(
            "Civil construction across the Hadoti region since 2008 — highways, "
            "township roads, industrial infrastructure and stepwell restoration."
        ),
        img="assets/photo-p7-1.jpg",
        img_alt="Cement plant at Kota with silos and conveyor gallery under a bright sky",
        index=True,
        og_type="website",
    ),
    "about.html": dict(
        path="/about.html",
        title=f"About the Firm — {BRAND}, Kota",
        desc=(
            "A Kota civil construction firm building roads, highways and townships "
            "since 2008 — for PWD, UIT Kota, Nagar Nigam, RIICO and developers."
        ),
        img="assets/photo-p9-1.jpg",
        img_alt="Aerial view of a road interchange under construction",
        index=True,
        og_type="website",
    ),
    "ongoing-projects.html": dict(
        path="/ongoing-projects.html",
        title=f"Ongoing Projects — {BRAND}",
        desc=(
            "Industrial townships, government road works and heritage stepwell "
            "restoration under way across Kota, Bhilwara, Mandana and Jaipur."
        ),
        img="assets/1000514574.jpg",
        img_alt="Entrance gate of Urbana Techno Park at Mandana",
        index=True,
        og_type="website",
    ),
    "completed-projects.html": dict(
        path="/completed-projects.html",
        title=f"Completed Projects — {BRAND}",
        desc=(
            "Finished work across Kota and Hadoti — flyover corridors, underpasses, "
            "township roads, M-35 industrial concrete and bawari restoration."
        ),
        img="assets/photo-p11-1.jpg",
        img_alt="Aerial view of a completed flyover crossing Kota",
        index=True,
        og_type="website",
    ),
    "capability.html": dict(
        path="/capability.html",
        title=f"Services, Plant & Machinery — {BRAND}",
        desc=(
            "Construction services backed by owned plant — excavators, paver "
            "finishers, rollers, 60 TPH bitumen plants and in-house material testing."
        ),
        img="assets/photo-p7-1.jpg",
        img_alt="Industrial plant with silos and conveyor gallery",
        index=True,
        og_type="website",
    ),
    "contact.html": dict(
        path="/contact.html",
        title=f"Contact — {BRAND}, Kota, Rajasthan",
        desc=(
            "Talk to our Kota office about roads, township, industrial or heritage "
            "works. WhatsApp 98293 54600 or email laddha.ankit1986@gmail.com."
        ),
        img="assets/photo-p12-1.jpg",
        img_alt="Lit entrance gateway of a completed township",
        index=True,
        og_type="website",
    ),
}

# ── structured data ────────────────────────────────────────────────────────
# GeneralContractor is the Schema.org type that actually fits a civil works
# firm; it inherits from LocalBusiness, so one node covers both.
ORG_LD = {
    "@context": "https://schema.org",
    "@type": "GeneralContractor",
    "@id": f"{SITE}/#organization",
    "name": BRAND,
    "url": f"{SITE}/",
    # Schema.org expects the real logo here, not a photograph. PNG rather
    # than SVG: Google's structured-data logo field does not accept SVG.
    "logo": f"{SITE}/assets/brand/favicon-512.png",
    "image": f"{SITE}/assets/photo-p6-1.jpg",
    "description": (
        "Civil construction firm in Kota, Rajasthan, delivering roads and highways, "
        "township infrastructure, industrial site works with electrical scope, "
        "buildings, industrial concrete and heritage stepwell restoration."
    ),
    "foundingDate": "2008",
    "telephone": PHONE,
    "email": EMAIL,
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "A-491 Indra Vihar",
        "addressLocality": "Kota",
        "addressRegion": "Rajasthan",
        "addressCountry": "IN",
    },
    "areaServed": [
        {"@type": "AdministrativeArea", "name": "Hadoti region, Rajasthan"},
        {"@type": "City", "name": "Kota"},
        {"@type": "City", "name": "Bundi"},
        {"@type": "City", "name": "Bhilwara"},
        {"@type": "City", "name": "Jaipur"},
        {"@type": "State", "name": "Rajasthan"},
    ],
    "knowsAbout": [
        "Road and highway construction",
        "Granular sub-base and wet mix macadam",
        "Bituminous macadam surfacing",
        "Township road networks and drainage",
        "Industrial site infrastructure",
        "33 kV feeder and GSS installation",
        "M-35 industrial concrete paving",
        "Bawari (stepwell) heritage restoration",
    ],
    "founder": {"@type": "Person", "name": "Ashok Laddha"},
    # Coordinates and the Maps URL of the verified Google Business listing
    # (Knowledge Graph id /g/11ntks3732). These tie the site to the listing,
    # which is what earns the map pack for local searches.
    "hasMap": MAPS_URL,
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": 25.1433019,
        "longitude": 75.843112,
    },
    "sameAs": [
        "https://wa.me/919829354600",
        MAPS_URL,
    ],
}

SERVICES = [
    ("Roads & highways",
     "Excavation, granular sub-base, wet mix macadam, primer and tack coat, "
     "bituminous macadam and concrete surfacing."),
    ("Township infrastructure",
     "Internal road networks, drainage, hume pipe, PCC and masonry works for "
     "residential and coaching-hub townships."),
    ("Industrial & electrical",
     "Industrial site infrastructure with water supply, overhead power line, "
     "32 kV GSS and 33 kV feeder installation."),
    ("Buildings",
     "Row houses and villas from foundation through structure to finishing."),
    ("Industrial concrete",
     "Heavy-duty paving in grades up to M-35 for coal yards and plant roads."),
    ("Heritage restoration",
     "Conservation of historic bawaris in stone — step reconstruction, gallery "
     "repair and water management."),
]


def json_ld(obj, indent=2):
    """Minimal JSON serializer. Avoids importing json just to get 2-space output
    with the key order preserved as authored above."""
    import json
    return json.dumps(obj, indent=indent, ensure_ascii=False)


def breadcrumb(name, path):
    items = [{
        "@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/",
    }]
    if path != "/":
        items.append({
            "@type": "ListItem", "position": 2, "name": name,
            "item": f"{SITE}{path}",
        })
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def crumb_name(fname):
    return {
        "about.html": "About",
        "ongoing-projects.html": "Ongoing projects",
        "completed-projects.html": "Completed projects",
        "capability.html": "Services, plant & machinery",
        "contact.html": "Contact",
    }.get(fname, "Home")


def build_block(fname, cfg):
    url = f"{SITE}{cfg['path']}"
    img = f"{SITE}/{cfg['img']}"
    robots = (
        "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
        if cfg["index"] else
        "noindex, nofollow"
    )

    lines = [START]
    lines.append(f'<title>{cfg["title"]}</title>')
    lines.append(f'<meta name="description" content="{cfg["desc"]}">')
    lines.append(f'<link rel="canonical" href="{url}">')
    lines.append(f'<meta name="robots" content="{robots}">')
    if not cfg["index"]:
        lines.append("<!-- Retired holding page, kept out of search on purpose: it must not")
        lines.append("     compete with the live homepage at /. -->")
    lines.append(f'<meta name="author" content="{BRAND}">')

    # Geo / local signals — Kota, Rajasthan.
    lines.append('<meta name="geo.region" content="IN-RJ">')
    lines.append('<meta name="geo.placename" content="Kota, Rajasthan">')

    # Open Graph
    lines.append(f'<meta property="og:type" content="{cfg["og_type"]}">')
    lines.append(f'<meta property="og:site_name" content="{BRAND}">')
    lines.append('<meta property="og:locale" content="en_IN">')
    lines.append(f'<meta property="og:title" content="{cfg["title"]}">')
    lines.append(f'<meta property="og:description" content="{cfg["desc"]}">')
    lines.append(f'<meta property="og:url" content="{url}">')
    lines.append(f'<meta property="og:image" content="{img}">')
    og_w, og_h = image_size(ROOT, cfg["img"])
    lines.append(f'<meta property="og:image:width" content="{og_w}">')
    lines.append(f'<meta property="og:image:height" content="{og_h}">')
    lines.append(f'<meta property="og:image:alt" content="{cfg["img_alt"]}">')

    # Twitter / X
    lines.append('<meta name="twitter:card" content="summary_large_image">')
    lines.append(f'<meta name="twitter:title" content="{cfg["title"]}">')
    lines.append(f'<meta name="twitter:description" content="{cfg["desc"]}">')
    lines.append(f'<meta name="twitter:image" content="{img}">')
    lines.append(f'<meta name="twitter:image:alt" content="{cfg["img_alt"]}">')

    # Theme colour matches the dark footer ground.
    lines.append('<meta name="theme-color" content="#1a1917">')

    # Favicons. The SVG is preferred by modern browsers and stays sharp at any
    # size; the PNGs cover older ones and the Android/iOS home-screen icons.
    # Below 48px the mark uses simplified artwork - the formation hairline
    # fills in and muddies at small sizes.
    lines.append('<link rel="icon" href="assets/brand/laddha-favicon.svg" type="image/svg+xml">')
    lines.append('<link rel="icon" href="assets/brand/favicon-32.png" sizes="32x32" type="image/png">')
    lines.append('<link rel="icon" href="assets/brand/favicon-192.png" sizes="192x192" type="image/png">')
    lines.append('<link rel="apple-touch-icon" href="assets/brand/apple-touch-icon-180.png">')

    # Structured data. The organization node is emitted once per page (it is the
    # same @id everywhere, which is how search engines reconcile it), plus a
    # page-specific breadcrumb.
    lines.append(f'<script type="application/ld+json">\n{json_ld(ORG_LD)}\n</script>')
    lines.append(
        f'<script type="application/ld+json">\n'
        f'{json_ld(breadcrumb(crumb_name(fname), cfg["path"]))}\n</script>'
    )

    # Capability page carries the service catalogue.
    if fname == "capability.html":
        catalog = {
            "@context": "https://schema.org",
            "@type": "OfferCatalog",
            "name": "Civil construction services",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": n,
                        "description": d,
                        "provider": {"@id": f"{SITE}/#organization"},
                        "areaServed": {"@type": "State", "name": "Rajasthan"},
                    },
                }
                for n, d in SERVICES
            ],
        }
        lines.append(f'<script type="application/ld+json">\n{json_ld(catalog)}\n</script>')

    # Contact page gets an explicit ContactPage node.
    if fname == "contact.html":
        contact = {
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "url": url,
            "mainEntity": {"@id": f"{SITE}/#organization"},
        }
        lines.append(f'<script type="application/ld+json">\n{json_ld(contact)}\n</script>')

    lines.append(END)
    return "\n".join(lines)


def apply(fname, cfg):
    p = ROOT / fname
    s = p.read_text(encoding="utf-8")
    block = build_block(fname, cfg)

    # Re-run: swap out the previously generated block.
    if START in s:
        s = re.sub(re.escape(START) + r".*?" + re.escape(END), block, s,
                   flags=re.S)
    else:
        # First run: drop the hand-written title/description/canonical/OG lines
        # and insert the generated block in their place.
        s = re.sub(r'[ \t]*<title>.*?</title>\n', '', s, flags=re.S)
        s = re.sub(r'[ \t]*<meta name="description"[^>]*>\n', '', s)
        s = re.sub(r'[ \t]*<link rel="canonical"[^>]*>\n', '', s)
        s = re.sub(r'[ \t]*<meta name="robots"[^>]*>\n', '', s)
        s = re.sub(r'[ \t]*<meta property="og:[^>]*>\n', '', s)
        s = re.sub(r'\n[ \t]*\n(?=<link rel="stylesheet")', '\n', s)
        anchor = '<meta name="viewport" content="width=device-width, initial-scale=1">'
        s = s.replace(anchor, anchor + "\n" + block, 1)

    p.write_text(s, encoding="utf-8", newline="")
    return len(block.splitlines())


if __name__ == "__main__":
    for fname, cfg in PAGES.items():
        n = apply(fname, cfg)
        flag = "index" if cfg["index"] else "noindex"
        print(f"{fname:26} {n:3} lines  [{flag}]")
