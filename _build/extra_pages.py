#!/usr/bin/env python3
"""About, FAQ, shopper recruitment and 404 pages. Called by build_pages.py."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_pages as bp  # noqa: E402
from content import SERVICES, INDUSTRIES  # noqa: E402

e = bp.e
SITE = bp.SITE
ROOT = bp.ROOT


def shell(slug, title, desc, crumb, h1, lead, body, graph, index=True):
    url = f"{SITE}/{slug}/"
    robots = "index, follow, max-image-preview:large" if index else "noindex"
    canonical = f'\n  <link rel="canonical" href="{url}" />' if index else ""
    ld = ""
    if graph:
        ld = '\n  <script type="application/ld+json">\n' + json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2) + "\n  </script>"
    return f"""<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}" />
  <meta name="robots" content="{robots}" />
  <meta name="theme-color" content="#0A1929" />{canonical}
  <link rel="icon" href="/favicon.ico?v=2" sizes="48x48" />
  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png?v=2" />
  <link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png?v=2" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png?v=2" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Verify Lanka" />
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(desc)}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{SITE}/og-image.png" />
  <meta name="twitter:card" content="summary_large_image" />{ld}
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="{bp.FONTS}" rel="stylesheet" />
  <link rel="stylesheet" href="/style.css" />
  <link rel="stylesheet" href="/pages.css" />
  <script src="/nav.js" defer></script>
</head>

<body>
{bp.nav_html()}

  <header class="pg-hero">
    <div class="pg-wrap">
      <div class="pg-crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <span>{e(crumb)}</span></div>
      <h1>{e(h1)}</h1>
      <p class="pg-lead">{e(lead)}</p>
    </div>
  </header>
{body}
{bp.footer_html()}
</body>

</html>
"""


def crumbs(name, slug):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": f"{SITE}/{slug}/"},
        ],
    }


def cards(items):
    return "".join(
        f'<div class="svc"><span class="svc-num">{n:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
        for n, (t, d) in enumerate(items, 1)
    )


def links(items):
    return "".join(f'<a class="pg-link" href="{href}">{e(name)}</a>' for name, href in items)


CTA = """
  <section class="pg-cta">
    <div class="pg-wrap">
      <h2>Ready to see what your customers see?</h2>
      <p>Tell us what you need. We reply within 24 hours.</p>
      <a href="/#contact" class="btn-primary">Request an Audit</a>
    </div>
  </section>
