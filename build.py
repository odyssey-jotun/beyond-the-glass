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

# The aquarium directory. Each entry is one aquarium with a real rescue or
# rehabilitation program. While this list is empty the directory page shows a
# "coming soon" state. Only add facts the aquarium itself, AZA or a federal or
# state wildlife agency has published, put the year beside every number, and
# fill every key:
# {"id": "", "region": "", "name": "", "city": "", "state": "", "accredited": True,
#  "manatees": False, "animals": "", "rescue": "", "conservation": "", "source": ""}
# "region" must be one of REGIONS. "manatees": True adds a link to manatees.html.
# Accreditation for every entry below was checked on AZA's Find a Zoo or
# Aquarium list (241 accredited institutions as of September 2026).
REGIONS = ["Northeast and Mid-Atlantic", "Southeast", "Florida", "Gulf Coast", "Midwest", "West Coast and Alaska"]
AQUARIUMS = [
    {"id": "new-england-aquarium", "region": "Northeast and Mid-Atlantic", "name": "New England Aquarium",
     "city": "Boston", "state": "Massachusetts", "accredited": True, "manatees": False,
     "animals": "Cold-stunned Kemp's ridley, green and loggerhead sea turtles.",
     "rescue": "Its Sea Turtle Hospital at the Quincy Animal Care Center treats sea turtles stranded by cold water on Cape Cod, a partnership with Mass Audubon's Wellfleet Bay Wildlife Sanctuary that has run for more than 35 years. The hospital admitted 473 turtles in 2025, and close to 85% of its turtle patients are released back into the ocean.",
     "conservation": "Its Anderson Cabot Center for Ocean Life studies sea turtles and right whales. In 2023 the team tagged 14 rehabilitated sea turtles to follow them after release.",
     "source": "New England Aquarium, Sea Turtle Rescue and Rehabilitation; New England Aquarium, 2023 Annual Report."},
    {"id": "mystic-aquarium", "region": "Northeast and Mid-Atlantic", "name": "Mystic Aquarium",
     "city": "Mystic", "state": "Connecticut", "accredited": True, "manatees": False,
     "animals": "Mostly seals (harbor, gray, harp and occasionally hooded), plus other stranded marine mammals and sea turtles.",
     "rescue": "Its Animal Rescue Program has rescued, rehabilitated and released sick, injured and stranded marine animals since 1975, along 1,000 miles of coastline in Connecticut, Rhode Island and Fishers Island, New York. The team works with NOAA Fisheries and answers an average of 150 hotline calls a year.",
     "conservation": "Takes part in AZA's SAFE: Saving Animals From Extinction programs for African penguins, coral reefs, sea turtles, and sharks and rays, and studies beluga whale health.",
     "source": "Mystic Aquarium, Animal Rescue Program; Mystic Aquarium, Saving Endangered Species."},
    {"id": "national-aquarium", "region": "Northeast and Mid-Atlantic", "name": "National Aquarium",
     "city": "Baltimore", "state": "Maryland", "accredited": True, "manatees": True,
     "animals": "Harbor, gray, harp and hooded seals; Kemp's ridley, green and loggerhead sea turtles. It has also returned a harbor porpoise, a pygmy sperm whale and a manatee to the wild.",
     "rescue": "National Aquarium Animal Rescue has rescued and rehabilitated endangered and protected marine species since 1991. It holds NOAA and U.S. Fish and Wildlife Service permits to respond to sick and injured sea turtles and marine mammals along Maryland's 3,190 miles of coastline, and has run a Stranding Response Center in Ocean City since 2023.",
     "conservation": "Works year-round with the Greater Atlantic Region Stranding Network, and has returned hundreds of rehabilitated animals to their natural habitats since 1991.",
     "source": "National Aquarium, Animal Rescue."},
    {"id": "north-carolina-aquarium-roanoke-island", "region": "Southeast", "name": "North Carolina Aquarium on Roanoke Island",
     "city": "Manteo", "state": "North Carolina", "accredited": True, "manatees": False,
     "animals": "Loggerhead, green and Kemp's ridley sea turtles, the most common species in North Carolina.",
     "rescue": "Its Sea Turtle Assistance and Rehabilitation (STAR) Center, built in 2014, treats cold-stunned and injured turtles with partners such as the Network for Endangered Sea Turtles. In a single week of December 2024, 553 cold-stunned sea turtles were delivered to the aquarium. By December 17 it had received 576 and released 399.",
     "conservation": "Works under a N.C. Wildlife Resources Commission sea turtle permit alongside Cape Hatteras National Seashore and U.S. Coast Guard stations. Every sea turtle it treats is protected by the Endangered Species Act.",
     "source": "North Carolina Aquariums, 399 Sea Turtles Rescued, Rehabilitated, and Released Thanks to Community Partnerships (2024); North Carolina Aquarium on Roanoke Island, About."},
    {"id": "south-carolina-aquarium", "region": "Southeast", "name": "South Carolina Aquarium",
     "city": "Charleston", "state": "South Carolina", "accredited": True, "manatees": False,
     "animals": "Sea turtles, including loggerheads, greens and Kemp's ridleys.",
     "rescue": "Its Sea Turtle Care Center is a working hospital. With the South Carolina Department of Natural Resources, the aquarium rescues, rehabilitates and releases dozens of sea turtles each year that arrive with injuries and illness.",
     "conservation": "Part of AZA's Sea Turtle SAFE program, with citizen science projects (Sea Turtle Guardian and Tangled in Trash) and work on plastic pollution and sustainable seafood.",
     "source": "South Carolina Aquarium, Conservation; South Carolina Aquarium, Sea Turtle Care Center."},
    {"id": "georgia-aquarium", "region": "Southeast", "name": "Georgia Aquarium",
     "city": "Atlanta", "state": "Georgia", "accredited": True, "manatees": True,
     "animals": "Cold-stunned loggerhead and Kemp's ridley sea turtles, and manatees.",
     "rescue": "The aquarium has taken in over 40 cold-stunned sea turtles in the past five years (2025) and keeps space to rehabilitate loggerheads and return them to the wild. As a Manatee Rescue &amp; Rehabilitation Partnership member it also cares for manatees: one, Lorenzo, arrived weighing under 300 pounds and was released in February 2026 at 639 pounds.",
     "conservation": "Researches whale sharks, bottlenose dolphins, African penguins, manta rays, corals, belugas, manatees and sea lions, and studies algal toxins in Arctic walruses.",
     "source": "Georgia Aquarium, Conservation Works When We Work Together (2025); Georgia Aquarium, Manatee Rehabilitation: From Rescue to Release (2026)."},
    {"id": "seaworld-orlando", "region": "Florida", "name": "SeaWorld Orlando",
     "city": "Orlando", "state": "Florida", "accredited": True, "manatees": True,
     "animals": "Manatees, sea turtles, birds, dolphins and other marine mammals.",
     "rescue": "One of the critical care facilities for manatees in Florida. The most serious cases are treated in its medical pools before the Manatee Rescue &amp; Rehabilitation Partnership moves recovering manatees to other facilities. SeaWorld has rescued more than 670 manatees over its history (2018). In 2016 the Orlando rescue team answered 701 calls and cared for 32 manatees, 82 sea turtles and reptiles, 8 cetaceans and 579 birds.",
     "conservation": "The SeaWorld Conservation Fund, set up in 2003, has given more than $20 million to nearly 1,400 organizations (2026).",
     "source": "SeaWorld Orlando, Toxic Algae Bloom: Rescuing Florida's Manatees (2018); SeaWorld, Rescue and Rehab Results; Manatee Rescue &amp; Rehabilitation Partnership, FAQs; SeaWorld Orlando AZA accreditation release (2026)."},
    {"id": "florida-aquarium", "region": "Florida", "name": "The Florida Aquarium",
     "city": "Tampa", "state": "Florida", "accredited": True, "manatees": False,
     "animals": "Sea turtles, including turtles stunned by cold water.",
     "rescue": "Its Sea Turtle Rehabilitation Center opened in January 2019 at the Apollo Beach Conservation Campus, with a veterinary hospital and 12 recovery pools. Annual turtle intakes have grown 330% since opening, it took in 75 patients in 2025, and it has cared for more than 200 turtles in all (January 2026).",
     "conservation": "Its Coral Conservation &amp; Research Center, opened in March 2024, has spawned 14 coral species. In December 2021 the aquarium reared and released nearly 200 long-spined sea urchins off the Florida coast.",
     "source": "The Florida Aquarium, Honored as Lightning Community Hero for Sea Turtle Conservation Program (2026); The Florida Aquarium, Our Conservation Campus; About Us."},
    {"id": "mote-marine-laboratory", "region": "Florida", "name": "Mote Marine Laboratory &amp; Aquarium",
     "city": "Sarasota", "state": "Florida", "accredited": True, "manatees": True,
     "animals": "Sea turtles, dolphins and whales, and manatees.",
     "rescue": "Its Stranding Investigations Program responds 24 hours a day to sick, injured and dead marine mammals and sea turtles in Southwest Florida, mainly Sarasota and Manatee counties, and has recovered more than 2,000 turtles since 2003. Mote runs a Sea Turtle Rehabilitation Hospital and a Dolphin and Whale Hospital, and in May 2025 it became a federally designated secondary care facility for rescued manatees.",
     "conservation": "Necropsies of stranded animals help explain causes of death, including vessel strikes. Its goal for every patient is a return to the ocean.",
     "source": "Mote Marine Laboratory &amp; Aquarium, Stranding Investigations; Mote, Federal Designation as a Secondary Care Rehabilitation Facility for Rescued Manatees (2025)."},
    {"id": "audubon-aquarium", "region": "Gulf Coast", "name": "Audubon Aquarium",
     "city": "New Orleans", "state": "Louisiana", "accredited": True, "manatees": True,
     "animals": "Bottlenose dolphins; green, hawksbill, Kemp's ridley, leatherback and loggerhead sea turtles; West Indian manatees.",
     "rescue": "Audubon Aquarium Rescue is the only group in Louisiana responsible for rehabilitating live marine mammals and sea turtles, authorized by the U.S. Fish and Wildlife Service and NOAA. In 2023 it released nine Kemp's ridley sea turtles that had been stunned by cold water in Massachusetts.",
     "conservation": "Serves as NOAA Fisheries' main stranding response partner for marine mammals and sea turtles in Louisiana (2023), and funds dolphin protection through its Protect Wild Dolphins license plate.",
     "source": "Audubon Nature Institute, Audubon Aquarium Rescue; Audubon Coastal Wildlife Network Releases Nine Kemp's Ridley Sea Turtles (2023)."},
    {"id": "texas-state-aquarium", "region": "Gulf Coast", "name": "Texas State Aquarium",
     "city": "Corpus Christi", "state": "Texas", "accredited": True, "manatees": True,
     "animals": "Marine mammals, manatees, sea turtles, raptors and shorebirds.",
     "rescue": "The Port Corpus Christi Center for Wildlife Rescue is the largest coastal wildlife rescue facility in Texas and the only rescue program in the state permitted to receive marine mammals, manatees, sea turtles and birds. Since 1995 the aquarium has admitted over 8,700 animals and released over 4,000.",
     "conservation": "Endangered species are a large share of the work: 2,855 of the animals admitted since 1995 were endangered. The center also has the only CAT scanner in Texas used just for wildlife.",
     "source": "Texas State Aquarium, Wildlife Rescue Press Packet."},
    {"id": "columbus-zoo", "region": "Midwest", "name": "Columbus Zoo and Aquarium",
     "city": "Powell", "state": "Ohio", "accredited": True, "manatees": True,
     "animals": "West Indian manatees.",
     "rescue": "A Manatee Rescue &amp; Rehabilitation Partnership member since 1999 and a second-stage rehabilitation facility. Manatees live in its 300,000-gallon Manatee Coast pool until they are ready to return to Florida waters. In 2019 it welcomed its 30th and 31st manatees.",
     "conservation": "Contributes $4 million a year in privately raised funds to conservation projects worldwide (2019), including field work for three of the four living manatee species.",
     "source": "Columbus Zoo and Aquarium, Manatee Rescue and Rehabilitation Partnership; Columbus Zoo and Aquarium Welcomes Two Orphaned Manatees (2019)."},
    {"id": "cincinnati-zoo", "region": "Midwest", "name": "Cincinnati Zoo &amp; Botanical Garden",
     "city": "Cincinnati", "state": "Ohio", "accredited": True, "manatees": True,
     "animals": "Manatees, cared for at its Manatee Springs habitat.",
     "rescue": "Manatees rescued in Florida by FWC and partners recover at Manatee Springs before going home. The zoo has rehabilitated 35 manatees since 1999, and three of them went back to Florida waters in February 2026 as part of a release of more than 20 manatees.",
     "conservation": "Known for protecting and breeding endangered animals and plants, with research and conservation projects around the world.",
     "source": "Cincinnati Zoo &amp; Botanical Garden, Mass Manatee Release Includes Three Former Cincinnati Zoo Residents (2026)."},
    {"id": "monterey-bay-aquarium", "region": "West Coast and Alaska", "name": "Monterey Bay Aquarium",
     "city": "Monterey", "state": "California", "accredited": True, "manatees": False,
     "animals": "Southern sea otters, both stranded adults and orphaned pups.",
     "rescue": "Its Sea Otter Program has cared for more than 1,000 stranded sea otters over 40 years. Since 2001 it has paired orphaned pups with exhibit otters that raise them as surrogate mothers, and 84 pups have been raised this way. Nearly 300 otters have been released back to the wild (2025).",
     "conservation": "Between 2001 and 2016 it released 37 surrogate-raised otters in Elkhorn Slough, and those otters and their offspring accounted for more than half of that area's population growth. Its Seafood Watch program has guided sustainable seafood choices since 1999.",
     "source": "Monterey Bay Aquarium, Sea Otter Recovery Program; A History of Our Sea Otter Program; Our History."},
    {"id": "oregon-coast-aquarium", "region": "West Coast and Alaska", "name": "Oregon Coast Aquarium",
     "city": "Newport", "state": "Oregon", "accredited": True, "manatees": False,
     "animals": "Pacific green and olive ridley sea turtles, seabirds and shorebirds, including endangered snowy plovers.",
     "rescue": "It is one of three wildlife rehabilitation facilities in the Pacific Northwest, and the only one in Oregon, authorized by the U.S. Fish and Wildlife Service to care for endangered marine life. Sea turtles that strand in winter are treated with the Oregon Marine Mammal Stranding Network, and staff free birds tangled in fishing line and plastic.",
     "conservation": "Surveys sevengill sharks with AZA partners, treats sea star wasting disease and monitors sunflower stars, and serves as the official dive team for the Oregon Marine Reserve Program.",
     "source": "Oregon Coast Aquarium, Animal Rehabilitation; Conservation Efforts at the Aquarium and Beyond."},
    {"id": "alaska-sealife-center", "region": "West Coast and Alaska", "name": "Alaska SeaLife Center",
     "city": "Seward", "state": "Alaska", "accredited": True, "manatees": False,
     "animals": "Harbor, ringed, spotted and bearded seals, northern fur seals, sea otters, walruses, beluga whales and seabirds.",
     "rescue": "Its Wildlife Response Program answers calls about abandoned, stranded and injured marine wildlife across Alaska. It is the only permanent marine mammal rescue and rehabilitation facility in the state, working under NOAA and U.S. Fish and Wildlife Service permits.",
     "conservation": "Since opening in 1998 its scientists have published close to 400 journal articles, with long-running work on Steller sea lions, harbor seals, sea otters and eiders.",
     "source": "Alaska SeaLife Center, About Us; Wildlife Response Overview; Science and Research Overview."},
]

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
TITLES.update({"managed": "Reimagining the Animal Management Puzzle", "benefits": "Why Zoos and Aquariums Are Beneficial"})
FWC = "Florida Fish and Wildlife Conservation Commission"
USFWS = "U.S. Fish and Wildlife Service"
NOAA = "NOAA Fisheries"
SOURCES.update({
    "find": f"{AZA}. <em>Find a Zoo or Aquarium Near Me.</em> aza.org, September 2026.",
    "managed": f"{AZA}. <em>Reimagining the Animal Management Puzzle.</em> aza.org, 2019.",
    "aza-turtles": f"{AZA}. <em>Sea Turtle Rescue.</em> aza.org, 2021.",
    "noaa-turtles": f"{NOAA}. <em>Sea Turtles.</em> fisheries.noaa.gov.",
    "noaa-coldstun": f"{NOAA}. <em>Rescuing Cold Stunned Sea Turtles in St Joseph Bay, Florida.</em> fisheries.noaa.gov, 2026.",
    "fws-manatee": f"{USFWS}. <em>Manatee (Trichechus manatus).</em> fws.gov.",
    "fws-2017": f"{USFWS}. <em>Manatee Reclassified from Endangered to Threatened as Habitat Improves and Population Expands.</em> fws.gov, March 30, 2017.",
    "fws-2025": f"{USFWS}. <em>U.S. Fish and Wildlife Service Publishes Finding on Two West Indian Manatee Petitions.</em> fws.gov, January 13, 2025.",
    "fws-village": f"{USFWS}. <em>It Takes a Village to Save Manatees.</em> fws.gov, May 15, 2023.",
    "usgs-sirenia": "U.S. Geological Survey. <em>Florida Manatees</em> (Lefebvre and O'Shea). usgs.gov, 1995.",
    "fwc-profile": f"{FWC}. <em>Aquatic Mammals: Manatee.</em> myfwc.com.",
    "fwc-2025": f"{FWC}. <em>2025 Manatee Mortality in Review.</em> myfwc.com.",
    "fwc-2021": f"{FWC}. <em>Manatee Mortality Table by County, 2021 Final.</em> myfwc.com.",
    "fwc-ume": f"{FWC}. <em>Closed Manatee Mortality Event Along the East Coast.</em> myfwc.com.",
    "fwc-rescue": f"{FWC}. <em>Manatee Rescue Statistics</em> (2024 and 2025 preliminary rescue summaries). myfwc.com.",
    "fwc-help": f"{FWC}. <em>Florida Manatee: How to Help; Viewing Guidelines; Living with Florida Manatees.</em> myfwc.com.",
    "benefits": f"{AZA}. <em>Why Zoos and Aquariums Are Beneficial.</em> aza.org.",
    "mrp": "Manatee Rescue &amp; Rehabilitation Partnership. <em>FAQs.</em> manateerescue.org.",
})

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
         ("rescue-and-conservation.html", "Rescue &amp; Conservation"), ("manatees.html", "Manatees"),
         ("aquarium-directory.html", "Directory")]
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
    <p>{SITE_NAME}, a passion project by {AUTHOR}. Facts on this site come from the {AZA}, federal and state wildlife agencies, and the aquariums themselves.</p>
    <ul>
{lis}
    </ul>
  </div>
