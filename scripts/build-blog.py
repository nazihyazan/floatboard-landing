"""Generate static blog pages from reviewed posts.json. Run from repository root."""
import json
import html
from pathlib import Path
import struct
from datetime import date
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://floatboard.xyz'
posts = json.loads((ROOT / 'blog/posts.json').read_text())
posts_by_slug = {post['slug']: post for post in posts}
assert len(posts_by_slug) == len(posts), 'Duplicate blog slug'
esc = html.escape
nav = '<nav class="guide-nav" aria-label="Main navigation"><a class="guide-brand" href="/">FloatBoard</a><div class="guide-nav-links"><a href="/blog/">Blog</a><a href="/floating-notes.html">Floating notes</a><a href="/clipboard-manager.html">Clipboard manager</a><a href="/download/" class="guide-nav-btn">Download Free ↓</a></div></nav>'
promo_bar = '''<aside class="blog-promo-bar" aria-label="FloatBoard Premium offer">
<div class="blog-promo-ticker" aria-hidden="true"><div class="blog-promo-track"><span>Special offer · 50% off FloatBoard Pro · Use code DEVTO50 · </span><span>Special offer · 50% off FloatBoard Pro · Use code DEVTO50 · </span></div></div>
<div class="blog-promo-details"><strong class="blog-promo-discount">50% OFF</strong><span>FloatBoard Pro Special Deal</span><span>Use code <code>DEVTO50</code></span><a href="/pricing.html">Claim offer →</a></div>
</aside>'''
ad_leaderboard_top = '''<aside class="ad-card-iab ad-leaderboard-top" aria-label="Sponsored leaderboard">
<div class="ad-leaderboard-inner">
<div class="ad-leaderboard-left">
<div class="ad-iab-badge-group"><span class="ad-iab-badge">Ad</span><span class="ad-iab-brand">FloatBoard Pro</span><span class="ad-iab-info" title="Advertisement">ⓘ ✕</span></div>
<h3 class="ad-leaderboard-title">Stop Losing Copied Screenshots &amp; API Keys! Pin Anything Always-on-Top</h3>
<p class="ad-leaderboard-desc">FloatBoard for Windows 11, macOS &amp; Linux — 100% Offline &amp; Instant Shortcut (728x90 Leaderboard)</p>
</div>
<div class="ad-leaderboard-right">
<a href="/pricing.html" class="ad-leaderboard-offer">Use code <code>DEVTO50</code> (50% Off)</a>
<a href="/download/" class="ad-iab-btn-google">Download Free App →</a>
</div>
</div>
</aside>'''

ad_left_skyscraper = '''<aside class="ad-card-iab ad-card-left-skyscraper" aria-label="Sponsored product showcase">
<div class="ad-iab-header">
<div class="ad-iab-badge-group"><span class="ad-iab-badge">Ad</span><span class="ad-iab-brand">FloatBoard</span></div>
<span class="ad-iab-info" title="Advertisement">ⓘ ✕</span>
</div>
<div class="ad-left-title-box">
<h3 class="ad-left-title">FLOATBOARD<br>CLIPBOARD<br>MANAGER</h3>
</div>
<div class="ad-left-checklist">
<div><span>✔</span> Save Image + Source URL</div>
<div><span>✔</span> Pin Sticky Notes on Top</div>
<div><span>✔</span> OCR Screenshot Text</div>
<div><span>✔</span> Compare Photos Side-by-Side</div>
<div><span>✔</span> 100% Local &amp; Private</div>
</div>
<div class="ad-left-media">
<img src="/blog/assets/developer-floating-notes-workspace.jpg" width="268" height="178" alt="FloatBoard floating notes screenshot preview" loading="lazy">
</div>
<div class="ad-left-footer">
<a href="/download/" class="ad-left-btn">TRY FREE ON PC →</a>
<span class="ad-left-label">160x600 Tall Skyscraper Ad</span>
</div>
</aside>'''

