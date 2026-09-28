# Distribution and measurement for the two revised guides

Goal: grow to **500 relevant visits per day** (roughly 15,000 per 30 days). This is a target to measure, not a traffic forecast. Search Console measures Google Search clicks, not all visits; use a site analytics tool or hosting logs for total sessions and count download clicks separately. Record a seven-day baseline before comparing changes.

## Publish the source pages first

1. Deploy the revised [UI debugging guide](https://floatboard.xyz/blog/code-snippets-and-screenshots/) and [writing notes guide](https://floatboard.xyz/blog/keep-reference-notes-visible-while-writing/). Keep their existing slugs and canonical URLs.
2. Confirm both pages and the new `.jpg` images return 200, the sitemap `lastmod` dates reflect 28 September 2026, and the page source contains the correct canonical and `dateModified` values.
3. In Search Console, inspect the two article URLs after deployment. Use the performance report to see **queries and clicks**, not guessed search volume. Check whether the snippets article earns impressions for UI debugging, screenshots, snippet manager with images and Windows snippet workflows; check whether the writing article earns impressions for research notes beside a draft and always-on-top notes for writers.

## Distribute to the matching audience

- **DEV Community:** Cross-post the *complete* UI debugging article, not a thin teaser. Link its original URL as `canonical_url` in the editor. DEV's [editor guide](https://dev.to/p/editor_guide) documents this field. Keep the comparison accurate and disclose that the article is from FloatBoard. Use no more than four relevant tags.
- **Hashnode:** If the publication already exists, cross-post the same developer guide with the original URL in **Are you republishing? → Add Original URL**. Hashnode [documents the setting](https://docs.hashnode.com/blogs/editor/writing-a-blog-post). Check the rendered canonical before sharing. Do not create a second near-duplicate article on floatboard.xyz.
- **Relevant discussions:** Answer an active, specific question about debugging with screenshots or keeping source notes beside a document. Lead with the useful checklist and disclose the FloatBoard connection. Add the article link only when it directly answers the person's question and the community rules allow it. Do not revive an old thread solely to drop a link.
- **Hacker News:** A Show HN submission should demonstrate the working app, not simply link to the blog. Follow the current [Show HN guidelines](https://news.ycombinator.com/showhn.html) and restriction notice before submitting. It is not an automatic traffic source.
- **Writing audience:** Share the source-card template with a writing or research audience separately from the developer article. Do not post the debugging comparison in writing communities.

## Copy-ready useful excerpts

Developer discussion answer, to adapt to the specific question:

> For UI bugs I keep a tiny evidence set: the screenshot at the failing viewport, the file/component path, the smallest relevant code fragment, and one sentence for actual versus expected behavior. I then change one suspected cause and recapture at the same viewport. I work on FloatBoard, so I keep that set in its floating text-and-image window; for long-term searchable snippets I would use a repository or a dedicated snippet manager instead.

Writing discussion answer, to adapt to the specific question:

> A source card beside the draft helps me avoid mixing a quotation with my own wording: source URL and author, date checked, exact wording, my paraphrase, and the claim I need to verify. I keep only the two or three cards needed for the current paragraph. For citations and a full research library, Zotero or another reference manager still does the long-term job.

## Weekly decision rule

Review landing sessions by article and source, engaged sessions, download clicks, Search Console queries and indexing status each week. If a query gets impressions but few clicks, improve the title and opening answer. If a social post sends visits but no engaged sessions, revise the audience or promise. If a guide attracts engaged readers, write one *distinct* follow-up question rather than another page that repeats the same keywords. Keep a log of actual numbers; do not turn the 500/day target into a claim about expected results.