</footer>

</body>
</html>
"""


def sources(keys, heading="Sources", note=""):
    lis = "\n".join(f"      <li>{SOURCES[k]}</li>" for k in keys)
    note = f'\n    <p class="cite-line">{note}</p>' if note else ""
    return f"""
<section class="refs" id="sources">
  <div class="wrap">
    <h2>{heading}</h2>
    <ol>
{lis}
    </ol>{note}
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
ICON_HEART = svg('<path d="M24 41s-15-8.5-15-20a8 8 0 0115-4 8 8 0 0115 4c0 11.5-15 20-15 20z"/>')
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
      <p class="lede">{SITE_NAME} is a student-built guide to aquarium conservation, animal welfare and the rescue work most visitors never see. Every fact on it comes from the {AZA}, federal and state wildlife agencies, or the aquariums themselves.</p>
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
      <li><span class="n">{len(MYTHS)}</span><span class="t">aquarium myths checked against AZA research</span></li>
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
        <p>Read {WORDS[len(MYTHS)]} things people often believe about aquariums, each set beside what the research shows.</p>
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
          f"{WORDS[len(MYTHS)].capitalize()} common aquarium myths, each checked against the research. It takes about five minutes to read.",
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
    ("wild", "Most animals in aquariums were taken from the ocean.",
     "Most", "animals at AZA-accredited zoos and aquariums today were born in human care",
     ["In 2019 AZA reported that most animals in AZA-accredited zoos and aquariums today were born in managed care, meaning in a zoo or aquarium.",
      "Some animals did come from the wild, including rescued animals. AZA-accredited zoos and aquariums frequently work with the U.S. Fish and Wildlife Service to rescue, rehabilitate and care for wild animals such as sea turtles, manatees and sea otters until they can be released."],
     ["managed", "benefits"]),
]
WORDS = {4: "four", 5: "five", 6: "six"}


