# Publishing workflow

Edit `posts.json`, then run `python3 scripts/build-blog.py` from the repository root. Commit the source and generated HTML together. No runtime or JavaScript is needed to read articles.

For each new article:
- Solve one concrete reader problem. Check the existing articles and product guides to avoid duplicating intent.
- Add an original example, useful steps, limitations and only verified product claims. Do not invent experience, measurements or testimonials.
- Inspect the chosen screenshot. Use one relevant image with descriptive alt text and a caption; do not republish every screenshot in every article.
- Use a stable slug, unique title and description, and the real publication date. The generator currently uses that date for dateModified; add a separate modification field when revising older posts.
- Check current plan limits and platform support against the app. Request author review for claims not supported by documentation or screenshots.
- Link to related guides where useful. Avoid pages created solely for small keyword variations.
- Run the SEO validator and inspect desktop/mobile layout before publishing. Check sitemap inclusion, then use Search Console for new canonical article URLs.

Initial intent map:
- organize-image-references: small image reference board for a design decision.
- code-snippets-and-screenshots: preserve context while investigating one UI issue.
- keep-reference-notes-visible-while-writing: keep sources separate from a draft.
- /floating-notes.html and /clipboard-manager.html remain product overviews.

These are relevance-based topics, not claims of measured keyword search volume. Google does not prescribe a minimum word count or guarantee indexing/ranking.

## Search intent and comparison updates

The image-reference guide targets designers and illustrators organizing reference images. Its secondary questions cover reference image organizers and whether a PureRef alternative fits a mixed notes-and-images task. Keep these in this guide rather than making near-duplicate keyword pages.

For future articles, identify one audience and task, answer it early, include a concrete FloatBoard example, and link naturally to the relevant notes or clipboard guide. Compare competitors only where it helps the decision; cite official documentation, date the check, disclose that this is a product blog, and distinguish documented features from hands-on tests. Add useful FAQs without claiming unverified search volume or rich-result eligibility. Measure actual queries and clicks in Search Console before choosing follow-up topics.
