#!/usr/bin/env python3
"""Builds every page of Beyond the Glass.

Run: python3 build.py
The site name lives in SITE_NAME below. Change it there, rebuild, and every
page title, heading, wordmark, footer and JSON-LD block follows. Facts and
copy live in this file too, so a correction is made once.
"""
import json
import re
from html import escape

# ---------------------------------------------------------------- settings
SITE_NAME = "Beyond the Glass"
AUTHOR = "Abby McGowan"
SITE = "https://odyssey-jotun.github.io/beyond-the-glass/"
TODAY = "2026-10-08"

# The aquarium directory. Each entry is one aquarium Abby has researched.
# While this list is empty the directory page shows a "coming soon" state.
# Only add facts the aquarium itself (or AZA) has published, and fill every key:
# {"name": "", "city": "", "state": "", "accredited": True,
#  "animals": "", "rescue": "", "conservation": "", "source": ""}
AQUARIUMS = []

# Sources, cited in plain text. No links on purpose (see README).
AZA = "Association of Zoos &amp; Aquariums"
TITLES = {
    "about": "About Us",
    "conservation": "Conservation",
    "rescue": "Accountability Within the AZA Accreditation Process",
    "accreditation": "Accreditation",
    "what": "What Is Accreditation?",
    "becoming": "Becoming Accredited",
}
SOURCES = {k: f"{AZA}. <em>{v}</em>{'' if v.endswith('?') else '.'} aza.org." for k, v in TITLES.items()}

# ---------------------------------------------------------------- helpers
CSS = None


def css():
    """styles.css, minified and inlined so no stylesheet blocks first paint."""
    global CSS
    if CSS is None:
        t = open("styles.css").read()
        t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
        t = re.sub(r"\s+", " ", t)
        t = re.sub(r"\s*([{};:,>])\s*", r"\1", t).replace(";}", "}")
        CSS = t.strip()
    return CSS


def srcset(name, widths):
    return ", ".join(f"images/{name}-{w}.webp {w}w" for w in widths)


HERO_W = (600, 800, 960, 1200)
HOME_SIZES = "(max-width: 620px) calc(100vw - 40px), (max-width: 1136px) calc(100vw - 56px), 1080px"
PAGE_SIZES = "(max-width: 860px) calc(100vw - 40px), 500px"


def hero_img(name, alt, sizes, cls="hero-photo"):
    return (f'<figure class="{cls}"><img src="images/{name}-960.webp" srcset="{srcset(name, HERO_W)}" '
            f'sizes="{sizes}" width="1200" height="800" alt="{alt}" fetchpriority="high" decoding="async"></figure>')


def photo(name, alt, sizes="(max-width: 860px) calc(100vw - 40px), 520px"):
    return (f'<figure class="photo"><img src="images/{name}-900.webp" srcset="{srcset(name, (600, 900))}" '
            f'sizes="{sizes}" width="900" height="675" alt="{alt}" loading="lazy" decoding="async"></figure>')


PERSON = {
    "@type": "Person", "@id": SITE + "#abby", "name": AUTHOR,
    "description": f"High school senior and creator of {SITE_NAME}, a guide to aquarium conservation, animal welfare and common aquarium myths.",
    "url": SITE + "#about",
}


def head(title, desc, path="", schema=None, hero=None, sizes=HOME_SIZES):
    url = SITE + path
    graph = [{"@type": "WebSite", "@id": SITE + "#site", "url": SITE, "name": SITE_NAME,
              "description": "Clear, sourced information on aquarium conservation, rescue, animal welfare and common aquarium myths.",
              "author": {"@id": SITE + "#abby"}, "inLanguage": "en-US"}, PERSON]
    graph += schema or []
    preload = ""
    if hero:
        preload = (f'<link rel="preload" as="image" type="image/webp" href="images/{hero}-960.webp" '
                   f'imagesrcset="{srcset(hero, HERO_W)}" imagesizes="{sizes}" fetchpriority="high">\n')
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, separators=(",", ":"))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<meta name="author" content="{AUTHOR}">
<meta name="theme-color" content="#F7F3EA">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}images/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Two children watching a sea lion swim up to the glass of an aquarium">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
{preload}<link rel="preload" href="fonts/fraunces.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/source-sans.woff2" as="font" type="font/woff2" crossorigin>
<style>{css()}</style>
<script type="application/ld+json">{ld}</script>
</head>
<body>