"""

# ── ABOUT ─────────────────────────────────────────────────────────────
PRINCIPLES = [
    ("Independent", "We work for the owner or head office, never for the branch being checked. Our auditors have no link to the outlets they visit."),
    ("Unannounced", "Staff are not told when a visit will happen. What we see is an ordinary day."),
    ("Evidence, not opinion", "Every score comes from a fixed checklist and written notes of what was seen and heard."),
    ("Confidential", "Findings go only to the people you name. We do not share client results with anyone else."),
    ("The same standard everywhere", "One score sheet for every outlet, so a branch in Jaffna is measured the same way as a branch in Colombo."),
    ("Fast", "Reports reach you within 48 hours of the visit, while there is still time to act."),
]


def about():
    svc = links([(s["name"], f"/{s['slug']}/") for s in SERVICES])
    ind = links([(i["name"], f"/{i['slug']}/") for i in INDUSTRIES])
    body = f"""
  <section class="pg-section">
    <div class="pg-wrap pg-two">
      <div>
        <span class="eyebrow">Who we are</span>
        <h2 class="section-title">A Sri Lankan mystery shopping company</h2>
        <p class="pg-prose">Verify Lanka is a Sri Lankan mystery shopping service and customer experience audit company. We send independent auditors into businesses as ordinary customers, in person, by phone and online, and report exactly what happened.</p>
        <p class="pg-prose">Verify Lanka (Pvt) Ltd is a private limited company registered in Sri Lanka, company number PV 00377171. We are based in Kandy and serve businesses across the whole island.</p>
        <p class="pg-prose">Our only job is to show you what your customers really experience, so you can fix what is broken and keep what works.</p>
      </div>
      <div>
        <span class="eyebrow">What we do</span>
        <h2 class="section-title">Audits from the customer side</h2>
        <p class="pg-prose">Mystery shopping, customer service audits, branch audits, compliance checks, competitor benchmarking and monthly tracking programmes. One outlet or a full network, anywhere on the island.</p>
        <p class="pg-prose">We work in Sinhala, Tamil and English, and we cover every district of Sri Lanka.</p>
      </div>
    </div>
  </section>

  <section class="pg-section pg-alt">
    <div class="pg-wrap">
      <span class="eyebrow">How we work</span>
      <h2 class="section-title">Six rules we do not bend</h2>
      <div class="services-grid pg-grid">{cards(PRINCIPLES)}</div>
    </div>
  </section>

  <section class="pg-section">
    <div class="pg-wrap">
      <span class="eyebrow">Services</span>
      <h2 class="section-title">What we offer</h2>
      <div class="pg-links">{svc}</div>
      <span class="eyebrow" style="margin-top:3rem;">Industries</span>
      <h2 class="section-title">Who we work with</h2>
      <div class="pg-links">{ind}</div>
    </div>
  </section>
{CTA}"""
    graph = [
        {"@type": "AboutPage", "url": f"{SITE}/about/", "name": "About Verify Lanka", "about": {"@id": SITE + "/#org"}},
        crumbs("About", "about"),
    ]
    return shell(
        "about",
        "About Verify Lanka | Mystery Shopping Company in Sri Lanka",
        "Verify Lanka is an independent mystery shopping service in Sri Lanka, covering every district of the island with customer experience audits.",
        "About",
        "About Verify Lanka",
        "An independent mystery shopping and customer experience audit company, working across all of Sri Lanka.",
        body,
        graph,
    )


# ── FAQ ───────────────────────────────────────────────────────────────
FAQS = [
    ("What is mystery shopping?", "Mystery shopping is a way to measure customer service. A trained person visits a business as an ordinary customer, follows a planned scenario, and reports what happened against a checklist. Staff do not know the visit is a check."),
    ("What is a mystery shopping service?", "A mystery shopping service is a company that sends trained people to visit your business as ordinary customers, then reports on the service they received. Verify Lanka is a mystery shopping service that does this for businesses across Sri Lanka, in person, by phone and online."),
    ("What is a mystery shopper?", "A mystery shopper is the person who makes the visit. They are also called secret shoppers, mystery guests when they visit hotels and restaurants, and mystery callers when they test phone lines."),
    ("What is a customer service audit?", "A customer service audit, also called a customer experience or CX audit, compares the service your customers really get with the service your company promises. Mystery shopping is the main method, often with phone, email and chat checks added."),
    ("Which businesses use mystery shopping in Sri Lanka?", "Banks, finance and leasing companies, insurers, telecom providers, supermarkets and retail chains, hotels, restaurants, fuel stations, hospitals, pharmacies, vehicle showrooms, schools, public offices, online stores and call centres."),
    ("Which parts of Sri Lanka do you cover?", "The whole island. We cover every district, including smaller towns and remote areas."),
    ("How much does mystery shopping cost in Sri Lanka?", "The price depends on the number of outlets, where they are and how detailed the scenario is. Send us your outlet list and we will reply with a quote within 24 hours."),
    ("How fast will we get the report?", "Within 48 hours of the visit."),
    ("What is in the report?", "A score for each area checked, such as staff conduct, service speed, compliance and environment, an overall score, and written notes on what the auditor saw and heard. For several outlets you also get a ranking."),
    ("Will our staff know they are being checked?", "No. Auditors behave as normal customers and do not reveal themselves. Results go only to the people you name."),
    ("Is mystery shopping fair to staff?", "Yes, when it is done properly. Auditors act as ordinary customers, never try to trick staff into breaking rules, and score against standards the company has already set. Most clients use the results for training and recognition."),
    ("Can you run a one time audit, or only ongoing programmes?", "Both. You can start with a single audit and move to monthly or quarterly visits later."),
    ("Can you compare us with our competitors?", "Yes. We can run the same scenario at competitor outlets and report the difference."),
    ("Which languages do you work in?", "Sinhala, Tamil and English."),
    ("How do I become a mystery shopper in Sri Lanka?", "We take on freelance mystery shoppers in every district. See our Become a Mystery Shopper page for how to apply."),
]


def faq():
    qa = "".join(f'<div class="pg-qa"><h3>{e(q)}</h3><p>{e(a)}</p></div>' for q, a in FAQS)
    more = links(
        [(s["name"], f"/{s['slug']}/") for s in SERVICES]
        + [("Become a Mystery Shopper", "/become-a-mystery-shopper-sri-lanka/"), ("About Verify Lanka", "/about/")]
    )
    body = f"""
  <section class="pg-section">
    <div class="pg-wrap pg-narrow">
      {qa}
    </div>
  </section>

  <section class="pg-section pg-alt">
    <div class="pg-wrap">
      <span class="eyebrow">Read more</span>
      <h2 class="section-title">Our services</h2>
      <div class="pg-links">{more}</div>
    </div>
  </section>
{CTA}"""
    graph = [
        {
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS],
        },
        crumbs("FAQ", "faq"),
    ]
    return shell(
        "faq",
        "Mystery Shopping in Sri Lanka: Questions and Answers | Verify Lanka",
        "What mystery shopping is, how it works in Sri Lanka, what it costs, what a report contains and how to become a mystery shopper.",
        "FAQ",
        "Mystery Shopping in Sri Lanka: Questions and Answers",
        "Plain answers about mystery shoppers, customer service audits and how Verify Lanka works.",
        body,
        graph,
    )


# ── BECOME A MYSTERY SHOPPER ──────────────────────────────────────────
JOIN_STEPS = [
    ("Apply by email", "Send us your name, district, phone number and the languages you speak."),
    ("Get a brief", "When a job comes up near you, we send the place, the scenario and the checklist."),
    ("Make the visit", "Go as a normal customer. Watch, listen and remember. Do not tell staff who you are."),
    ("Send your report", "Fill in the checklist honestly on the same day, while it is fresh."),
    ("Get paid", "You are paid a fixed fee for each completed assignment."),
    ("Stay in the pool", "Good, reliable shoppers are offered more assignments as new jobs come in."),
]
JOIN_FAQS = [
    ("Do I have to pay to join?", "No. Verify Lanka never asks shoppers for a joining fee or a deposit. If someone asks you for money in our name, it is not us."),
    ("Is this a full time job?", "No. It is freelance work. Assignments are offered when a job comes up in your area, and you choose which ones to take."),
    ("Which districts are you looking for shoppers in?", "Every district of Sri Lanka, including smaller towns and rural areas."),
    ("Which languages do I need?", "Sinhala, Tamil or English. One language is enough."),
    ("What do I need?", "You must be 18 or older, have a smartphone, and be honest, observant and on time."),
]


def join():
    faqs = "".join(f'<details class="pg-faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in JOIN_FAQS)
    body = f"""
  <section class="pg-section">
    <div class="pg-wrap">
      <span class="eyebrow">How it works</span>
      <h2 class="section-title">From application to payment</h2>
      <div class="services-grid pg-grid">{cards(JOIN_STEPS)}</div>
    </div>
  </section>

  <section class="pg-section pg-alt">
    <div class="pg-wrap pg-two">
      <div>
        <span class="eyebrow">The work</span>
        <h2 class="section-title">What a mystery shopper does</h2>
        <p class="pg-prose">You visit a bank, shop, hotel, restaurant or other business as an ordinary customer. You follow a simple scenario, such as asking about a product, and note how you were treated. Afterwards you fill in a checklist.</p>
        <p class="pg-prose">We are building a pool of freelance mystery shoppers in every district of Sri Lanka, so there is work in cities and in small towns.</p>
      </div>
      <div>
        <span class="eyebrow">Apply</span>
        <h2 class="section-title">How to apply</h2>
        <p class="pg-prose">Email <a href="mailto:info@verifylanka.com?subject=Mystery%20shopper%20application">info@verifylanka.com</a> with the subject "Mystery shopper application" and tell us:</p>
        <ul class="pg-list">
          <li>Your full name</li>
          <li>Your district and nearest town</li>
          <li>Your phone or WhatsApp number</li>
          <li>The languages you speak</li>
        </ul>
        <div class="pg-actions"><a href="mailto:info@verifylanka.com?subject=Mystery%20shopper%20application" class="btn-primary">Apply by Email</a></div>
      </div>
    </div>
  </section>

  <section class="pg-section">
    <div class="pg-wrap pg-narrow">
      <span class="eyebrow">Questions</span>
      <h2 class="section-title">Common questions</h2>
      {faqs}
    </div>
  </section>