ad_sidebar_300x600 = '''<aside class="ad-card-iab ad-card-300x600" aria-label="Sponsored product showcase">
<div class="ad-iab-header">
<div class="ad-iab-badge-group"><span class="ad-iab-badge">Ad</span><span class="ad-iab-brand">AdChoices</span></div>
<span class="ad-iab-info" title="Advertisement">ⓘ ✕</span>
</div>
<div class="ad-iab-body">
<p class="ad-iab-category">⚡ ALWAYS-ON-TOP WORKSPACE</p>
<h3 class="ad-iab-title">Pin Dev Notes, API Keys &amp; Screenshots Above Your IDE or Browser</h3>
<div class="ad-iab-media">
<img src="/blog/assets/developer-floating-notes-workspace.jpg" width="268" height="178" alt="FloatBoard always-on-top developer workspace with notes and screenshots" loading="lazy">
</div>
<p class="ad-iab-desc">Stop paying the Alt-Tab tax. 100% offline local memory for Windows, Mac &amp; Linux.</p>
</div>
<div class="ad-iab-footer">
<a href="/download/" class="ad-iab-btn-google">Download Free on Desktop →</a>
<div class="ad-iab-offer-row"><a href="/pricing.html" class="ad-iab-offer-link">50% off lifetime with <code>DEVTO50</code> ($2.99)</a></div>
<span class="ad-iab-attribution">300x600 Half-Page Vertical Ad (Tall, Not Wide!)</span>
</div>
</aside>'''

ad_sidebar_300x250_emerald = '''<aside class="ad-card-iab ad-card-300x250 ad-card-emerald" aria-label="Sponsored visual tools">
<div class="ad-iab-header">
<div class="ad-iab-badge-group"><span class="ad-iab-badge">Ad</span><span class="ad-iab-brand">FloatBoard</span></div>
<span class="ad-iab-info" title="Advertisement">ⓘ ✕</span>
</div>
<div class="ad-iab-body">
<p class="ad-iab-category">📸 ORGANIZE IMAGE REFERENCES</p>
<h3 class="ad-iab-title">Compare Photos Side-by-Side</h3>
<p class="ad-iab-desc">Compare photos side-by-side &amp; inspect 100% original resolution without opening 20 browser tabs.</p>
</div>
<div class="ad-iab-footer">
<a href="/floating-notes.html" class="ad-iab-btn-emerald">Launch Free Image Board →</a>
<span class="ad-iab-attribution">300x250 Medium Rectangle Ad</span>
</div>
</aside>'''

ad_sidebar_sticky_offer = '''<aside class="ad-card-iab ad-card-300x250 ad-sticky-offer" aria-label="Special offer">
<div class="ad-iab-header">
<div class="ad-iab-badge-group"><span class="ad-iab-badge">Ad</span><span class="ad-iab-brand">Special Deal</span></div>
<span class="ad-iab-info" title="Advertisement">ⓘ</span>
</div>
<div class="ad-iab-body">
<p class="ad-iab-category">Limited Lifetime Access</p>
<h3 class="ad-iab-title">Get Unlimited Floating Windows for $2.99</h3>
<p class="ad-iab-desc">Upgrade to FloatBoard Pro once, keep it forever. No monthly cloud fees, offline privacy guaranteed.</p>
</div>
<div class="ad-iab-footer">
<a href="/pricing.html" class="ad-iab-btn-google">Claim 50% Off Lifetime →</a>
<span class="ad-iab-attribution">Coupon DEVTO50 Applied at Checkout</span>
</div>
</aside>'''

ad_sidebar_sponsored_links = '''<aside class="ad-card-iab ad-sponsored-links" aria-label="Sponsored recommendations">
<div class="ad-iab-header">
<div class="ad-iab-badge-group"><span class="ad-iab-badge">Ad</span><span class="ad-iab-brand">Recommended by FloatBoard</span></div>
<span class="ad-iab-info" title="Advertisement">ⓘ</span>
</div>
<div class="ad-sponsored-links-list">
<a href="/download/" class="ad-sponsored-link-item">
<span class="ad-link-bullet">▶</span>
<div><strong>FloatBoard for Windows 11</strong><span>Pin scratchpad notes above any app. Free download.</span></div>
</a>
<a href="/pricing.html" class="ad-sponsored-link-item">
<span class="ad-link-bullet">▶</span>
<div><strong>Lifetime License · $2.99</strong><span>Unlock unlimited floating windows with code DEVTO50.</span></div>
</a>
<a href="/web-pad/" class="ad-sponsored-link-item">
<span class="ad-link-bullet">▶</span>
<div><strong>Free Online WebPad</strong><span>No-install floating notes in Chrome &amp; Edge.</span></div>
</a>
<a href="/clipboard-manager.html" class="ad-sponsored-link-item">
<span class="ad-link-bullet">▶</span>
<div><strong>Floating Clipboard Manager</strong><span>Auto-pin copied text &amp; images in real time.</span></div>
</a>
</div>
</aside>'''