<a class="skip" href="#main">Skip to content</a>
"""


def page_schema(kind, path, title, desc, extra=None):
    d = {"@type": kind, "@id": SITE + path + "#page", "url": SITE + path, "name": title, "headline": title,
         "description": desc, "isPartOf": {"@id": SITE + "#site"}, "author": {"@id": SITE + "#abby"},
         "inLanguage": "en-US", "datePublished": TODAY, "dateModified": TODAY,
         "image": SITE + "images/og.jpg"}
    d.update(extra or {})
    return d


def crumbs(name, path):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}


PAGES = [("index.html", "Home"), ("aquarium-myths.html", "Aquarium Myths"),
         ("rescue-and-conservation.html", "Rescue &amp; Conservation"), ("aquarium-directory.html", "Directory")]
# Nav labels; the .x part is hidden on narrow phones so the nav fits on one line.
NAV_LABELS = {"aquarium-myths.html": '<span class="x">Aquarium </span>Myths',
              "rescue-and-conservation.html": 'Rescue<span class="x"> &amp; Conservation</span>'}


def wordmark():
    words = SITE_NAME.split()
    if len(words) > 1:
        return f'<span>{" ".join(words[:-1])} <span class="last">{words[-1]}</span></span>'
    return f"<span>{SITE_NAME}</span>"


def nav(current):
    lis = []
    for href, label in PAGES:
        cur = ' aria-current="page"' if href == current else ""
        lis.append(f'      <li><a href="{href}"{cur}><span>{NAV_LABELS.get(href, label)}</span></a></li>')
    return f"""<nav class="site" aria-label="Primary">
  <div class="wrap">
    <a class="wordmark" href="index.html">{WAVE}{wordmark()}</a>
    <ul>
{chr(10).join(lis)}
    </ul>
  </div>
</nav>
"""


def foot():
    lis = "\n".join(f'      <li><a href="{h}">{l}</a></li>' for h, l in PAGES)
    return f"""
<footer>
  <div class="wrap">
    <p>{SITE_NAME}, a passion project by {AUTHOR}. Facts on this site come from the {AZA}.</p>
    <ul>
{lis}
    </ul>
  </div>
</footer>

</body>
</html>
"""


def sources(keys, heading="Sources"):
    lis = "\n".join(f"      <li>{SOURCES[k]}</li>" for k in keys)
    return f"""
<section class="refs" id="sources">
  <div class="wrap">
    <h2>{heading}</h2>
    <ol>
{lis}
    </ol>
  </div>
</section>
"""


def cta(heading, text, href, label):
    return f"""
<section class="closing">
  <div class="wrap">
    <h2>{heading}</h2>
    <p>{text}</p>
    <div class="btn-row"><a href="{href}" class="btn">{label}</a></div>
  </div>