"""
    slug = "become-a-mystery-shopper-sri-lanka"
    graph = [
        {
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in JOIN_FAQS],
        },
        crumbs("Become a Mystery Shopper", slug),
    ]
    return shell(
        slug,
        "Become a Mystery Shopper in Sri Lanka | Verify Lanka",
        "Freelance mystery shopper work in every district of Sri Lanka. Visit businesses as a customer, send a report, and get paid per completed assignment.",
        "Become a Mystery Shopper",
        "Become a Mystery Shopper in Sri Lanka",
        "Freelance work in your own area. Visit businesses as a customer, tell us what happened, and get paid for each completed assignment.",
        body,
        graph,
    )


def not_found():
    body = f"""
  <section class="pg-section">
    <div class="pg-wrap">
      <div class="pg-links">{links([("Home", "/"), ("Mystery Shopping", "/mystery-shopping-sri-lanka/"), ("About", "/about/"), ("FAQ", "/faq/"), ("Contact", "/#contact")])}</div>
    </div>
  </section>
"""
    return shell("404", "Page not found | Verify Lanka", "This page does not exist.", "Not found", "Page not found", "The page you were looking for is not here. Try one of these.", body, None, index=False)


def write_all():
    for slug, fn in (("about", about), ("faq", faq), ("become-a-mystery-shopper-sri-lanka", join)):
        d = os.path.join(ROOT, slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(fn())
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(not_found())


if __name__ == "__main__":
    write_all()