def myths():
    t = f"Aquarium Myths vs. Facts: What the Research Shows | {SITE_NAME}"
    d = (f"{WORDS[len(MYTHS)].capitalize()} common aquarium myths checked against research from the Association of Zoos & Aquariums: "
         "entertainment, care standards, accreditation, animal welfare and where aquarium animals come from.")
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
      <p class="lede">People repeat these {WORDS[len(MYTHS)]} ideas about aquariums all the time. Here is each one beside what the {AZA} has published.</p>
    </div>
    {hero_img("hero-rays", "Two young visitors standing at a huge aquarium window as a pale ray swims past", PAGE_SIZES)}
  </div>
</header>

<section class="band tight">
  <div class="wrap">
    <h2 class="small-h">The {WORDS[len(MYTHS)]} aquarium myths on this page</h2>
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

<section id="sea-turtles" class="band">
  <div class="wrap">
    <div class="section-head">
      <h2>Sea turtle rescue by the numbers</h2>
      <p>Cold water is one of the biggest reasons sea turtles need rescue. Turtles can become cold stunned when the water falls below 50 degrees Fahrenheit, and rescue teams move them to rehabilitation facilities to recover.</p>
    </div>
    <ul class="strip">
      <li><span class="n">6</span><span class="t">sea turtle species live in U.S. waters, and every one is protected under the Endangered Species Act</span></li>
      <li><span class="n">600+</span><span class="t">cold-stunned sea turtles rescued from St. Joseph Bay, Florida, in February 2026</span></li>
      <li><span class="n">12,000+</span><span class="t">sea turtles recovered in Texas in February 2021, the largest cold stun event in U.S. history</span></li>
    </ul>
    <p class="cite-line">Sources: {NOAA}, Sea Turtles and Rescuing Cold Stunned Sea Turtles in St Joseph Bay, Florida (2026); {AZA}, Sea Turtle Rescue (2021).</p>
  </div>
