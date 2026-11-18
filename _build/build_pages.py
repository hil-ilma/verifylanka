#!/usr/bin/env python3
"""Generate Verify Lanka service and industry pages, sitemap.xml and llms.txt.

Run from the repo root:  python3 _build/build_pages.py
Content lives in _build/content.py.
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from content import SERVICES, INDUSTRIES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://verifylanka.com"
TODAY = "2026-11-15"
FONTS = ("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600"
         "&family=Inter:wght@300;400;500;600&family=Comfortaa:wght@300;400;700&display=swap")

e = html.escape


def nav_html():
    return """  <nav>
    <a href="/" class="nav-logo">
      <img src="/logo-128.png" alt="Verify Lanka logo" class="nav-icon" />
      <span class="nav-brand"><span class="nav-verify">Verify</span><span class="nav-lanka">lanka</span></span>
    </a>
    <ul class="nav-links">
      <li><a href="/#services">What We Do</a></li>
      <li><a href="/#industries">Industries</a></li>
      <li><a href="/#how">How It Works</a></li>
      <li><a href="/#coverage">Coverage</a></li>
      <li><a href="/about/">About</a></li>
      <li><a href="/#contact" class="nav-cta">Get a Quote</a></li>
    </ul>
  </nav>"""


COMPANY = [
    ("About Verify Lanka", "/about/"),
    ("Questions and answers", "/faq/"),
    ("Become a Mystery Shopper", "/become-a-mystery-shopper-sri-lanka/"),
    ("Contact", "/#contact"),
]


def sitemap_block():
    svc = "".join(f'<li><a href="/{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES)
    ind = "".join(f'<li><a href="/{i["slug"]}/">{e(i["name"])}</a></li>' for i in INDUSTRIES)
    co = "".join(f'<li><a href="{h}">{e(n)}</a></li>' for n, h in COMPANY)
    return (
        '  <div class="pg-sitemap">\n'
        f'    <div><h4>Services</h4><ul>{svc}</ul></div>\n'
        f'    <div><h4>Industries we audit</h4><ul>{ind}</ul></div>\n'
        f'    <div><h4>Company</h4><ul>{co}</ul></div>\n'
        '  </div>\n'
    )


def footer_html():
    return f"""{sitemap_block()}  <footer>
    <div class="footer-left">
      <img src="/logo-128.png" alt="Verify Lanka logo" loading="lazy" style="height:32px; mix-blend-mode:screen; filter:brightness(1.5);" />
      <span class="footer-brand-text">
        <span style="font-family:'Comfortaa',sans-serif;font-weight:700;color:#7BA7D4;font-size:0.95rem;">Verify</span><span style="font-family:'Comfortaa',sans-serif;font-weight:700;color:var(--orange);font-size:0.95rem;">lanka</span>
      </span>
    </div>
    <p>&copy; 2026 Verify Lanka (Pvt) Ltd. Company No. PV 00377171. All rights reserved.</p>
    <ul class="footer-links">
      <li><a href="https://linkedin.com/company/verifylanka" target="_blank" rel="noopener">LinkedIn</a></li>
      <li><a href="https://wa.me/94742266513" target="_blank" rel="noopener">WhatsApp +94 74 226 6513</a></li>
      <li><a href="mailto:info@verifylanka.com">info@verifylanka.com</a></li>
    </ul>
  </footer>"""


def related_links(page, kind):
    others_s = [s for s in SERVICES if s["slug"] != page["slug"]]
    others_i = [i for i in INDUSTRIES if i["slug"] != page["slug"]]
    items = []
    if kind == "industry":
        items += [(s["name"], s["slug"]) for s in SERVICES]
        idx = INDUSTRIES.index(page)
        pick = [INDUSTRIES[(idx + k) % len(INDUSTRIES)] for k in range(1, 6)]
        items += [(i["name"] + " audits", i["slug"]) for i in pick]
    else:
        items += [(s["name"], s["slug"]) for s in others_s]
        items += [(i["name"] + " audits", i["slug"]) for i in others_i]
    return "".join(f'<a class="pg-link" href="/{slug}/">{e(name)}</a>' for name, slug in items)


def render(page, kind):
    slug = page["slug"]
    url = f"{SITE}/{slug}/"
    crumbs_mid = ("Services", "/#services") if kind == "service" else ("Industries", "/#industries")
    checks = "".join(
        f'<div class="svc reveal"><span class="svc-num">{n:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
        for n, (t, d) in enumerate(page["checks"], 1)
    )
    faqs = "".join(
        f'<details class="pg-faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in page["faqs"]
    )
    faq_ld = {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in page["faqs"]
        ],
    }
    crumb_ld = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": crumbs_mid[0], "item": SITE + "/" + crumbs_mid[1].lstrip("/")},
            {"@type": "ListItem", "position": 3, "name": page["h1"], "item": url},
        ],
    }
    service_ld = {
        "@type": "Service",
        "name": page["h1"],
        "serviceType": page["name"],
        "description": page["desc"],
        "url": url,
        "provider": {"@type": "ProfessionalService", "name": "Verify Lanka", "url": SITE + "/"},
        "areaServed": {"@type": "Country", "name": "Sri Lanka"},
    }
    ld = json.dumps({"@context": "https://schema.org", "@graph": [service_ld, crumb_ld, faq_ld]}, indent=2)
    return f"""<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(page["title"])}</title>
  <meta name="description" content="{e(page["desc"])}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="theme-color" content="#0A1929" />
  <link rel="canonical" href="{url}" />
  <link rel="icon" href="/favicon.ico?v=2" sizes="48x48" />
  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png?v=2" />
  <link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png?v=2" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png?v=2" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Verify Lanka" />
  <meta property="og:title" content="{e(page["title"])}" />
  <meta property="og:description" content="{e(page["desc"])}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{SITE}/og-image.png" />
  <meta property="og:locale" content="en_LK" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{e(page["title"])}" />
  <meta name="twitter:description" content="{e(page["desc"])}" />
  <meta name="twitter:image" content="{SITE}/og-image.png" />
  <script type="application/ld+json">
{ld}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="{FONTS}" rel="stylesheet" />
  <link rel="stylesheet" href="/style.css" />
  <link rel="stylesheet" href="/pages.css" />
