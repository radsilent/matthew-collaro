#!/usr/bin/env python3
"""Static site generator for the Matthew Collaro personal site.

Reads Markdown files with simple key: value frontmatter from content/,
wraps them in a shared template, and writes a deployable site to dist/.
Also emits sitemap.xml, robots.txt, and an RSS feed.

Usage:  python3 build.py [--base-url https://example.com/path]
"""

import argparse
import html
import re
import shutil
import xml.sax.saxutils as sx
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
DIST = ROOT / "docs"  # GitHub Pages serves main:/docs

PERSON = {
    "name": "Matthew Collaro",
    "alt": "Matt Collaro",
    "role": "Systems Engineer",
    "github": "https://github.com/radsilent",
    "company": "Vector Stream Systems LLC",
    "company_url": "https://vectorstreamsystems.com/",
}


# --------------------------------------------------------------------------
# Frontmatter + Markdown
# --------------------------------------------------------------------------

def parse_frontmatter(text):
    """Split `---` delimited key: value frontmatter from the body."""
    meta, body = {}, text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta, body.strip()


def md_inline(s):
    """Inline Markdown: links, bold, italics, code."""
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def md_to_html(md):
    """Minimal block-level Markdown: headings, lists, blockquotes, paragraphs."""
    out, buf, in_ul, in_ol = [], [], False, False

    def flush_p():
        if buf:
            out.append(f"<p>{md_inline(' '.join(buf))}</p>")
            buf.clear()

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush_p()
            close_lists()
            continue

        m = re.match(r"^(#{2,4})\s+(.*)$", line)
        if m:
            flush_p()
            close_lists()
            lvl = len(m.group(1))
            text = m.group(2)
            slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            out.append(f'<h{lvl} id="{slug}">{md_inline(text)}</h{lvl}>')
            continue

        if line.startswith("> "):
            flush_p()
            close_lists()
            out.append(f"<blockquote><p>{md_inline(line[2:])}</p></blockquote>")
            continue

        m = re.match(r"^[-*]\s+(.*)$", line)
        if m:
            flush_p()
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{md_inline(m.group(1))}</li>")
            continue

        m = re.match(r"^\d+\.\s+(.*)$", line)
        if m:
            flush_p()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{md_inline(m.group(1))}</li>")
            continue

        buf.append(line.strip())

    flush_p()
    close_lists()
    return "\n".join(out)


def word_count(md):
    return len(re.findall(r"\b\w+\b", md))


# --------------------------------------------------------------------------
# Structured data
# --------------------------------------------------------------------------

def person_ld(base):
    return {
        "@type": "Person",
        "@id": f"{base}/#person",
        "name": PERSON["name"],
        "givenName": "Matthew",
        "familyName": "Collaro",
        "alternateName": PERSON["alt"],
        "url": f"{base}/",
        "jobTitle": "Systems Engineer and Founder",
        "description": (
            "Systems engineer specializing in model-based systems engineering, "
            "SysML architecture modeling, and requirements traceability across "
            "aerospace, defense, and automotive programs."
        ),
        "alumniOf": [
            {"@type": "CollegeOrUniversity", "name": "University of South Florida"},
            {"@type": "CollegeOrUniversity", "name": "Georgia Institute of Technology"},
        ],
        "knowsAbout": [
            "Model-Based Systems Engineering", "SysML", "Requirements Traceability",
            "Systems Architecture", "Aerospace Systems Engineering",
            "Model Context Protocol", "Verification and Validation", "DoDAF",
        ],
        "worksFor": {
            "@type": "Organization",
            "name": PERSON["company"],
            "url": PERSON["company_url"],
        },
        "sameAs": [PERSON["github"], PERSON["company_url"]],
    }


def json_ld(page, base):
    """Build the @graph for a page."""
    import json

    url = f"{base}/{page['out']}".replace("/index.html", "/")
    graph = [person_ld(base), {
        "@type": "WebSite",
        "@id": f"{base}/#website",
        "url": f"{base}/",
        "name": f"{PERSON['name']} — {PERSON['role']}",
        "publisher": {"@id": f"{base}/#person"},
        "inLanguage": "en",
    }]

    if page["type"] == "article":
        graph.append({
            "@type": "BlogPosting",
            "@id": f"{url}#article",
            "headline": page["title"],
            "description": page["description"],
            "url": url,
            "datePublished": page["date"],
            "dateModified": page["date"],
            "wordCount": page["words"],
            "author": {"@id": f"{base}/#person"},
            "publisher": {"@id": f"{base}/#person"},
            "isPartOf": {"@id": f"{base}/#website"},
            "mainEntityOfPage": url,
            "inLanguage": "en",
        })
    else:
        graph.append({
            "@type": "ProfilePage" if page["out"] == "index.html" else "WebPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": page["title"],
            "description": page["description"],
            "isPartOf": {"@id": f"{base}/#website"},
            "about": {"@id": f"{base}/#person"},
            "mainEntity": {"@id": f"{base}/#person"},
            "inLanguage": "en",
        })

    return json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2)


# --------------------------------------------------------------------------
# Template
# --------------------------------------------------------------------------

NAV = [
    ("index.html", "Profile"),
    ("cv.html", "CV"),
    ("projects.html", "Projects"),
    ("writing.html", "Writing"),
    ("contact.html", "Contact"),
]