</section>

<section id="conservation">
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

<section id="accreditation" class="band">
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

<section id="support">
  <div class="wrap">
    <div class="section-head">
      <h2>Simple ways to support marine conservation</h2>
      <p>None of these take more than a few minutes, and each one helps responsible aquariums do more of this work.</p>
    </div>
    <ol class="steps">
      <li>
        <h3>Check accreditation before you visit</h3>
        <p>Only about one in ten USDA-licensed animal exhibitors is AZA-accredited. AZA's Find a Zoo or Aquarium list names all 241 accredited institutions (September 2026) and can be searched by zip code.</p>
      </li>
      <li>
        <h3>Ask about rescue and conservation</h3>
        <p>Ask staff which animals the aquarium helps and which conservation projects it supports. The <a href="aquarium-directory.html">aquarium directory</a> on this site already answers that for 16 aquariums and zoos.</p>
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
          "aquarium-directory.html", "Open the aquarium directory") + sources(["rescue", "about", "conservation", "accreditation", "becoming", "what", "find", "noaa-turtles", "noaa-coldstun", "aza-turtles"]) + "\n</main>\n" + foot()


# ---------------------------------------------------------------- directory
FIELDS = [
    ("Animals this aquarium helps", ICON_TURTLE, "The species the aquarium rescues, rehabilitates or protects, such as sea turtles, seals or manatees."),
    ("Rescue and rehabilitation program", svg('<path d="M24 41s-15-8.5-15-20a8 8 0 0115-4 8 8 0 0115 4c0 11.5-15 20-15 20z"/><path d="M24 20v10M19 25h10"/>'),
     "What the aquarium actually does when an injured or stranded animal comes in, and whether animals are released."),
    ("Conservation work", ICON_GLOBE, "The field projects and research the aquarium supports, in the wild and on site."),
]


