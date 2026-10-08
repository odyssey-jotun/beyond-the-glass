# Beyond the Glass

Passion-project site for Abby McGowan: clear, sourced information on aquarium conservation, rescue and rehabilitation, animal welfare, and the most common aquarium myths. Built from Abby's "Aquarium Project" research doc and her StoryBrand answers.

## Live site

https://odyssey-jotun.github.io/beyond-the-glass/

The repository is public and GitHub Pages serves `main` at root. Pushing to `main` redeploys.

## Pages

| Page | What it is |
| --- | --- |
| `index.html` | StoryBrand home page: hero, the problem (three icon cards: external, internal, philosophical), Abby as guide in her first person, a three-step plan, rescue teaser, what is at stake, closing call to action |
| `aquarium-myths.html` | Aquarium myths vs. facts: five misconceptions, each with what the research shows and its AZA source |
| `rescue-and-conservation.html` | Rescue and rehabilitation, sea turtle rescue numbers (NOAA, AZA), field conservation spending, what AZA accreditation checks, and simple ways to support marine conservation |
| `manatees.html` | Manatee landing page: Abby's first-person section on why manatees are her favorite animal, then sourced facts (species, size, diet, lifespan, ESA status), threats with FWC numbers, how the Manatee Rescue & Rehabilitation Partnership works, links to the directory entries that help manatees, three ways to help (FWC hotline as a `tel:` link) |
| `aquarium-directory.html` | Directory of 16 AZA-accredited U.S. aquariums and zoos, grouped by region, with the animals each one helps, its rescue program and its conservation work. Entries that help manatees link to `manatees.html` |

## Editing

All five pages, `sitemap.xml` and `robots.txt` are generated. Change copy or facts in `build.py`, then run:

    python3 build.py

Styles live in `styles.css` and are minified and inlined by the build.

- Site name: change `SITE_NAME` at the top of `build.py`. Abby's other options were Sea Clearly, Clear Waters and Sea for Yourself. The repo name and URL stay `beyond-the-glass` unless the repo is renamed (then update `SITE`).
- Aquarium directory: entries live in `AQUARIUMS` in `build.py` (the keys are listed in the comment above it), grouped by `REGIONS`. Only use facts the aquarium itself, AZA or a federal or state wildlife agency has published, and put the year beside every number. Confirm accreditation on AZA's Find a Zoo or Aquarium list first (aza.org blocks plain scripted fetches; a real browser or Playwright loads it). Set `"manatees": True` to add a link to the manatee page.
- Manatee page: Abby's first-person section is written in her style from ideas in her writing, with no sentences taken from her college essay (college plagiarism checks could match published text). Before changing that section, check that no run of five or more words matches her essay.
- Fonts: Fraunces (headings) and Source Sans 3 (body) are self-hosted in `fonts/` and subset to the characters the site uses. After adding new symbols or accented letters, run `python3 tools/subset_fonts.py` (needs `pip install fonttools brotli`). Full originals are in `tools/font-src/`.

## Rules this site follows

- Every fact comes from Abby's research doc (which cites the Association of Zoos & Aquariums), from FWC, the U.S. Fish and Wildlife Service, NOAA Fisheries or USGS, or from the aquariums' own published pages. Nothing is invented. Sources are cited in plain text with no links: the site has zero external links.
- Hero photos show people. Photos have rounded corners and a light color pass.
- No em dashes, no small uppercase labels above headings, no bold phrases inside sentences.

## SEO and performance

- Lighthouse (local, 2026-10-08): 100 in performance, accessibility, best practices and SEO on all five pages, mobile and desktop.
- Each page has a canonical URL, Open Graph tags and JSON-LD (`WebSite`, `Person`, plus `WebPage`, `Article` or `CollectionPage`, and `BreadcrumbList`). All pages are in `sitemap.xml`.
- Hero images use `fetchpriority="high"`, a preload, `srcset` and explicit dimensions.

## Photos

Stock photos are from Unsplash under the Unsplash licence (free, no credit required), except the manatee hero, which is from Flickr under CC BY 2.0 and is credited on the page. All were cropped and color-graded for the site.

| File | Used on | Unsplash ID | Subject |
| --- | --- | --- | --- |
| `images/hero-sea-lion-*.webp`, `images/og.jpg` | Home hero, social preview | `J_lJJ8di3B8` | Two girls watching a sea lion at the glass |
| `images/hero-rays-*.webp` | Myths hero | `Qn3c2MlM5DQ` | Two young visitors watching rays |
| `images/hero-walrus-*.webp` | Rescue hero | `SJBw8wCEO6Q` | A child face to face with a walrus |
| `images/hero-big-tank-*.webp` | Directory hero | `0RzzFmq64ek` | Crowd silhouetted at a giant tank |
| `images/turtle-blue-*.webp` | Home, Abby's section | `L-2p8fapOA8` | Sea turtle in blue water |
| `images/sea-turtle-*.webp` | Home rescue section, conservation section | `aGihPIbrtVE` | Sea turtle near the surface |
| `images/manatee-*.webp` | Rescue section, manatee facts | `8EXZXZrj3Tw` | Manatee mother and calf (NOAA) |
| `images/hero-manatee-window-*.webp` | Manatee hero | Flickr 8423624578, "Benjamin Watches Manatees" by Eugene Kim, CC BY 2.0 | A boy watching two manatees at an aquarium window |
| `images/manatee-face-*.webp` | Manatee page, Abby's section | `muI8sLeCIY8` | Close view of a manatee's face |
| `images/manatee-care-*.webp` | Manatee page, rescue section | `GPqsrCEg7KY` | Manatee eating lettuce in an aquarium pool |
| `images/manatee-surface-*.webp` | Manatee page, how to help | `3-zLjbZf4Rs` | Three manatees at the surface |

## Still needed from Abby

- Her own photos (from her Canva design) for the guide section, ideally one of her at an aquarium.
- Confirmation of the site name.
- A read of the first-person copy in the home guide section (adapted from her StoryBrand answer) and in the manatee page's opening section (written in her style, not taken from her essay).
- Her own manatee photo, if she has one, to replace or join the stock hero.
- Directory entries she would like to add or drop. Left out on purpose: Clearwater Marine Aquarium (not on AZA's accredited list), Shedd Aquarium (its rescue pages could not be verified), Aquarium of the Pacific and Seattle Aquarium (verified, but held to keep the list focused).
- Note: the $230M+ field conservation figure comes from AZA's About Us page, which Abby cited. AZA's Zoo and Aquarium Statistics page now reports $341.1 million spent in 2024. Swap the figure if she wants the newer one.
