# Beyond the Glass

Passion-project site for Abby McGowan: clear, sourced information on aquarium conservation, rescue and rehabilitation, animal welfare, and the most common aquarium myths. Built from Abby's "Aquarium Project" research doc and her StoryBrand answers.

## Live site

https://odyssey-jotun.github.io/beyond-the-glass/

The repository is public and GitHub Pages serves `main` at root. Pushing to `main` redeploys.

## Pages

| Page | What it is |
| --- | --- |
| `index.html` | StoryBrand home page: hero, the problem (three icon cards: external, internal, philosophical), Abby as guide in her first person, a three-step plan, rescue teaser, what is at stake, closing call to action |
| `aquarium-myths.html` | Aquarium myths vs. facts: four misconceptions, each with what the research shows and its AZA source |
| `rescue-and-conservation.html` | Rescue and rehabilitation, field conservation spending, what AZA accreditation checks, and simple ways to support marine conservation |
| `aquarium-directory.html` | Directory of U.S. aquariums and the animals, rescue programs and conservation work behind each one. Shows a "coming soon" state until entries are added |

## Editing

All four pages, `sitemap.xml` and `robots.txt` are generated. Change copy or facts in `build.py`, then run:

    python3 build.py

Styles live in `styles.css` and are minified and inlined by the build.

- Site name: change `SITE_NAME` at the top of `build.py`. Abby's other options were Sea Clearly, Clear Waters and Sea for Yourself. The repo name and URL stay `beyond-the-glass` unless the repo is renamed (then update `SITE`).
- Aquarium directory: add entries to `AQUARIUMS` in `build.py` (the keys are listed in the comment above it). Only use facts the aquarium itself or AZA has published. Once the list has entries, the page drops the "coming soon" block and renders a card per aquarium.
- Fonts: Fraunces (headings) and Source Sans 3 (body) are self-hosted in `fonts/` and subset to the characters the site uses. After adding new symbols or accented letters, run `python3 tools/subset_fonts.py` (needs `pip install fonttools brotli`). Full originals are in `tools/font-src/`.

## Rules this site follows

- Every fact comes from Abby's research doc, which cites the Association of Zoos & Aquariums. Nothing is invented. Sources are cited in plain text with no links: the site has zero external links.
- Hero photos show people. Photos have rounded corners and a light color pass.
- No em dashes, no small uppercase labels above headings, no bold phrases inside sentences.

## SEO and performance

- Lighthouse (local, 2026-10-08): 100 in performance, accessibility, best practices and SEO on all four pages, mobile and desktop.
- Each page has a canonical URL, Open Graph tags and JSON-LD (`WebSite`, `Person`, plus `WebPage`, `Article` or `CollectionPage`, and `BreadcrumbList`). All pages are in `sitemap.xml`.
- Hero images use `fetchpriority="high"`, a preload, `srcset` and explicit dimensions.

## Photos

All stock photos are from Unsplash under the Unsplash licence (free, no credit required). They were cropped and color-graded for the site.

| File | Used on | Unsplash ID | Subject |
| --- | --- | --- | --- |
| `images/hero-sea-lion-*.webp`, `images/og.jpg` | Home hero, social preview | `J_lJJ8di3B8` | Two girls watching a sea lion at the glass |
| `images/hero-rays-*.webp` | Myths hero | `Qn3c2MlM5DQ` | Two young visitors watching rays |
| `images/hero-walrus-*.webp` | Rescue hero | `SJBw8wCEO6Q` | A child face to face with a walrus |
| `images/hero-big-tank-*.webp` | Directory hero | `0RzzFmq64ek` | Crowd silhouetted at a giant tank |
| `images/turtle-blue-*.webp` | Home, Abby's section | `L-2p8fapOA8` | Sea turtle in blue water |
| `images/sea-turtle-*.webp` | Home rescue section, conservation section | `aGihPIbrtVE` | Sea turtle near the surface |
| `images/manatee-*.webp` | Rescue section | `8EXZXZrj3Tw` | Manatee swimming |

## Still needed from Abby

- Her own photos (from her Canva design) for the guide section, ideally one of her at an aquarium.
- Confirmation of the site name.
- The first aquarium directory entries.
- A read of the first-person copy in the guide section, which was adapted from her StoryBrand answer.