</section>
"""


# ---------------------------------------------------------------- icons
def svg(body, vb="0 0 48 48", sw="2.6"):
    return (f'<svg viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{body}</svg>')


WAVE = ('<svg class="mark" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" fill="#0B4A57"/>'
        '<path d="M6 13c3.3 0 3.3-2.6 6.7-2.6s3.3 2.6 6.6 2.6 3.4-2.6 6.7-2.6M6 20.5c3.3 0 3.3-2.6 6.7-2.6s3.3 2.6 6.6 2.6 3.4-2.6 6.7-2.6" '
        'fill="none" stroke="#9ED8CC" stroke-width="2.4" stroke-linecap="round"/></svg>')
ICON_BADGE = svg('<circle cx="24" cy="19" r="11"/><path d="M19 19l3.5 3.5L29.5 15"/><path d="M17 28.5L14 43l10-5 10 5-3-14.5"/>')
ICON_QUESTION = svg('<path d="M8 10h32a3 3 0 013 3v18a3 3 0 01-3 3H22l-9 7v-7H8a3 3 0 01-3-3V13a3 3 0 013-3z"/>'
                    '<path d="M20 18a4 4 0 117 2.7c-1.4 1-3 1.8-3 3.8"/><path d="M24 28.5v.1"/>')
ICON_GLOBE = svg('<circle cx="24" cy="24" r="18"/><path d="M6 24h36M24 6c5 5 7.5 11 7.5 18S29 37 24 42c-5-5-7.5-11-7.5-18S19 11 24 6z"/>')
ICON_TURTLE = svg('<ellipse cx="22" cy="25" rx="13" ry="9.5"/><circle cx="39.5" cy="23" r="4"/>'
                  '<path d="M28 17.5l5-7M28 32.5l5 6.5M15 18l-5-5M15 32l-5 5M9 25H5M22 15.5v19M14 25h16"/>')
ICON_FLASK = svg('<path d="M19 6h10M21 6v12L10 38a3 3 0 002.6 4.5h22.8A3 3 0 0038 38L27 18V6"/><path d="M15 30h18"/>')
ICON_BOOK = svg('<path d="M6 10c6-2 12-1 18 3 6-4 12-5 18-3v28c-6-2-12-1-18 3-6-4-12-5-18-3z"/><path d="M24 13v28"/>')
CHECK = svg('<path d="M10 25l9 9 19-20"/>', sw="3.4")
CROSS = svg('<path d="M14 14l20 20M34 14L14 34"/>', sw="3.4")
ARROW = svg('<path d="M8 24h30M28 14l10 10-10 10"/>', sw="3")

CHECKS = {  # what an AZA accreditation inspection examines (aza.org, Accreditation)
    "Animal welfare": ICON_TURTLE,
    "Veterinary care": svg('<path d="M24 41s-15-8.5-15-20a8 8 0 0115-4 8 8 0 0115 4c0 11.5-15 20-15 20z"/><path d="M24 20v10M19 25h10"/>'),
    "Living environments": svg('<rect x="6" y="12" width="36" height="26" rx="3"/><path d="M6 30c5 0 5-3 10-3s5 3 10 3 5-3 10-3 5 3 6 3"/><circle cx="17" cy="21" r="2"/>'),
    "Nutrition": svg('<path d="M10 28c0-9 6-15 14-15s14 6 14 15H10z"/><path d="M6 33h36M24 13V8"/>'),
    "Conservation": ICON_GLOBE,
    "Safety": svg('<path d="M24 5l16 6v12c0 10-6.5 17.5-16 21C14.5 40.5 8 33 8 23V11z"/><path d="M17 24l5 5 9-10"/>'),
    "Education": ICON_BOOK,
}


# ---------------------------------------------------------------- home
def index():
    t = f"Aquarium Conservation, Rescue and Animal Welfare Facts | {SITE_NAME}"
    d = ("What accredited aquariums do for marine animals: rescue and rehabilitation, field conservation, "
         "research and animal welfare, plus the most common aquarium myths checked against the facts.")
    schema = [page_schema("WebPage", "", t, d, {"about": "Aquarium conservation and animal welfare"})]
    return head(t, d, "", schema, hero="hero-sea-lion") + nav("index.html") + f"""
<main id="main">

<header class="hero">
  <div class="wrap">
    <div class="hero-text">
      <h1>What aquariums really do for the animals behind the glass</h1>
      <p class="lede">{SITE_NAME} is a student-built guide to aquarium conservation, animal welfare and the rescue work most visitors never see. Every fact on it comes from the {AZA}.</p>
      <div class="btn-row center">
        <a href="aquarium-myths.html" class="btn">Read the aquarium myths</a>
        <a href="rescue-and-conservation.html" class="btn ghost">See the rescue work</a>
      </div>
    </div>
    {hero_img("hero-sea-lion", "Two young girls in pink sweaters watching a sea lion swim right up to the aquarium glass", HOME_SIZES, "hero-photo wide")}
  </div>