def render(page, base, body_html):
    url = f"{base}/{page['out']}".replace("/index.html", "/")
    depth = page["out"].count("/")
    prefix = "../" * depth

    nav = "\n".join(
        f'        <li><a href="{prefix}{href}"'
        f'{" aria-current=\"page\"" if href == page["out"] else ""}>{label}</a></li>'
        for href, label in NAV
    )

    byline = ""
    if page["type"] == "article":
        pretty = datetime.strptime(page["date"], "%Y-%m-%d").strftime("%B %-d, %Y")
        byline = (
            f'      <p class="byline">By <a href="{prefix}index.html" rel="author">'
            f'{PERSON["name"]}</a> &middot; <time datetime="{page["date"]}">{pretty}</time>'
            f' &middot; {page["words"]} words</p>\n'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(page['title'])}</title>
<meta name="description" content="{html.escape(page['description'], quote=True)}">
<meta name="author" content="{PERSON['name']}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<link rel="alternate" type="application/rss+xml" title="{PERSON['name']} — Writing" href="{base}/feed.xml">
<meta property="og:type" content="{'article' if page['type'] == 'article' else 'profile'}">
<meta property="og:site_name" content="{PERSON['name']}">
<meta property="og:title" content="{html.escape(page['title'], quote=True)}">
<meta property="og:description" content="{html.escape(page['description'], quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{html.escape(page['title'], quote=True)}">
<meta name="twitter:description" content="{html.escape(page['description'], quote=True)}">
<link rel="stylesheet" href="{prefix}style.css">
<script type="application/ld+json">
{json_ld(page, base)}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{prefix}index.html">{PERSON['name']}</a>
    <nav aria-label="Primary">
      <ul>
{nav}
      </ul>
    </nav>
  </div>
</header>

<main id="main" class="wrap">
  <article>
    <header class="page-head">
      <h1>{html.escape(page['h1'])}</h1>
{byline}    </header>
{body_html}
  </article>
</main>

<footer class="site-footer">
  <div class="wrap">
    <p><strong>{PERSON['name']}</strong> &mdash; {PERSON['role']}</p>
    <p><a href="{PERSON['github']}" rel="me noopener">GitHub</a> &middot;
       <a href="{PERSON['company_url']}" rel="noopener">{PERSON['company']}</a> &middot;
       <a href="{prefix}feed.xml">RSS</a></p>
    <p class="fine">&copy; {datetime.now(timezone.utc).year} {PERSON['name']}. All rights reserved.</p>
  </div>
</footer>
</body>
</html>
"""


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------

def collect():
    pages = []
    for path in sorted(CONTENT.rglob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        rel = path.relative_to(CONTENT)
        out = str(rel.with_suffix(".html"))
        pages.append({
            "src": path,
            "out": out,
            "title": meta.get("title", path.stem),
            "h1": meta.get("h1", meta.get("title", path.stem)),
            "description": meta.get("description", ""),
            "date": meta.get("date", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
            "type": meta.get("type", "page"),
            "body": body,
            "words": word_count(body),
        })
    return pages


def build(base):
    base = base.rstrip("/")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    pages = collect()
    articles = sorted(
        [p for p in pages if p["type"] == "article"],
        key=lambda p: p["date"], reverse=True,
    )

    # Inject the article index into writing.html and index.html.
    listing = "\n".join(
        f'- [{a["title"].split(" — ")[0]}]({a["out"]}) — {a["description"]}'
        for a in articles
    )
    recent = "\n".join(
        f'- [{a["title"].split(" — ")[0]}]({a["out"]}) — {a["description"]}'
        for a in articles[:5]
    )

    for p in pages:
        body = p["body"].replace("{{ARTICLE_LIST}}", listing).replace("{{RECENT}}", recent)
        dest = DIST / p["out"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render(p, base, md_to_html(body)), encoding="utf-8")

    for f in STATIC.iterdir():
        shutil.copy2(f, DIST / f.name)

    # sitemap.xml
    urls = []
    for p in pages:
        loc = f"{base}/{p['out']}".replace("/index.html", "/")
        pri = "1.0" if p["out"] == "index.html" else "0.8"
        urls.append(
            f"  <url><loc>{sx.escape(loc)}</loc><lastmod>{p['date']}</lastmod>"
            f"<changefreq>monthly</changefreq><priority>{pri}</priority></url>"
        )
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")

    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")

    # RSS
    items = "\n".join(
        f"    <item>\n"
        f"      <title>{sx.escape(a['title'])}</title>\n"
        f"      <link>{base}/{a['out']}</link>\n"
        f"      <guid isPermaLink=\"true\">{base}/{a['out']}</guid>\n"
        f"      <description>{sx.escape(a['description'])}</description>\n"
        f"      <dc:creator>{PERSON['name']}</dc:creator>\n"
        f"      <pubDate>{datetime.strptime(a['date'], '%Y-%m-%d').strftime('%a, %d %b %Y')} 00:00:00 GMT</pubDate>\n"
        f"    </item>" for a in articles)
    (DIST / "feed.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        f"  <channel>\n    <title>{PERSON['name']} — Writing</title>\n"
        f"    <link>{base}/</link>\n"
        f"    <description>Essays on model-based systems engineering by {PERSON['name']}.</description>\n"
        f"    <language>en-us</language>\n{items}\n  </channel>\n</rss>\n", encoding="utf-8")

    (DIST / ".nojekyll").write_text("", encoding="utf-8")

    total = sum(p["words"] for p in pages)
    print(f"Built {len(pages)} pages ({len(articles)} articles, {total:,} words) -> {DIST}")
    print(f"Base URL: {base}")
    return pages


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="https://radsilent.github.io/matthew-collaro")
    build(ap.parse_args().base_url)
