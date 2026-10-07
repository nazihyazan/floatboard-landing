# Publishing workflow

Edit `posts.json`, then run `python3 scripts/build-blog.py` from the repository root. Commit the source and generated HTML together. No runtime or JavaScript is needed to read articles.

## Audience and product fit

FloatBoard is a small desktop working board: short text and image references can stay visible above another app, and recent copied text can be reused. The primary reader is someone switching between desktop apps who needs the current note or copied item in sight. Writing, calls, UI debugging and design references are examples of that same job. FloatBoard is not an OCR tool, screenshot tool, searchable snippet library, asset catalog or full image editor.

Choose one `audience` for each post: `clipboard`, `floating-notes` or `visual-references`. The blog index groups guides by these jobs, with clipboard and floating notes first. Keep a distinct reader task per URL. For image-reference guides, name the specific decision the board supports; do not turn every step of one recording into another broad design-advice article. Retain existing published URLs when improving them so inbound links and Search Console history continue to point to the same guide.

Before claiming a plan limit, check the current packaged app and pricing page against each other. The Windows 1.0.19 package currently applies a combined daily addition limit, while the public pricing copy describes separate text and image limits. Until those agree, link to the current pricing page rather than restating a precise count in a guide.

For each new article:
- Solve one concrete reader problem. Check the existing articles and product guides to avoid duplicating intent.
- Add an original example, useful steps, limitations and only verified product claims. Do not invent experience, measurements or testimonials.
- Inspect the chosen screenshot. Use one relevant image with descriptive alt text and a caption; do not republish every screenshot in every article.
- For a recorded demo, derive a small poster and a compressed MP4 from the source GIF. Put `image`, `demo_video` and `demo_alt` in the post. The player waits for the reader to press play, so the blog index never loads all videos.
- Use a stable slug, unique title and description, and the real publication date. Set `modified` only when revising a post; the generator uses it for the visible update date, schema and sitemap.
- Give each article a distinct task and a few descriptive `tags`. Tags appear to readers and in BlogPosting data; they are not a substitute for clear titles or original guidance.
- Check current plan limits and platform support against the app. Request author review for claims not supported by documentation or screenshots.
- Link to related guides where useful. Avoid pages created solely for small keyword variations.
- Run the SEO validator and inspect desktop/mobile layout before publishing. Check sitemap inclusion, then use Search Console for new canonical article URLs.

Initial intent map:
- organize-image-references: small image reference board for a design decision.
- code-snippets-and-screenshots: investigate one UI bug with a screenshot and relevant code in view; compare the role of a visible board with searchable snippet managers.
- keep-reference-notes-visible-while-writing: keep research sources separate from the writer's own words while drafting, with a practical Windows pinning option.
- windows-clipboard-history-vs-floating-notes: reuse recent copies with Windows + V, troubleshoot missing entries, and distinguish clipboard history from a visible task note.
- take-notes-while-watching-tutorials: follow a software tutorial on one screen with timestamps, next actions and expected-versus-actual results.
- compare-photos-side-by-side-windows: compare two local or web images with Photos or Snap, then keep a four-image shortlist visible while working; use originals for precise detail.
- copy-text-from-screenshot-windows: extract screenshot text with Windows OCR tools, verify the copy against the original, and keep the source image with the corrected note. FloatBoard is not the OCR tool.
- keep-meeting-notes-visible-video-call: keep a personal agenda card in sight during a Teams call while recording agreed actions in shared meeting notes; check screen-sharing privacy.
- /floating-notes.html and /clipboard-manager.html remain product overviews.

The blog-wide `DEVTO50` ribbon uses the same discount message as the landing page. New posts can set `promo_after_section` to show one offer card within the article. Keep the offer outside editorial claims and remove or update both placements when the campaign changes.

The GIF-based demos were recorded on Linux in July 2026. Some show an older website and a board with more images than the current free plan permits per day. Captions must make this clear and articles must not present the footage as the current Windows interface or imply the full recorded board fits the free tier.

These are relevance-based topics, not claims of measured keyword search volume. Google does not prescribe a minimum word count or guarantee indexing/ranking.

## Search intent and comparison updates

The image-reference guide targets designers and illustrators organizing reference images. Its secondary questions cover reference image organizers and whether a PureRef alternative fits a mixed notes-and-images task. Keep these in this guide rather than making near-duplicate keyword pages.

For future articles, identify one audience and task, answer it early, include a concrete FloatBoard example, and link naturally to the relevant notes or clipboard guide. Compare competitors only where it helps the decision; cite official documentation, date the check, disclose that this is a product blog, and distinguish documented features from hands-on tests. Add useful FAQs without claiming unverified search volume or rich-result eligibility. Measure actual queries and clicks in Search Console before choosing follow-up topics.

The developer comparison must not claim that snippet managers cannot handle images: massCode documents visual notes, Pieces supports screenshots, and Cacher supports image attachments. FloatBoard's differentiator here is a small always-on-top working set, not exclusive image support.

Traffic goal: 500 visits/day is a measurement target, not an expected result from these two article revisions. Track actual article landing sessions, engaged sessions and downloads separately from Search Console clicks. Review search queries after indexing, then improve existing articles or choose a distinct follow-up topic based on demonstrated demand rather than guessed keyword volume.

## GIF guide intent map (5 October 2026)

These phrases describe the reader's task; they are not measured search-volume claims. Each guide uses one different segment of the July Linux recording, with a compressed video and a small poster.

- `keep-web-image-reference-visible-while-browsing`: keep one web image visible during browsing.
- `shortlist-landscape-photos-for-website-hero`: choose a website hero photo using crop and text-space checks.
- `review-image-grid-and-large-preview`: triage a small image grid, then inspect one candidate larger.
- `collect-visual-references-across-search-pages`: gather attribute-specific references from several result pages.
- `copy-web-image-and-keep-source`: copy an image while recording its source and usage context.
- `capture-webpage-detail-screenshot-reference`: capture a specific on-screen detail rather than the original image file.
- `keep-webpage-text-beside-image-references`: keep a labelled webpage excerpt next to visual references.
- `clear-copied-text-history-keep-working-set`: clean transient history after preserving useful content.
- `inspect-image-original-after-thumbnail`: verify fine detail in the original outside the board.
- `start-two-image-reference-board`: start a new design decision with two contrasting references.