</header>

<section id="problem" class="band">
  <div class="wrap">
    <div class="section-head center">
      <h2>Aquariums are hard to judge from the visitor side of the glass</h2>
      <p>Families, teens and animal lovers walk through aquariums with questions the exhibits rarely answer.</p>
    </div>
    <div class="cards">
      <div class="card problem">
        <div class="icon">{ICON_BADGE}</div>
        <p class="num">About 10%</p>
        <h3>Animal care standards vary from place to place</h3>
        <p>An open door says nothing about accreditation. Only about one in ten USDA-licensed animal exhibitors is accredited by the {AZA}.</p>
        <p class="of">of USDA-licensed animal exhibitors are AZA-accredited</p>
      </div>
      <div class="card problem">
        <div class="icon">{ICON_QUESTION}</div>
        <h3>Conflicting stories leave animal lovers uneasy</h3>
        <p>Headlines, posts and documentaries disagree about aquariums. People who care about sea life end up unsure what to believe, and some feel uneasy about visiting at all.</p>
      </div>
      <div class="card problem">
        <div class="icon">{ICON_GLOBE}</div>
        <p class="num">$230M+</p>
        <h3>Conservation work this large deserves to be seen</h3>
        <p>Accredited zoos and aquariums fund field conservation for more than 800 species in 130 countries. Work on that scale belongs in the conversation about aquariums.</p>
        <p class="of">spent on field conservation every year</p>
      </div>
    </div>
    <p class="punch">Nobody should have to guess whether the animals behind the glass are well cared for.</p>
  </div>
</section>

<section id="about">
  <div class="wrap split">
    <div class="about-text">
      <h2>A high school senior's guide to aquarium research</h2>
      <p class="name-line">I'm {AUTHOR}, and sea life has fascinated me for as long as I can remember.</p>
      <p>I have always been curious about the world beyond what we can see. Over the years I have spent many hours watching documentaries, researching marine animals, and learning about marine life and conservation.</p>
      <p>That curiosity led me past the common misconceptions about aquariums and into the research behind them. I built {SITE_NAME} to share what I have learned and to help people see aquariums and marine conservation from a different perspective.</p>
    </div>
    {photo("turtle-blue", "A sea turtle gliding through clear blue water")}
  </div>
  <div class="wrap">
    <ul class="strip">
      <li><span class="n">4</span><span class="t">aquarium myths checked against AZA research</span></li>
      <li><span class="n">5 years</span><span class="t">between full AZA accreditation reviews</span></li>
      <li><span class="n">1+</span><span class="t">welfare assessment a year for animals at accredited institutions</span></li>
    </ul>
  </div>
</section>

<section id="plan" class="band">
  <div class="wrap">
    <div class="section-head center">
      <h2>How to separate aquarium myths from facts in three steps</h2>
      <p>Your next aquarium visit can teach you a lot more than the names of the fish.</p>
    </div>
    <ol class="steps">
      <li>
        <h3>Check the common myths</h3>
        <p>Read four things people often believe about aquariums, each set beside what the research shows.</p>
      </li>
      <li>
        <h3>Learn what happens off exhibit</h3>
        <p>See how responsible aquariums contribute to rescue, rehabilitation, research, education and conservation.</p>
      </li>
      <li>
        <h3>Support the work that protects sea life</h3>
        <p>Find simple ways to support marine conservation and make informed choices about where you spend a day.</p>
      </li>
    </ol>
    <div class="btn-row center">
      <a href="aquarium-myths.html" class="btn">Start with the aquarium myths</a>
    </div>
  </div>
</section>

<section id="rescue">
  <div class="wrap split flip">
    {photo("sea-turtle", "Close view of a sea turtle swimming near the surface in bright blue water")}
    <div>
      <h2>Sea turtle and manatee rescue starts at accredited aquariums</h2>
      <p>Some animals in aquariums arrived because they were rescued and needed professional care. Accredited institutions work with government agencies to rescue and rehabilitate wildlife, including sea turtles and manatees. Depending on an animal's condition, rehabilitation can eventually lead to release.</p>
      <p>The same institutions put more than $230 million a year into field conservation and study animal biology, health, behavior and habitats to help protect species in the wild.</p>
      <div class="btn-row center"><a href="rescue-and-conservation.html" class="btn ghost">See the rescue and conservation work</a></div>
    </div>
  </div>