def region_id(r):
    return re.sub(r"[^a-z]+", "-", r.lower()).strip("-")


def entry_card(a):
    yes = "AZA-accredited" if a.get("accredited") else "Not AZA-accredited"
    rows = "\n".join(f'        <div class="field"><span class="fi">{ic}</span><h4>{lab}</h4><p>{a[k]}</p></div>'
                     for (lab, ic, _), k in zip(FIELDS, ("animals", "rescue", "conservation")))
    link = ('\n      <p class="entry-link"><a href="manatees.html#rescue">How manatee rescue works</a></p>'
            if a.get("manatees") else "")
    return f"""
    <article class="entry" id="{a["id"]}">
      <div class="entry-head"><h3>{a["name"]}</h3><p>{a["city"]}, {a["state"]} &middot; {yes}</p></div>
{rows}{link}
      <p class="cite-line">Source: {a["source"]}</p>
    </article>"""


def directory():
    t = f"U.S. Aquarium Directory: Rescue and Conservation Programs | {SITE_NAME}"
    d = (f"{len(AQUARIUMS)} AZA-accredited U.S. aquariums and zoos and the animals they rescue, their rehabilitation "
         "programs and conservation work, from sea turtle hospitals to manatee and sea otter rescue.")
    items = [{"@type": "ListItem", "position": i, "name": re.sub("&amp;", "&", a["name"]), "url": SITE + "aquarium-directory.html#" + a["id"]}
             for i, a in enumerate(AQUARIUMS, 1)]
    schema = [page_schema("CollectionPage", "aquarium-directory.html", t, d,
                          {"about": "Aquarium rescue and conservation programs in the United States",
                           "mainEntity": {"@type": "ItemList", "numberOfItems": len(AQUARIUMS), "itemListElement": items}}),
              crumbs("Aquarium Directory", "aquarium-directory.html")]
    fields = "\n".join(f'      <li><span class="fi">{ic}</span><div><h3>{lab}</h3><p>{txt}</p></div></li>' for lab, ic, txt in FIELDS)
    groups = [(r, [a for a in AQUARIUMS if a["region"] == r]) for r in REGIONS]
    groups = [(r, g) for r, g in groups if g]
    down = svg('<path d="M24 10v26M14 27l10 10 10-10"/>', sw="3.4")
    jump = "\n".join(f'      <li><a href="#{region_id(r)}"><span class="down">{down}</span>{r}<em>{len(g)} entries</em></a></li>' for r, g in groups)
    body = "".join(f"""
<section id="{region_id(r)}" class="{'band ' if i % 2 else ''}region">
  <div class="wrap">
    <h2>{r}</h2>
    <div class="entries">{"".join(entry_card(a) for a in g)}
    </div>
  </div>
</section>
""" for i, (r, g) in enumerate(groups))
    return head(t, d, "aquarium-directory.html", schema, hero="hero-big-tank", sizes=PAGE_SIZES) + nav("aquarium-directory.html") + f"""
<main id="main">

<header class="page-hero">
  <div class="wrap split">
    <div>
      <h1>U.S. aquarium directory: rescue and conservation programs</h1>
      <p class="lede">Most aquarium listings stop at the address and ticket price. This directory records what {len(AQUARIUMS)} AZA-accredited aquariums and zoos do for marine animals: who they rescue, how they care for them, and the conservation work they fund.</p>
    </div>
    {hero_img("hero-big-tank", "A crowd of visitors silhouetted against a giant aquarium window full of fish and a manta ray", PAGE_SIZES)}
  </div>
</header>

<section class="band tight">
  <div class="wrap">
    <h2 class="small-h">Aquariums by region</h2>
    <ol class="jump">
{jump}
    </ol>
    <p class="note">Every aquarium here appears on the list of accredited institutions published by the {AZA} (September 2026). Each fact comes from the aquarium's own published pages, and every number carries the year it was reported.</p>
  </div>
</section>
{body}
<section class="band">
  <div class="wrap">
    <div class="section-head">
      <h2>How to read each aquarium entry</h2>
      <p>Every listing answers the same three questions, so two aquariums are easy to compare.</p>
    </div>
    <ul class="fields">
{fields}
    </ul>
  </div>
</section>
""" + cta("Check the myths before your next visit",
          f"{WORDS[len(MYTHS)].capitalize()} common aquarium myths, each checked against the research.",
          "aquarium-myths.html", "Read the aquarium myths") + sources(["find"]) + "\n</main>\n" + foot()