ad_incontent_1 = '''<aside class="ad-card-iab ad-card-in-content ad-incontent-orange" aria-label="Sponsored in-content ad">
<div class="ad-iab-header">
<div class="ad-iab-badge-group"><span class="ad-iab-badge">Ad</span><span class="ad-iab-brand">FloatBoard Pro · 50% Off</span></div>
<span class="ad-iab-info" title="Advertisement">ⓘ ✕</span>
</div>
<div class="ad-iab-body">
<p class="ad-iab-category">Productivity Tool</p>
<h3 class="ad-iab-title">Stop Losing API Keys Behind Windows</h3>
<p class="ad-iab-desc">FloatBoard keeps temporary notes and reference screenshots floating on top of your screen. 100% offline local memory.</p>
</div>
<div class="ad-iab-footer">
<a href="/pricing.html" class="ad-iab-btn-orange">Get 50% Off Lifetime ($2.99) →</a>
<span class="ad-iab-attribution">Limited-time developer deal · Code <code>DEVTO50</code></span>
</div>
</aside>'''

ad_incontent_2 = '''<aside class="ad-card-iab ad-card-in-content ad-incontent-yellow" aria-label="Sponsored in-content ad">
<div class="ad-iab-header">
<div class="ad-iab-badge-group"><span class="ad-iab-badge-sponsored">SPONSORED</span><span class="ad-iab-brand">FloatBoard Desktop</span></div>
<span class="ad-iab-info" title="Advertisement">ⓘ ✕</span>
</div>
<div class="ad-iab-body">
<h3 class="ad-iab-title">Tired of Windows Clipboard Losing Your Image Source Links?</h3>
<p class="ad-iab-desc">FloatBoard automatically saves the webpage URL every time you copy a picture or screenshot. Pin notes and commands directly above your IDE.</p>
</div>
<div class="ad-iab-footer">
<a href="/download/" class="ad-iab-btn-blue">Download Free App →</a>
<span class="ad-iab-attribution">Offline &amp; Lightweight · Windows 11, Mac &amp; Linux</span>
</div>
</aside>'''

ad_incontent_3 = '''<aside class="ad-card-iab ad-card-in-content ad-incontent-emerald" aria-label="Sponsored in-content ad">
<div class="ad-iab-header">
<div class="ad-iab-badge-group"><span class="ad-iab-badge">Ad</span><span class="ad-iab-brand">Screen Pinning &amp; Scratchpad</span></div>
<span class="ad-iab-info" title="Advertisement">ⓘ ✕</span>
</div>
<div class="ad-iab-body">
<p class="ad-iab-category">Visual Reference Board</p>
<h3 class="ad-iab-title">Stop Saving 80 Throwaway Desktop Screenshots</h3>
<p class="ad-iab-desc">Pin UI mockups, hex codes, and error traces into an always-on-top board instantly without saving temporary files to disk.</p>
</div>
<div class="ad-iab-footer">
<a href="/pricing.html" class="ad-iab-btn-emerald">Upgrade to Pro ($2.99) →</a>
<span class="ad-iab-attribution">Use Code <code>DEVTO50</code> at checkout</span>
</div>
</aside>'''