</section>

<section id="stakes" class="after">
  <div class="wrap">
    <div class="section-head center">
      <h2>What changes when visitors know the facts about aquariums</h2>
    </div>
    <div class="stakes">
      <div class="stake">
        <h3>When myths keep spreading</h3>
        <ul class="outcomes">
          <li>{CROSS}<span>Misconceptions about aquariums travel further with every share.</span></li>
          <li>{CROSS}<span>People overlook the rescue, rehabilitation, research and education work done by responsible aquariums.</span></li>
          <li>{CROSS}<span>Visitors have no way to tell an accredited aquarium from one that has never been inspected.</span></li>
        </ul>
      </div>
      <div class="stake good">
        <h3>When visitors leave informed</h3>
        <ul class="outcomes">
          <li>{CHECK}<span>You understand what aquariums contribute to marine life and conservation.</span></li>
          <li>{CHECK}<span>You make educated decisions about which aquariums to visit and support.</span></li>
          <li>{CHECK}<span>You become more involved in protecting sea life.</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>
""" + cta("See aquariums from the other side of the glass",
          "Four common aquarium myths, each checked against the research. It takes about five minutes to read.",
          "aquarium-myths.html", "Read the aquarium myths") + sources(["about", "conservation", "rescue", "what", "becoming"]) + "\n</main>\n" + foot()


# ---------------------------------------------------------------- myths
MYTHS = [
    ("entertainment", "Aquariums only exist for entertainment.",
     "$230M+", "a year spent on field conservation by AZA-accredited zoos and aquariums",
     ["Conservation, scientific research and education are part of the missions and accreditation standards of many professional aquariums. The Association of Zoos &amp; Aquariums describes conservation as a priority of its accredited institutions.",
      "Aquariums also contribute research on animal biology, health, behavior, habitats and conservation. That research helps scientists understand species and how they can be protected in the wild."],
     ["conservation", "about"]),
    ("standards", "Every aquarium follows the same animal care standards.",
     "5 years", "until an accredited facility goes through the full accreditation process again",
     ["Accreditation is where the standards differ. AZA accreditation involves expert review and a multi-day inspection that examines animal welfare, veterinary care, living environments, nutrition, conservation, safety, education and other parts of an institution.",
      "Accredited facilities must go through the full process again every five years."],
     ["accreditation"]),
    ("accredited", "If an aquarium is open to the public, it must be AZA-accredited.",
     "About 10%", "of USDA-licensed animal exhibitors are AZA-accredited",
     ["Being open to the public and being accredited are two separate things. AZA says only about 10% of USDA-licensed animal exhibitors are AZA-accredited.",
      "That makes accreditation something a visitor can check before a visit, rather than assume."],
     ["what"]),
    ("tanks", "Animals in accredited aquariums are simply placed in tanks and displayed.",
     "1+ a year", "welfare assessments for each animal at an accredited institution",
     ["AZA standards look at far more than whether animals are fed. They consider health, nutrition, living environments, social groupings and enrichment intended to encourage natural behavior.",
      "AZA says animals at accredited institutions receive a welfare assessment at least once a year."],
     ["becoming"]),
]
KEYS = list(SOURCES)


def myths():
    t = f"Aquarium Myths vs. Facts: What the Research Shows | {SITE_NAME}"
    d = ("Four common aquarium myths checked against research from the Association of Zoos & Aquariums: "
         "entertainment, care standards, accreditation and animal welfare.")
    schema = [page_schema("Article", "aquarium-myths.html", t, d, {"about": "Common misconceptions about aquariums"}),
              crumbs("Aquarium Myths", "aquarium-myths.html")]
    used = []
    blocks = []
    for i, (slug, myth, num, numtxt, facts, refs) in enumerate(MYTHS, 1):
        for r in refs:
            if r not in used:
                used.append(r)
        cites = " and ".join(TITLES[r] for r in refs)
        paras = "\n".join(f"        <p>{p}</p>" for p in facts)
        blocks.append(f"""
    <article class="myth" id="{slug}">
      <div class="myth-q">
        <h2><span class="mi no">{CROSS}</span>Myth {i}: &ldquo;{myth}&rdquo;</h2>
      </div>
      <div class="myth-a">
        <h3><span class="mi yes">{CHECK}</span>What the research shows</h3>
        <p class="myth-num"><span class="n">{num}</span>{numtxt}</p>
{paras}
        <p class="cite-line">Source: {AZA}, {cites}{'' if cites.endswith('?') else '.'}</p>
      </div>
    </article>""")
    jump = "\n".join(f'      <li><a href="#{s}"><span>{i}</span>{m}</a></li>' for i, (s, m, *_r) in enumerate(MYTHS, 1))
    return head(t, d, "aquarium-myths.html", schema, hero="hero-rays", sizes=PAGE_SIZES) + nav("aquarium-myths.html") + f"""
