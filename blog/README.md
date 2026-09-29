# Publishing workflow

Edit `posts.json`, then run `python3 scripts/build-blog.py` from the repository root. Commit the source and generated HTML together. No runtime or JavaScript is needed to read articles.

For each new article:
- Solve one concrete reader problem. Check the existing articles and product guides to avoid duplicating intent.
- Add an original example, useful steps, limitations and only verified product claims. Do not invent experience, measurements or testimonials.
- Inspect the chosen screenshot. Use one relevant image with descriptive alt text and a caption; do not republish every screenshot in every article.
- Use a stable slug, unique title and description, and the real publication date. Set `modified` only when revising a post; the generator uses it for the visible update date, schema and sitemap.
- Check current plan limits and platform support against the app. Request author review for claims not supported by documentation or screenshots.
- Link to related guides where useful. Avoid pages created solely for small keyword variations.
- Run the SEO validator and inspect desktop/mobile layout before publishing. Check sitemap inclusion, then use Search Console for new canonical article URLs.

Initial intent map:
- organize-image-references: small image reference board for a design decision.
- code-snippets-and-screenshots: investigate one UI bug with a screenshot and relevant code in view; compare the role of a visible board with searchable snippet managers.
- keep-reference-notes-visible-while-writing: keep research sources separate from the writer's own words while drafting, with a practical Windows pinning option.
- windows-clipboard-history-vs-floating-notes: reuse recent copies with Windows + V, troubleshoot missing entries, and distinguish clipboard history from a visible task note.
- take-notes-while-watching-tutorials: follow a software tutorial on one screen with timestamps, next actions and expected-versus-actual results.
- /floating-notes.html and /clipboard-manager.html remain product overviews.

These are relevance-based topics, not claims of measured keyword search volume. Google does not prescribe a minimum word count or guarantee indexing/ranking.

## Search intent and comparison updates

The image-reference guide targets designers and illustrators organizing reference images. Its secondary questions cover reference image organizers and whether a PureRef alternative fits a mixed notes-and-images task. Keep these in this guide rather than making near-duplicate keyword pages.

For future articles, identify one audience and task, answer it early, include a concrete FloatBoard example, and link naturally to the relevant notes or clipboard guide. Compare competitors only where it helps the decision; cite official documentation, date the check, disclose that this is a product blog, and distinguish documented features from hands-on tests. Add useful FAQs without claiming unverified search volume or rich-result eligibility. Measure actual queries and clicks in Search Console before choosing follow-up topics.

The developer comparison must not claim that snippet managers cannot handle images: massCode documents visual notes, Pieces supports screenshots, and Cacher supports image attachments. FloatBoard's differentiator here is a small always-on-top working set, not exclusive image support.

Traffic goal: 500 visits/day is a measurement target, not an expected result from these two article revisions. Track actual article landing sessions, engaged sessions and downloads separately from Search Console clicks. Review search queries after indexing, then improve existing articles or choose a distinct follow-up topic based on demonstrated demand rather than guessed keyword volume.