ad_sponsored_grid = '''<section class="ad-sponsored-grid-section" aria-label="Sponsored content recommendations">
<div class="ad-sponsored-grid-header">
<h3>Promoted Stories</h3>
<span class="ad-iab-badge">Sponsored by FloatBoard</span>
</div>
<div class="ad-sponsored-grid">
<a href="/download/" class="ad-sponsored-tile">
<img src="/blog/assets/developer-floating-notes-workspace.jpg" width="270" height="180" alt="FloatBoard developer floating scratchpad workspace" loading="lazy">
<span class="ad-tile-badge">Ad · FloatBoard Desktop</span>
<h4>How Developers Eliminate 1,200 Alt-Tabs a Day with One Screen Pin</h4>
<p>Keep active API keys and curl templates floating directly above your code editor.</p>
</a>
<a href="/blog/instant-screenshot-capture-floating-reference/" class="ad-sponsored-tile">
<img src="/blog/assets/infinity-mirror-screenshot-reference.jpg" width="270" height="180" alt="Recursive screenshot reference in FloatBoard" loading="lazy">
<span class="ad-tile-badge">Ad · Screen Capture</span>
<h4>Stop Saving 80 Throwaway PNGs: The Instant Floating Capture Loop</h4>
<p>Pin screenshots immediately into an always-on-top workspace without saving files to disk.</p>
</a>
<a href="/pricing.html" class="ad-sponsored-tile">
<img src="/blog/assets/code-and-image-references.jpg" width="270" height="152" alt="FloatBoard side by side code and image references" loading="lazy">
<span class="ad-tile-badge">Ad · Limited Offer</span>
<h4>Get 50% Off Lifetime FloatBoard License ($2.99 with Code DEVTO50)</h4>
<p>One-time payment, zero subscriptions, 100% offline security for personal &amp; commercial use.</p>
</a>
<a href="/web-pad/" class="ad-sponsored-tile">
<img src="/blog/assets/design-tokens-and-mockup-board.jpg" width="270" height="180" alt="Design tokens and mockups pinned in FloatBoard" loading="lazy">
<span class="ad-tile-badge">Ad · WebPad Free</span>
<h4>Try Floating Notes Right in Your Browser with Zero Installation</h4>
<p>Leverage Document Picture-in-Picture to keep live notes above all desktop apps.</p>
</a>
</div>
</section>'''

sticky_dock = '''<aside class="ad-anchor-bar" aria-label="FloatBoard Offer">
<div class="ad-anchor-inner">
<div class="ad-anchor-left">
<span class="ad-iab-badge">AD</span>
<div class="ad-anchor-text-wrap">
<strong class="ad-anchor-title">FloatBoard Pro — The #1 Floating Clipboard &amp; Reference Board for Windows 11, Mac &amp; Linux</strong>
<span class="ad-anchor-deal">Special Reader Deal: Get 50% OFF Lifetime/Pro Plan with Promo Code: <code>DEVTO50</code></span>
</div>
</div>
<div class="ad-anchor-actions"><a href="/download/" class="ad-anchor-btn">Download Free + Claim 50% Off →</a></div>
</div>
</aside>'''
footer = '<footer class="guide-footer"><a href="/">FloatBoard</a><a href="/clipboard-manager.html">Floating Clipboard Manager</a><a href="/floating-notes.html">Always on Top Sticky Notes</a><a href="/download/">Download for Windows, Mac &amp; Linux</a><a href="/blog/about/">About this blog</a><a href="/pricing.html">Pricing</a><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a><a href="/#contact">Contact &amp; corrections</a></footer>'

def image(p, lazy=False):
    file = ROOT / 'blog/assets' / p['image']
    data = file.read_bytes()
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        width, height = struct.unpack('>II', data[16:24])
    elif data.startswith(b'\xff\xd8'):
        pos = 2
        while pos < len(data):
            if data[pos] != 0xff:
                raise ValueError(f'Invalid JPEG marker in {file}')
            while data[pos] == 0xff:
                pos += 1
            marker = data[pos]
            pos += 1
            if marker in (0xd8, 0xd9) or 0xd0 <= marker <= 0xd7:
                continue
            length = struct.unpack('>H', data[pos:pos + 2])[0]
            if marker in (0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf):
                height, width = struct.unpack('>HH', data[pos + 3:pos + 7])
                break
            pos += length
        else:
            raise ValueError(f'No JPEG dimensions found in {file}')
    else:
        raise ValueError(f'Unsupported image format: {file}')
    return f'<img src="/blog/assets/{esc(p["image"])}" width="{width}" height="{height}" alt="{esc(p["alt"])}" decoding="async" {"loading=\"lazy\"" if lazy else "fetchpriority=\"high\""}>'

def article_media(p):
    if not p.get('demo_video'):
        return image(p)
    video = ROOT / 'blog/assets' / p['demo_video']
    assert video.is_file(), f'Missing demo video: {video}'
    poster = f'/blog/assets/{esc(p["image"])}'
    return (f'<video class="guide-demo" width="960" height="540" controls muted playsinline preload="none" poster="{poster}" '
            f'aria-label="{esc(p["demo_alt"])}">'
            f'<source src="/blog/assets/{esc(p["demo_video"])}" type="video/mp4">'
            f'<a href="/blog/assets/{esc(p["demo_video"])}">Watch the recorded workflow</a>'
            '</video>')

