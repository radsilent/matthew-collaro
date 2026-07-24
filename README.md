# matthew-collaro

Personal site for Matthew Collaro systems engineer

Static site, no dependencies. Content lives in `content/` as Markdown with
simple frontmatter; `build.py` renders it into `docs/`, which GitHub Pages
serves.

## Build

```bash
python3 build.py --base-url "https://radsilent.github.io/matthew-collaro"
```

Emits HTML, `sitemap.xml`, `robots.txt`, and `feed.xml` with schema.org
`Person` / `BlogPosting` structured data on every page.

## Adding a post

Drop a Markdown file in `content/articles/` with frontmatter:

```
---
title: Post Title — Matthew Collaro
h1: Post title
description: One-sentence summary used for meta description and listings.
type: article
date: 2026-07-24
---
```

Rebuild and commit `docs/`.