<main id="main">

<header class="page-hero">
  <div class="wrap split">
    <div>
      <h1>Aquarium myths vs. facts: what the research shows</h1>
      <p class="lede">People repeat these four ideas about aquariums all the time. Here is each one beside what the {AZA} has published.</p>
    </div>
    {hero_img("hero-rays", "Two young visitors standing at a huge aquarium window as a pale ray swims past", PAGE_SIZES)}
  </div>
</header>

<section class="band tight">
  <div class="wrap">
    <h2 class="small-h">The four aquarium myths on this page</h2>
    <ol class="jump">
{jump}
    </ol>
  </div>
</section>

<section>
  <div class="wrap myths">
{"".join(blocks)}
  </div>
</section>
""" + cta("See the rescue work behind these facts",
          "How accredited aquariums help sea turtles, manatees and hundreds of other species, and what an accreditation inspection examines.",
          "rescue-and-conservation.html", "Read about rescue and conservation") + sources(used) + "\n</main>\n" + foot()


# ---------------------------------------------------------------- rescue + conservation
def rescue():
    t = f"Aquarium Rescue, Rehabilitation and Conservation Work | {SITE_NAME}"
    d = ("How accredited aquariums rescue and rehabilitate sea turtles and manatees, fund field conservation for "
         "800+ species, and earn AZA accreditation. Plus simple ways to support marine conservation.")
    schema = [page_schema("Article", "rescue-and-conservation.html", t, d, {"about": "Aquarium rescue, rehabilitation and conservation"}),
              crumbs("Rescue & Conservation", "rescue-and-conservation.html")]
    checks = "\n".join(f'      <li><span class="ci">{ic}</span>{name}</li>' for name, ic in CHECKS.items())
    return head(t, d, "rescue-and-conservation.html", schema, hero="hero-walrus", sizes=PAGE_SIZES) + nav("rescue-and-conservation.html") + f"""
<main id="main">

<header class="page-hero">
  <div class="wrap split">
    <div>
      <h1>Aquarium rescue, rehabilitation and conservation work</h1>
      <p class="lede">Much of what an accredited aquarium does happens away from the exhibits: rescuing injured animals, funding conservation in the field, and studying how to protect species in the wild.</p>
    </div>
    {hero_img("hero-walrus", "A child in a knit hat face to face with a walrus pressing its whiskers against the aquarium glass", PAGE_SIZES)}
  </div>
</header>

<section id="rescue">
  <div class="wrap split">
    <div>
      <h2>How aquariums help rescue and rehabilitate sea turtles and manatees</h2>
      <p>Some animals in aquariums arrived because they were rescued and needed professional care. Accredited institutions work with government agencies to rescue and rehabilitate wildlife, including sea turtles and manatees.</p>
      <p>Depending on the animal's condition and circumstances, rehabilitation may eventually lead to release.</p>
      <p class="cite-line">Source: {AZA}, Accountability Within the AZA Accreditation Process.</p>
    </div>
    {photo("manatee", "A manatee swimming toward the camera through green-blue water")}
  </div>