</head>

<body>
{nav_html()}

  <header class="pg-hero">
    <div class="pg-wrap">
      <div class="pg-crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="{crumbs_mid[1]}">{crumbs_mid[0]}</a> / <span>{e(page["name"])}</span></div>
      <h1>{e(page["h1"])}</h1>
      <p class="pg-lead">{e(page["lead"])}</p>
      <div class="pg-actions">
        <a href="/#contact" class="btn-primary">Request an Audit</a>
        <a href="https://wa.me/94742266513" class="btn-outline" target="_blank" rel="noopener">WhatsApp +94 74 226 6513</a>
      </div>
      <ul class="pg-facts">
        <li>All island coverage</li>
        <li>Reports in 48 hours</li>
        <li>100% independent</li>
      </ul>
    </div>
  </header>

  <section class="pg-section">
    <div class="pg-wrap">
      <span class="eyebrow">What we check</span>
      <h2 class="section-title">What our auditors look at</h2>
      <div class="services-grid pg-grid">{checks}</div>
    </div>
  </section>

  <section class="pg-section pg-alt">
    <div class="pg-wrap pg-two">
      <div>
        <span class="eyebrow">Why it matters</span>
        <h2 class="section-title">What you cannot see from head office</h2>
        <p class="pg-prose">{e(page["why"])}</p>
      </div>
      <div>
        <span class="eyebrow">How it works</span>
        <h2 class="section-title">From brief to report</h2>
        <p class="pg-prose">{e(page["how"])}</p>
        <p class="pg-prose">We cover every district of Sri Lanka, including smaller towns and remote areas, and we can work in Sinhala, Tamil and English.</p>
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

  <section class="pg-section pg-alt">
    <div class="pg-wrap">
      <span class="eyebrow">Related</span>
      <h2 class="section-title">Other audits we run</h2>
      <div class="pg-links">{related_links(page, kind)}</div>
    </div>
  </section>

  <section class="pg-cta">
    <div class="pg-wrap">
      <h2>Ready to see what your customers see?</h2>
      <p>Tell us what you need. We reply within 24 hours.</p>
      <a href="/#contact" class="btn-primary">Request an Audit</a>
    </div>
  </section>

{footer_html()}

  <script>
    const revObs = new IntersectionObserver(entries => {{
      entries.forEach(en => {{ if (en.isIntersecting) {{ en.target.classList.add('on'); revObs.unobserve(en.target); }} }});
    }}, {{ threshold: 0.1 }});
    document.querySelectorAll('.reveal').forEach(el => revObs.observe(el));
  </script>
</body>