def page(path, title, description, body, schema, picture=None):
    url = BASE + path
    social = BASE + '/blog/assets/' + picture if picture else BASE + '/icon.png'
    kind = 'article' if schema.get('@type') == 'BlogPosting' else 'website'
    main_class = 'guide-main guide-article-main' if kind == 'article' else 'guide-main'
    result = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | FloatBoard</title><meta name="description" content="{esc(description)}">
<link rel="canonical" href="{url}"><link rel="icon" href="/icon.png">
<link rel="stylesheet" href="/assets/content.css"><link rel="stylesheet" href="/blog/blog.css">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="FloatBoard"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{social}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{social}">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace('<', chr(92)+'u003c')}</script>
</head><body class="guide-page blog-page blog-light-mode"><a class="skip-link" href="#main">Skip to content</a>{promo_bar}{nav}<main id="main" class="{main_class}">{body}</main>{footer}</body></html>'''
    dest = ROOT / path.strip('/') / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(result)

audiences = {
    'clipboard': {
        'title': 'Clipboard and copied text',
        'description': 'For people moving text and images between desktop apps. Learn when recent clipboard history helps and when a short working note needs to stay visible.',
        'guide': '/clipboard-manager.html',
        'guide_label': 'See how FloatBoard handles copied text',
    },
    'floating-notes': {
        'title': 'Notes that stay in view',
        'description': 'For writing, learning, calls and debugging when the next instruction or reference disappears behind another window.',
        'guide': '/floating-notes.html',
        'guide_label': 'Explore floating desktop notes',
    },
    'visual-references': {
        'title': 'Small image working sets',
        'description': 'For designers who need a few images beside their work. Keep the original files elsewhere and use the board for the current decision.',
        'guide': '/floating-notes.html',
        'guide_label': 'See the text-and-image board',
    },
}
featured_order = {
    'windows-clipboard-history-vs-floating-notes': 0,
    'clear-copied-text-history-keep-working-set': 1,
    'keep-reference-notes-visible-while-writing': 0,
    'keep-meeting-notes-visible-video-call': 1,
    'code-snippets-and-screenshots': 2,
    'organize-image-references': 0,
    'compare-photos-side-by-side-windows': 1,
}
cards = {audience: [] for audience in audiences}
for p in posts:
    audience = p['audience']
    assert audience in audiences, f'Unknown audience for {p["slug"]}: {audience}'
    path = '/blog/' + p['slug'] + '/'
    toc = ''.join(f'<li><a href="#{s["id"]}">{esc(s["title"])}</a></li>' for s in p['sections'])
    in_content_ads = {
        1: ad_incontent_1,
        3: ad_incontent_2,
        5: ad_incontent_3,
    }
    if len(p['sections']) <= 3:
        in_content_ads = {1: ad_incontent_1, 2: ad_incontent_2}
    sections = ''.join(
        f'<section aria-labelledby="{s["id"]}"><h2 id="{s["id"]}">{esc(s["title"])}</h2>{s["html"]}</section>'
        + in_content_ads.get(index, '')
        for index, s in enumerate(p['sections'], start=1)
    )
    related = ''.join(f'<li><a href="/blog/{q["slug"]}/">{esc(q["title"])}</a></li>' for q in (posts_by_slug[slug] for slug in p['related_slugs']) if q != p)
    tags = ''.join(f'<li>{esc(tag)}</li>' for tag in p.get('tags', []))
    topic_list = f'<ul class="guide-tags" aria-label="Topics">{tags}</ul>' if tags else ''
    updated = f' · Updated <time datetime="{p["modified"]}">{date.fromisoformat(p["modified"]).strftime("%d %B %Y")}</time>' if p.get('modified') and p['modified'] != p['date'] else ''
    
    steps_li = ''.join(f'<li>{esc(st)}</li>' for st in p.get('quick_answer', []))
    quick_answer_row = f'''<div class="quick-answer-row">