</section>

<section id="conservation" class="band">
  <div class="wrap split flip">
    {photo("sea-turtle", "A sea turtle swimming near the surface of bright blue water")}
    <div>
      <h2>Where accredited aquariums spend on field conservation</h2>
      <p>AZA-accredited zoos and aquariums take part in projects that protect threatened species and habitats, carry out scientific research, and fund conservation work in the wild.</p>
      <p>Their research covers animal biology, health, behavior, habitats and conservation, and it helps scientists understand species and how to protect them.</p>
      <p class="cite-line">Sources: {AZA}, About Us and Conservation.</p>
    </div>
  </div>
  <div class="wrap">
    <ul class="strip">
      <li><span class="n">$230M+</span><span class="t">spent on field conservation every year</span></li>
      <li><span class="n">800+</span><span class="t">species helped by those projects</span></li>
      <li><span class="n">130</span><span class="t">countries where the projects take place</span></li>
    </ul>
  </div>
</section>

<section id="accreditation">
  <div class="wrap">
    <div class="section-head">
      <h2>What AZA accreditation checks at an aquarium</h2>
      <p>Accreditation means expert review and a multi-day inspection. Inspectors examine these parts of an institution, among others.</p>
    </div>
    <ul class="checks">
{checks}
    </ul>
    <div class="cards two">
      <div class="card">
        <p class="num">Every 5 years</p>
        <h3>The full review starts over</h3>
        <p>Accredited facilities go through the entire accreditation process again every five years.</p>
      </div>
      <div class="card">
        <p class="num">At least yearly</p>
        <h3>Each animal's welfare is assessed</h3>
        <p>Animals at accredited institutions receive a welfare assessment at least once a year, covering health, nutrition, living environments, social groupings and enrichment that encourages natural behavior.</p>
      </div>
    </div>
    <p class="cite-line">Sources: {AZA}, Accreditation and Becoming Accredited.</p>
  </div>
</section>

<section id="support" class="band">
  <div class="wrap">
    <div class="section-head">
      <h2>Simple ways to support marine conservation</h2>
      <p>None of these take more than a few minutes, and each one helps responsible aquariums do more of this work.</p>
    </div>
    <ol class="steps">
      <li>
        <h3>Check accreditation before you visit</h3>
        <p>Only about one in ten USDA-licensed animal exhibitors is AZA-accredited. Look it up before you buy a ticket.</p>
      </li>
      <li>
        <h3>Ask about rescue and conservation</h3>
        <p>Ask staff which animals the aquarium helps and which conservation projects it supports. The directory on this site will collect those answers.</p>
      </li>
      <li>
        <h3>Correct a myth when you hear one</h3>
        <p>Share what you learned here the next time someone says aquariums are only for entertainment.</p>
      </li>
    </ol>
  </div>