</html>
"""


def write_pages():
    for kind, items in (("service", SERVICES), ("industry", INDUSTRIES)):
        for p in items:
            d = os.path.join(ROOT, p["slug"])
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
                f.write(render(p, kind))


def write_sitemap():
    urls = [("/", "1.0")] + [(f"/{s['slug']}/", "0.9") for s in SERVICES] + [(f"/{i['slug']}/", "0.8") for i in INDUSTRIES] + [("/about/", "0.7"), ("/faq/", "0.7"), ("/become-a-mystery-shopper-sri-lanka/", "0.6")]
    body = "".join(
        f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{p}</priority>\n  </url>\n"
        for u, p in urls
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n")


def write_llms():
    lines = [
        "# Verify Lanka",
        "",
        "> Verify Lanka is a Sri Lankan mystery shopping service and customer experience audit company. "
        "Independent auditors visit businesses as real customers, in person and by phone, "
        "and deliver scored reports within 48 hours. We cover the whole island, every district, city, town and remote area.",
        "",
        "Website: " + SITE + "/",
        "Contact: info@verifylanka.com",
        "Service area: all of Sri Lanka",
        "",
        "## Services",
        "",
    ]
    lines += [f"- [{s['h1']}]({SITE}/{s['slug']}/): {s['desc']}" for s in SERVICES]
    lines += ["", "## Industries we audit", ""]
    lines += [f"- [{i['h1']}]({SITE}/{i['slug']}/): {i['desc']}" for i in INDUSTRIES]
    lines += [
        "",
        "## Company",
        "",
        f"- [About Verify Lanka]({SITE}/about/): who we are and how we work.",
        f"- [Mystery shopping in Sri Lanka: questions and answers]({SITE}/faq/): what mystery shopping is, cost, reports and coverage.",
        f"- [Become a mystery shopper in Sri Lanka]({SITE}/become-a-mystery-shopper-sri-lanka/): freelance shopper work in every district.",
    ]
    lines += [
        "",
        "## Key facts",
        "",
        "- Independent: auditors have no link to the businesses they audit.",
        "- Report turnaround: within 48 hours of the visit.",
        "- Languages checked: Sinhala, Tamil and English.",
        "- Methods: mystery shopping, mystery calls, branch audits, compliance checks, monthly tracking programmes.",
        "",
    ]
    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def update_home():
    p = os.path.join(ROOT, "index.html")
    s = open(p, encoding="utf-8").read()
    # industries block -> links
    a = s.index('<div class="industries-wrap reveal"')
    b = s.index("\n    </div>\n  </section>", a)
    links = "\n".join(f'        <a class="itag" href="/{i["slug"]}/">{e(i["name"])}</a>' for i in INDUSTRIES)
    svc_links = "\n".join(f'        <a class="itag" href="/{x["slug"]}/">{e(x["name"])}</a>' for x in SERVICES)
    block = (
        '<div class="industries-wrap reveal" id="industries">\n'
        '      <span class="eyebrow">Industries we audit</span>\n'
        '      <div class="industries-flex">\n' + links + "\n      </div>\n"
        '      <span class="eyebrow" style="margin-top:2rem;">Our audit services</span>\n'
        '      <div class="industries-flex">\n' + svc_links + "\n      </div>"
    )
    s = s[:a] + block + s[b:]
    # nav entry
    if 'href="#industries"' not in s:
        s = s.replace('<li><a href="#how">How It Works</a></li>', '<li><a href="#industries">Industries</a></li>\n      <li><a href="#how">How It Works</a></li>', 1)
    if 'href="/about/"' not in s.split("</nav>")[0]:
        s = s.replace('<li><a href="#coverage">Coverage</a></li>', '<li><a href="#coverage">Coverage</a></li>\n      <li><a href="/about/">About</a></li>', 1)
    # footer sitemap
    sm = sitemap_block()
    s = re.sub(r'  <div class="pg-sitemap">.*?</div>\n  </div>\n', "", s, flags=re.S)
    s = s.replace("  <footer>", sm + "  <footer>", 1)
    if 'href="/pages.css"' not in s:
        s = s.replace('<link rel="stylesheet" href="/style.css" />', '<link rel="stylesheet" href="/style.css" />\n  <link rel="stylesheet" href="/pages.css" />', 1)
    open(p, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    write_pages()
    write_sitemap()
    write_llms()
    update_home()
    import extra_pages
    extra_pages.write_all()
    print("built", len(SERVICES) + len(INDUSTRIES), "pages")
