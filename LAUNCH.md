# Site status — LIVE

The six-page site is the live site. The holding page has been retired.

| URL | File | Indexable |
| --- | --- | --- |
| `/` | `index.html` — homepage | yes |
| `/about.html` | About | yes |
| `/ongoing-projects.html` | Ongoing projects | yes |
| `/completed-projects.html` | Completed projects | yes |
| `/capability.html` | Services, plant & machinery | yes |
| `/contact.html` | Contact | yes |
| `/coming-soon.html` | retired holding page | **no** — `noindex, nofollow` |

`sitemap.xml` lists the six indexable URLs. `robots.txt` disallows
`/coming-soon.html`, `/archive/` and `/Document/`.

The holding page is kept on disk but deliberately excluded from search: a stale
"coming soon" page ranking against the real homepage is a real risk. Delete it
with `rm coming-soon.html` whenever you no longer want it, and drop its
`Disallow` line from `robots.txt` at the same time.

## Regenerating head tags

`tools-seo.py` owns every page's `<title>`, description, canonical, robots, OG,
Twitter and JSON-LD. Edit the `PAGES` dict and re-run:

```sh
python tools-seo.py
```

It replaces the block between `<!-- seo:start -->` and `<!-- seo:end -->`, so it
is safe to run repeatedly. Keep descriptions in the 120–160 character band and
titles at or under 60 — the script does not enforce this, but Google truncates
past it.

## DNS — still to do

`CNAME` in the repo root holds `laddhaconstructions.com`. The domain will not
resolve until these records exist at the registrar:

- Four `A` records for the apex → `185.199.108.153`, `185.199.109.153`,
  `185.199.110.153`, `185.199.111.153`
- Optional `AAAA` for IPv6 → `2606:50c0:8000::153`, `...8001::153`,
  `...8002::153`, `...8003::153`
- `CNAME` for `www` → `addictedabhi.github.io`

Then in repo settings → Pages, tick **Enforce HTTPS** once the certificate is
issued (a few minutes to an hour).

Until DNS resolves, every canonical and `og:url` points at a domain that does
not answer. That is expected and harmless — but do not submit the sitemap to
Search Console before the domain is live, or the URLs will be logged as
unreachable.

## After DNS is live

- Verify the property in Google Search Console, submit `sitemap.xml`.
- Request indexing for `/` via URL Inspection to speed up first crawl.
- Set up a Google Business Profile for the Kota office. For a local contractor
  this drives more enquiries than organic ranking, and it makes the
  `GeneralContractor` structured data on every page pay off.
- Check social previews with Facebook's Sharing Debugger and X's Card Validator.

## Outstanding content items

Awaiting the client:

1. Photograph for *Industrial township, Bhilwara* (Golcha Group).
2. Photograph for *Roads at Talwandi & Jawahar Nagar*.
3. Client name and project year for *Bawari restoration, Jaipur*.

Placeholders use `.plate--pending` and `.project-card-pending`. Remove the
class, not just the caption, when a photo lands — the dashed box must not ship
as a final state.

## Note on `Document/`

`Document/Laddha_Enterprises_Profile.pdf` is committed and will be served at
`https://laddhaconstructions.com/Document/Laddha_Enterprises_Profile.pdf`.

Its contents conflict with two rules in `README.md`:

- It has a **"Turnover, last three years"** section, plus contract values —
  README: *"No project costs, contract values or order-book figures anywhere."*
- It is branded **"Laddha Enterprises"** throughout — README: *"The trading
  name on the website is Laddha Constructions ... do not mix them."*

`robots.txt` disallows the directory, but that only asks well-behaved crawlers
not to index it. The file stays publicly downloadable by anyone with the URL.
To actually remove it from the deployed site:

```sh
git rm -r --cached Document
echo "Document/" >> .gitignore
```

It remains in git history (commit `2f0231b`); a full scrub needs
`git filter-repo` and a force push.

If a downloadable profile is wanted on the site, the clean path is a new PDF
with the turnover section removed and the branding corrected to Laddha
Constructions.