</section>
""" + cta("Find out what each aquarium does",
          "A directory of U.S. aquariums and the animals, rescue programs and conservation projects behind each one.",
          "aquarium-directory.html", "Open the aquarium directory") + sources(["rescue", "about", "conservation", "accreditation", "becoming", "what"]) + "\n</main>\n" + foot()


# ---------------------------------------------------------------- directory
FIELDS = [
    ("Animals this aquarium helps", ICON_TURTLE, "The species the aquarium rescues, rehabilitates or protects, such as sea turtles, seals or manatees."),
    ("Rescue and rehabilitation program", svg('<path d="M24 41s-15-8.5-15-20a8 8 0 0115-4 8 8 0 0115 4c0 11.5-15 20-15 20z"/><path d="M24 20v10M19 25h10"/>'),
     "What the aquarium actually does when an injured or stranded animal comes in, and whether animals are released."),
    ("Conservation work", ICON_GLOBE, "The field projects and research the aquarium supports, in the wild and on site."),
]


def entry_card(a):
    yes = "AZA-accredited" if a.get("accredited") else "Not AZA-accredited"
    rows = "\n".join(f'        <div class="field"><span class="fi">{ic}</span><h4>{lab}</h4><p>{escape(a[k])}</p></div>'
                     for (lab, ic, _), k in zip(FIELDS, ("animals", "rescue", "conservation")))
    return f"""
    <article class="entry">
      <div class="entry-head"><h3>{escape(a["name"])}</h3><p>{escape(a["city"])}, {escape(a["state"])} &middot; {yes}</p></div>
{rows}
      <p class="cite-line">Source: {escape(a["source"])}</p>
    </article>"""


def directory():
    t = f"U.S. Aquarium Directory: Rescue and Conservation Programs | {SITE_NAME}"
    d = ("A directory of U.S. aquariums and the animals they help, their rescue and rehabilitation programs, "
         "and the conservation work they support. Entries are being researched now.")
    schema = [page_schema("CollectionPage", "aquarium-directory.html", t, d, {"about": "Aquarium rescue and conservation programs in the United States"}),
              crumbs("Aquarium Directory", "aquarium-directory.html")]
    fields = "\n".join(f'      <li><span class="fi">{ic}</span><div><h3>{lab}</h3><p>{txt}</p></div></li>' for lab, ic, txt in FIELDS)
    if AQUARIUMS:
        body = '<div class="entries">' + "".join(entry_card(a) for a in AQUARIUMS) + "\n    </div>"
    else:
        ghost = "".join(f"""
      <div class="entry ghost" aria-hidden="true">
        <div class="entry-head"><span class="bar w60"></span><span class="bar w35"></span></div>
        <div class="field"><span class="fi">{FIELDS[0][1]}</span><span class="bar w80"></span></div>
        <div class="field"><span class="fi">{FIELDS[1][1]}</span><span class="bar w70"></span></div>
        <div class="field"><span class="fi">{FIELDS[2][1]}</span><span class="bar w75"></span></div>
      </div>""" for _ in range(3))
        body = f"""<div class="soon">
      <h2>The first aquarium entries are on the way</h2>
      <p>I am researching the first aquariums now. Each entry will be checked against what the aquarium and the {AZA} have published before it appears here.</p>
    </div>
    <div class="entries">{ghost}
    </div>"""
    return head(t, d, "aquarium-directory.html", schema, hero="hero-big-tank", sizes=PAGE_SIZES) + nav("aquarium-directory.html") + f"""
<main id="main">

<header class="page-hero">
  <div class="wrap split">
    <div>
      <h1>U.S. aquarium directory: rescue and conservation programs</h1>
      <p class="lede">Most aquarium listings stop at the address and ticket price. This directory records what each aquarium does for marine animals.</p>
    </div>
    {hero_img("hero-big-tank", "A crowd of visitors silhouetted against a giant aquarium window full of fish and a manta ray", PAGE_SIZES)}
  </div>
</header>

<section>
  <div class="wrap">
    {body}
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <h2>What each aquarium entry will cover</h2>
      <p>Every listing answers the same three questions, so two aquariums are easy to compare.</p>
    </div>
    <ul class="fields">
{fields}
    </ul>
  </div>
</section>
""" + cta("Read the facts while the directory grows",
          "Four common aquarium myths, each checked against the research.",
          "aquarium-myths.html", "Read the aquarium myths") + "\n</main>\n" + foot()


def sitemap():
    urls = "\n".join(f"  <url><loc>{SITE}{'' if h == 'index.html' else h}</loc><lastmod>{TODAY}</lastmod></url>" for h, _ in PAGES)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'


if __name__ == "__main__":
    out = {"index.html": index, "aquarium-myths.html": myths,
           "rescue-and-conservation.html": rescue, "aquarium-directory.html": directory}
    for name, fn in out.items():
        with open(name, "w") as f:
            f.write(fn())
        print("wrote", name)
    with open("sitemap.xml", "w") as f:
        f.write(sitemap())
    with open("robots.txt", "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")
