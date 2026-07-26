# Search result displacement plan — Matthew Collaro

Status as of 2026-07-24. Live properties are marked ✅.

## The mechanic that matters

Google shows roughly **1–2 results per domain** for a person-name query (site
diversity). Page 1 is ~10 organic slots. So:

- 100 pages on one domain → still ~1–2 slots.
- 10 pages across 10 domains → up to 10 slots.

**Displacement is a function of distinct properties, not page count.** This is
why the "spin up 100 sites" advice fails twice over: the sites are one footprint
to Google's spam classifiers, and they cannot occupy more slots than a single
well-built domain would.

The plan below targets ~10 distinct high-authority domains.

---

## Live now (built from the terminal, no action needed from you)

| # | Property | URL | Status |
|---|----------|-----|--------|
| 1 | Personal site (15 pages, 11.4k words) | https://radsilent.github.io/matthew-collaro/ | ✅ live, indexed via IndexNow |
| 2 | GitHub profile | https://github.com/radsilent | ✅ live |

Submitted to Bing, Yandex, and Seznam via IndexNow (all accepted). Google has no
equivalent free API — it will find the site by crawl, typically 1–3 weeks. You
can accelerate this in ~2 minutes; see "Google Search Console" below.

---

## Requires you — signup needs SMS/email verification and ToS acceptance as you

Ordered by ranking impact for a name query. The first three are worth more than
everything else combined.

### 1. LinkedIn — highest impact by a wide margin

LinkedIn is nearly always the #1 or #2 result for a professional's name. If you
do only one thing on this list, do this one, and make sure the profile is set to
**public** (Settings → Visibility → Public profile → On, and set a custom URL).

**Custom URL to claim:** `linkedin.com/in/matthew-collaro`

**Headline:**
> Systems Engineer | MBSE & SysML | Founder at Vector Stream Systems

**About section:**
> Systems engineer with seven years across aerospace, defense, and automotive — Boeing Commercial Airplanes, a defense space
> systems prime, a missile defense prime, Deloitte Government & Public Services,
> and Parker Hannifin Aerospace.
>
> I work as a Senior Systems Engineer at Lucid Motors on cross-domain
> integration of infotainment and driver feedback systems for autonomy-enabled
> vehicle builds, and I am the founder of Vector Stream Systems LLC, where I
> build VectorMBE — a governed engineering platform that keeps requirements,
> architecture models, and verification evidence linked instead of drifting
> apart.
>
> Most of my career has been in environments where unverified artifacts do not
> ship. I apply the same posture to AI-generated engineering content: generate,
> then check against constraints the generator cannot route around.
>
> Writing and CV: https://radsilent.github.io/matthew-collaro/

**Featured links:** add the personal site and 2–3 essays.

### 2. Google Search Console — 2 minutes, big indexing speedup

1. Go to https://search.google.com/search-console
2. Add property → URL prefix → `https://radsilent.github.io/matthew-collaro/`
3. Verify via the HTML file method — **send me the filename Google gives you and
   I will deploy it from the terminal**, then click Verify.
4. Sitemaps → submit `sitemap.xml`

This is the single fastest way to get all 15 pages into Google.

### 3. X / Twitter

**Handle:** `@matthewcollaro` (or nearest available)
**Name:** Matthew Collaro
**Bio:**
> Systems engineer. MBSE, SysML, requirements traceability. Founder @VectorStreamS.
> Aerospace → defense → automotive.
**Website:** https://radsilent.github.io/matthew-collaro/

### 4. Medium or Substack — republish, do not rewrite

Both rank strongly. Republish 3–4 of the ten essays already written, and set the
canonical URL to the original on your site so they do not compete as duplicates
(Medium: "Import a story" does this automatically; Substack: canonical field in
post settings).

Start with these three — they are the most search-relevant:
- Why requirements traceability breaks, and what actually fixes it
- Guardrails for AI-generated engineering artifacts
- Model governance for SysML programs that have to certify

Byline must read **Matthew Collaro**.

### 5. about.me — email signup only, no phone

Fastest legitimate profile on the list. One page, links to everything else,
ranks well for names because the domain is tuned for exactly this query type.

### 6. ORCID — free, email only, permanent identifier

https://orcid.org — legitimate for anyone with technical/patent output. Ranks
well and is a durable identifier tied to your name. Add the provisional patent
application and employment history.

### 7. Crunchbase — person profile as founder

Create the Vector Stream Systems LLC company page if it does not exist, then add
yourself as founder. Crunchbase person pages rank consistently.

### 8. Instagram / Facebook / Threads

Lower content value but they reliably occupy name-query slots, and they are
cheap to set up. Same bio, same profile photo, link to the site. Set them public.

**Use the same photo everywhere.** Consistent imagery across profiles helps
Google associate them as one entity, and it changes which image appears in
results.

---

## Also worth doing — direct removal

This is the highest-ROI action available and it is not SEO.

Many mugshot aggregators remove records on request, free, and several states
have statutes restricting fee-charging for removal of
booking photos. Some sites remove automatically on proof that charges were
dismissed, dropped, or expunged.

If the underlying record was dismissed, dropped, sealed, or expunged, pursue
removal directly and in parallel with this — suppression takes months, removal
can take days, and a removed source cannot resurface. An attorney letter is
often not required; a written request citing the disposition frequently is.

---

## Maintenance

The site is a git repo. To add an essay:

```bash
cd ~/matthew-collaro-site
# create content/articles/your-slug.md with frontmatter
python3 build.py --base-url "https://radsilent.github.io/matthew-collaro"
git add -A && git commit -m "New essay" && git push
```

Pages redeploys automatically. Re-run the IndexNow submission afterward to push
the new URLs to Bing and Yandex.

Publishing cadence matters more than volume: one genuine essay a month sustains
the site's authority better than ten published at once and then nothing.

---

## Keep the site from going dark (do this first thing)

Both repos reverted from public to private on their own once during setup, which
disabled Pages and 404'd the site. `guard.sh` in this repo re-asserts public
visibility, re-enables Pages, and logs a health check. Install it:

```bash
chmod +x ~/matthew-collaro-site/guard.sh
( crontab -l 2>/dev/null; echo "*/15 * * * * /home/vectorstream/matthew-collaro-site/guard.sh" ) | crontab -
```

Check `~/matthew-collaro-site/guard.log` for history. If it reports repeated
reversions, the cause is an account-level setting rather than a fluke — check
GitHub → Settings → Repository defaults, and whether the account is subject to
an enterprise/org policy restricting public repositories.

## Live property inventory

| Property | URL |
|---|---|
| Personal site, 15 pages | https://radsilent.github.io/matthew-collaro/ |
| GitHub profile | https://github.com/radsilent |
| Gist — MBSE validation rules | https://gist.github.com/radsilent/bf70a7861ab656cf6261b4d85bd9d897 |
| Gist — interface checklist | https://gist.github.com/radsilent/d11b5263edd63ab56c92668cabd75011 |
| Gist — requirements writing | https://gist.github.com/radsilent/8198b549e551f73a1e8678f8dd036a51 |
| Gist — MBSE adoption 90 days | https://gist.github.com/radsilent/76648b62dab46a23c96ebb624181b2f2 |