MANATEE_DIRECTORY = ["seaworld-orlando", "mote-marine-laboratory", "georgia-aquarium", "columbus-zoo",
                     "cincinnati-zoo", "texas-state-aquarium", "audubon-aquarium", "national-aquarium"]


def manatees():
    t = f"Florida Manatee Facts, Threats and How Rescue Works | {SITE_NAME}"
    d = ("Florida manatee facts from FWC and the U.S. Fish and Wildlife Service: size, diet, lifespan, boat strikes, "
         "cold stress, red tide and seagrass loss, how manatee rescue works, and how to help.")
    schema = [page_schema("Article", "manatees.html", t, d, {"about": "West Indian manatee"}),
              crumbs("Manatees", "manatees.html")]
    by_id = {a["id"]: a for a in AQUARIUMS}
    helpers = "\n".join(
        f'      <li><a href="aquarium-directory.html#{i}"><span class="ci">{ICON_HEART}</span><span><span class="hn">{by_id[i]["name"]}</span>'
        f'<em>{by_id[i]["city"]}, {by_id[i]["state"]}</em></span></a></li>' for i in MANATEE_DIRECTORY)
    return head(t, d, "manatees.html", schema, hero="hero-manatee-window", sizes=PAGE_SIZES) + nav("manatees.html") + f"""
<main id="main">

<header class="page-hero">
  <div class="wrap split">
    <div>
      <h1>Florida manatee facts, threats and how rescue works</h1>
      <p class="lede">Manatees are slow, plant-eating giants that share Florida's waters with boats and people. Here is what they need, what hurts them, and how rescue teams nurse injured manatees back to health.</p>
    </div>
    {hero_img("hero-manatee-window", "A young boy in a ball cap watching two manatees glide past a large aquarium window", PAGE_SIZES)}
  </div>
</header>

<section id="abby">
  <div class="wrap split">
    <div class="about-text">
      <h2>Why manatees are Abby's favorite animal</h2>
      <p class="name-line">Manatees are my favorite animal, and they are a big part of why I started {SITE_NAME}.</p>
      <p>Most people fall for their round faces and soft, wrinkly snouts first. I did too. What I love most, though, is how gentle they are. An adult can weigh about 1,000 pounds, and still nothing around a manatee has any reason to be afraid of it.</p>
      <p>Manatees only eat plants. They never hunt anything, so a normal day is slow meals of seagrass and long, quiet rests. I find that so peaceful to watch.</p>
      <p>I like to imagine people carrying themselves the way manatees do: unhurried, patient and harmless to whoever is nearby. Everyday life would be a lot softer. That thought is part of what pulled me into learning about the aquariums and zoos that rescue them.</p>
    </div>
    {photo("manatee-face", "Close view of a manatee's whiskered face and rounded snout underwater")}
  </div>
</section>

<section id="facts" class="band">
  <div class="wrap split flip">
    {photo("manatee", "A manatee mother and calf swimming together through green-blue water")}
    <div>
      <h2>Manatee facts: species, size, diet and lifespan</h2>
      <p>The West Indian manatee lives in U.S. waters as two subspecies: the Florida manatee and the Antillean manatee, whose range includes Puerto Rico. Adults are typically 9 to 10 feet long and weigh around 1,000 pounds, and some grow past 13 feet and 3,500 pounds. A newborn calf weighs about 60 to 70 pounds.</p>
      <p>Manatees are herbivores. They spend up to eight hours a day grazing on seagrass and other plants, eating up to 10% of their body weight daily. Together with their closest living relative, the dugong, they form the order Sirenia, the only marine mammals that eat plants.</p>
      <p>Of the wild manatees that reach adulthood, only about half are expected to survive into their early 20s. In human care, a manatee may live over 65 years.</p>
      <p class="cite-line">Sources: {FWC}, Aquatic Mammals: Manatee; {USFWS}, Manatee (Trichechus manatus); U.S. Geological Survey, Florida Manatees (1995).</p>
    </div>
  </div>
  <div class="wrap">
    <ul class="strip">
      <li><span class="n">8,350+</span><span class="t">manatees estimated to live in Florida</span></li>
      <li><span class="n">8 hours</span><span class="t">a day spent grazing on seagrass and other plants</span></li>
      <li><span class="n">65+ years</span><span class="t">the lifespan a manatee may reach in human care</span></li>
    </ul>
  </div>
</section>

<section id="threats">
  <div class="wrap">
    <div class="section-head">
      <h2>What threatens Florida manatees</h2>
      <p>In 2017 the {USFWS} moved the West Indian manatee from endangered to threatened under the Endangered Species Act, with its federal protections kept in place. In January 2025 the agency proposed listing the Florida manatee as threatened and the Antillean manatee as endangered. Manatees still face four big dangers.</p>
    </div>
    <div class="cards two">
      <div class="card">
        <p class="num">98</p>
        <h3>Boat strikes</h3>
        <p>Collisions with watercraft caused 25% of deaths among the manatees examined in 2025, 98 cases in all. That same year FWC and its partners rescued 33 manatees with boat injuries, the most on record.</p>
      </div>
      <div class="card">
        <p class="num">33</p>
        <h3>Cold stress</h3>
        <p>Losing warm water habitat is one of the main threats to manatees. In the colder winter of 2025, cold stress disease was diagnosed in 33 of the manatees examined.</p>
      </div>
      <div class="card">
        <p class="num">50</p>
        <h3>Red tide</h3>
        <p>Harmful algal blooms are another threat. In 2025, 50 manatee deaths were attributed to a red tide bloom in southwest Florida during the winter.</p>
      </div>
      <div class="card">
        <p class="num">1,255</p>
        <h3>Seagrass loss and starvation</h3>
        <p>When seagrass died off in the Indian River Lagoon, manatees on Florida's Atlantic coast starved. From December 2020 to April 2022, 1,255 manatee carcasses were documented during the event, and 2021 set a statewide record of 1,100 deaths. The event was officially closed on March 14, 2025.</p>
      </div>
    </div>
    <p class="cite-line">Sources: {FWC}, 2025 Manatee Mortality in Review, Manatee Mortality Table by County (2021) and Closed Manatee Mortality Event Along the East Coast; {USFWS}, 2017 reclassification and 2025 petition finding.</p>
  </div>
</section>

<section id="rescue" class="band">
  <div class="wrap split">
    <div>
      <h2>How manatee rescue and rehabilitation works</h2>
      <p>Florida manatees are rescued through the Manatee Rescue &amp; Rehabilitation Partnership, a cooperative of agencies, organizations and aquariums established in late 2001 to rescue, rehabilitate and release manatees. It now includes more than 20 organizations. FWC and its partners rescued 116 manatees in 2024 and 119 in 2025 (preliminary).</p>
      <p class="cite-line">Sources: {USFWS}, It Takes a Village to Save Manatees (2023); Manatee Rescue &amp; Rehabilitation Partnership, FAQs; {FWC}, Manatee Rescue Statistics.</p>
    </div>
    {photo("manatee-care", "A manatee eating lettuce in a green aquarium pool as small fish swim nearby")}
  </div>
  <div class="wrap">
    <ol class="steps">
      <li>
        <h3>Rescue</h3>
        <p>Someone reports an injured, orphaned, cold-stressed or tangled manatee, and FWC and partner teams bring it in from the water.</p>
      </li>
      <li>
        <h3>Critical care</h3>
        <p>The manatee goes straight to a federally authorized critical care facility. In Florida these include ZooTampa at Lowry Park, SeaWorld Orlando and Jacksonville Zoo and Gardens.</p>
      </li>
      <li>
        <h3>Second-stage care and release</h3>
        <p>Once critical care is no longer needed, a manatee may move to a second-stage facility, such as the zoos in Columbus and Cincinnati, until it is ready to return to Florida waters.</p>
      </li>
    </ol>
  </div>
</section>

<section id="directory">
  <div class="wrap">
    <div class="section-head">
      <h2>Aquariums and zoos in the directory that help manatees</h2>
      <p>Each of these institutions rescues, treats or houses recovering manatees. Open one to see its full program.</p>
    </div>
    <ul class="helpers">
{helpers}
    </ul>
  </div>
</section>

<section id="help" class="band">
  <div class="wrap split flip">
    {photo("manatee-surface", "Three manatees surfacing together in calm water near the shore")}
    <div>
      <h2>How you can help manatees in three steps</h2>
      <p>Boats and people share the water with manatees every day. A few habits on and near the water make a real difference.</p>
    </div>
  </div>
  <div class="wrap">
    <ol class="steps">
      <li>
        <h3>Slow down in manatee zones</h3>
        <p>Florida has regulatory speed zones to protect manatees. Obey every posted waterway sign, and wear polarized sunglasses, since glare on the water hides manatees.</p>
      </li>
      <li>
        <h3>Look, but never touch or feed</h3>
        <p>Do not touch manatees, feed them or give them water. Manatees that grow used to people can lose their natural fear of boats and humans, which puts them in danger.</p>
      </li>
      <li>
        <h3>Report a manatee in trouble</h3>
        <p>Call FWC's Wildlife Alert Hotline at <a href="tel:+18884043922">888-404-3922</a> (or *FWC or #FWC from a cell phone) for any injured, orphaned, tangled, distressed or dead manatee. Early calls start the rescue.</p>
      </li>
    </ol>
    <p class="cite-line">Source: {FWC}, Florida Manatee: How to Help, Viewing Guidelines and Living with Florida Manatees.</p>
  </div>
</section>
""" + cta("See every aquarium that rescues marine animals",
          f"{len(AQUARIUMS)} AZA-accredited aquariums and zoos, from sea turtle hospitals to manatee and sea otter rescue, grouped by region.",
          "aquarium-directory.html", "Open the aquarium directory") + sources(
        ["fws-manatee", "fwc-profile", "usgs-sirenia", "fws-2017", "fws-2025", "fwc-2025", "fwc-2021", "fwc-ume",
         "fws-village", "mrp", "fwc-rescue", "fwc-help"],
        note="Top photo: &ldquo;Benjamin Watches Manatees&rdquo; by Eugene Kim, CC BY 2.0, cropped and color-graded. Other photos: Unsplash.") + "\n</main>\n" + foot()


def sitemap():
    urls = "\n".join(f"  <url><loc>{SITE}{'' if h == 'index.html' else h}</loc><lastmod>{TODAY}</lastmod></url>" for h, _ in PAGES)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'


if __name__ == "__main__":
    out = {"index.html": index, "aquarium-myths.html": myths, "rescue-and-conservation.html": rescue,
           "manatees.html": manatees, "aquarium-directory.html": directory}
    for name, fn in out.items():
        with open(name, "w") as f:
            f.write(fn())
        print("wrote", name)
    with open("sitemap.xml", "w") as f:
        f.write(sitemap())
    with open("robots.txt", "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")