<div class="quick-answer-card">
<div class="quick-answer-badge">⚡ Quick Answer (TL;DR — 3 Seconds):</div>
<ol class="quick-answer-steps">{steps_li}</ol>
</div>
<aside class="ad-card-iab ad-card-inline-promo" aria-label="Sponsored special offer">
<div class="ad-iab-badge-group"><span class="ad-iab-badge">AD</span><span class="ad-iab-brand">FloatBoard Pro</span></div>
<h4 class="ad-inline-title">FloatBoard Pro · 50% OFF</h4>
<p class="ad-inline-desc">Pin images, source URLs &amp; dev notes above VS Code or Chrome.</p>
<a href="/pricing.html" class="ad-inline-btn">Get Instant Access (Code: DEVTO50) →</a>
</aside>
</div>''' if p.get('quick_answer') else ''

    body = f'''<article class="article-layout blog-portal-grid"><aside class="portal-left-col" aria-label="Quick navigation and shortcuts"><div class="left-sticky-wrap"><nav class="portal-toc-box" aria-label="Quick navigation"><div class="portal-toc-header">📑 Quick Navigation</div><ol class="portal-toc-list">{toc}</ol></nav>{ad_left_skyscraper}</div></aside><div class="article-content article-main-card"><a href="/blog/" class="portal-back-link">← All guides</a><header class="article-header"><div class="portal-category-pill">{esc(p['category'])}</div><h1>{esc(p['title'])}</h1><p class="byline">By <a href="/blog/about/">FloatBoard</a> · Published <time datetime="{p['date']}">{date.fromisoformat(p["date"]).strftime("%d %B %Y")}</time>{updated}</p>{topic_list}{ad_leaderboard_top}<p class="guide-intro">{esc(p['intro'])}</p></header><figure class="article-hero-figure">{article_media(p)}<figcaption>{esc(p['caption'])}</figcaption></figure>{quick_answer_row}<div class="article-body">{sections}</div>{ad_sponsored_grid}<aside class="related"><h2>Related workflows</h2><ul>{related}</ul></aside></div><aside class="article-sidebar portal-right-col" aria-label="Sponsored display advertisements"><div class="sidebar-sticky-wrap">{ad_sidebar_300x600}{ad_sidebar_300x250_emerald}{ad_sidebar_sponsored_links}{ad_sidebar_sticky_offer}</div></aside></article>{sticky_dock}'''
    schema = {'@context':'https://schema.org','@type':'BlogPosting','headline':p['title'],'description':p['description'],'image':[BASE+'/blog/assets/'+p['image']],'datePublished':p['date'],'dateModified':p.get('modified',p['date']),'mainEntityOfPage':BASE+path,'author':{'@type':'Organization','name':'FloatBoard','url':BASE+'/blog/about/'},'publisher':{'@type':'Organization','name':'FloatBoard','url':BASE+'/'}}
    if p.get('tags'):
        schema['keywords'] = p['tags']
    page(path,p['title'],p['description'],body,schema,p['image'])
    cards[audience].append((featured_order.get(p['slug'], 100), -date.fromisoformat(p['date']).toordinal(), f'<article class="blog-card"><a href="{path}" aria-label="{esc(p["title"])}">{image(p,True)}</a><div><p class="guide-eyebrow">{esc(p["category"])}</p><h3><a href="{path}">{esc(p["title"])}</a></h3><p>{esc(p["description"])}</p><a href="{path}">Read the guide →</a></div></article>'))

blog_sections = []
for key, info in audiences.items():
    entries = ''.join(markup for _, _, markup in sorted(cards[key]))
    blog_sections.append(f'<section id="{key}" class="blog-topic" aria-labelledby="{key}-heading"><h2 id="{key}-heading">{info["title"]}</h2><p>{info["description"]} <a href="{info["guide"]}">{info["guide_label"]}</a>.</p><div class="blog-grid">{entries}</div></section>')

blog_intro = '''<header><p class="guide-eyebrow">The FloatBoard blog</p>
<h1>Keep copied text, notes and images visible while you work</h1>
<p class="guide-intro">FloatBoard is a desktop working board for short notes and image references that can stay above your other windows. Start with the task you do across apps: copy something, keep a note in sight, or compare a few images. These guides show where the board helps and where a dedicated tool is a better fit.</p>
<p><a href="/download/">Try FloatBoard on your desktop</a> or read the <a href="/clipboard-manager.html">clipboard</a> and <a href="/floating-notes.html">floating-notes</a> overviews.</p>
</header><nav class="blog-topic-nav" aria-label="Guide topics"><a href="#clipboard">Clipboard and copied text</a><a href="#floating-notes">Notes that stay in view</a><a href="#visual-references">Small image working sets</a></nav>'''
blog_outro = '<section><h2>About these guides</h2><p>Published by FloatBoard, the app featured in these examples. Each guide addresses a specific workflow and explains when another tool is a better fit. <a href="/blog/about/">Read our editorial approach</a>.</p></section>'
page('/blog/','FloatBoard Guides: Windows 11, Mac & Linux Multitasking, Clipboard & Floating Notes Tips','Practical FloatBoard guides for keeping copied text, short notes and a few image references visible while working across desktop apps.', blog_intro + ''.join(blog_sections) + blog_outro,{'@context':'https://schema.org','@type':'Blog','name':'FloatBoard Blog','url':BASE+'/blog/'})
page('/blog/about/','About FloatBoard – The Offline Always-on-Top Floating Clipboard & Scratchpad for Desktop','Who publishes the FloatBoard blog, how its workflow guides are created, and how to report an error.', '''<h1>About the FloatBoard blog</h1><p class="guide-intro">This is FloatBoard’s official product blog. We publish practical guides for people working with desktop notes, copied text and image references.</p><section><h2>Who publishes these guides</h2><p>The publisher is FloatBoard, the application featured on this website. These are product guides, not independent reviews. For the app’s source and release history, visit the <a href="https://github.com/nazihyazan/floating_board">FloatBoard project</a> and <a href="https://github.com/nazihyazan/mac_test/releases">Linux releases</a>.</p></section><section><h2>How the guides are prepared</h2><p>These guides are drafted with AI assistance using product screenshots and recorded demonstrations supplied by the app owner, FloatBoard product information and linked primary documentation. The visuals illustrate workflows at the time captured; examples are not measured productivity studies. Older recordings may show controls or website copy that has since changed. We do not claim that a feature was independently tested unless the article documents that test.</p><p>We keep each guide focused on one task, describe limitations, link to current pricing and downloads, and avoid invented ratings, customer quotations or performance claims. Features and layouts can differ between versions.</p></section><section><h2>Corrections and updates</h2><p>If an instruction does not match your version, <a href="/#contact">contact FloatBoard</a> with the article URL, your operating system and app version. Publication dates identify the original articles; revision dates should change only when the content changes substantially.</p></section><p><a href="/blog/">Explore the guides</a></p>''',{'@context':'https://schema.org','@type':'AboutPage','name':'About the FloatBoard blog','url':BASE+'/blog/about/'})

ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
tree = ET.parse(ROOT/'sitemap.xml')
modified_dates = {'/blog/': max(p.get('modified', p['date']) for p in posts), '/blog/about/': '2026-10-05'}
modified_dates.update({'/blog/'+p['slug']+'/': p.get('modified', p['date']) for p in posts})
for path, modified in modified_dates.items():
    entry = next((x for x in tree.getroot() if x.find(ns+'loc') is not None and x.find(ns+'loc').text == BASE+path), None)
    if entry is None:
        el = ET.SubElement(tree.getroot(), ns+'url')
        ET.SubElement(el, ns+'loc').text=BASE+path
        ET.SubElement(el, ns+'lastmod').text=modified
    else:
        lastmod = entry.find(ns+'lastmod')
        if lastmod is None:
            lastmod = ET.SubElement(entry, ns+'lastmod')
        lastmod.text = max(lastmod.text or modified, modified)
ET.indent(tree, space='  ')
tree.write(ROOT/'sitemap.xml',encoding='UTF-8',xml_declaration=True)
sitemap_content = (ROOT/'sitemap.xml').read_text(encoding='utf-8')
if sitemap_content.startswith("<?xml version='1.0' encoding='UTF-8'?>"):
    sitemap_content = sitemap_content.replace("<?xml version='1.0' encoding='UTF-8'?>", '<?xml version="1.0" encoding="UTF-8"?>', 1)
if not sitemap_content.endswith('\n'):
    sitemap_content += '\n'
(ROOT/'sitemap.xml').write_text(sitemap_content, encoding='utf-8')
(ROOT/'sitemap-main.xml').write_text(sitemap_content, encoding='utf-8')
print('Built blog index, about page and',len(posts),'articles.')
