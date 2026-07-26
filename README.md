# matthew-collaro

Personal site for Matthew Collaro, systems engineer.

## Live URLs

| Page | URL |
|---|---|
| **Home** | **https://radsilent.github.io/matthew-collaro/** |
| CV | https://radsilent.github.io/matthew-collaro/cv.html |
| Projects | https://radsilent.github.io/matthew-collaro/projects.html |
| Writing | https://radsilent.github.io/matthew-collaro/writing.html |
| Contact | https://radsilent.github.io/matthew-collaro/contact.html |
| Feed | https://radsilent.github.io/matthew-collaro/feed.xml |
| Sitemap | https://radsilent.github.io/matthew-collaro/sitemap.xml |

Companion site: https://radsilent.github.io/ (repo
[radsilent.github.io](https://github.com/radsilent/radsilent.github.io)).

Served by GitHub Pages from `main` branch, `/docs` folder. **The repo must stay
public** — Pages is disabled the moment it goes private, and the site 404s.
`guard.sh` re-asserts both conditions on a cron.

## Content rule

Two former employers are excluded from anything published here by standing
instruction and are referred to only as "a defense space systems prime" and "a
missile defense prime". Release gate, must return nothing before every push:

```bash
grep -rniE "raytheon|northrop|grumman|protonmail" . --exclude-dir=.git
```

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
