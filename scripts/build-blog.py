"""Generate static blog pages with UiSavior cosmic design system across multiple color palettes."""
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

# 6 Radiant Cosmic Color Palettes inspired by UiSavior, Pelmatech, FluxEdit & Solix
PALETTES = [
    {
        'id': 'cyber-blue',
        'name': 'Electric Cyber Blue & Neon Coral',
        'primary': '#0297de',
        'primary_rgb': '2, 151, 222',
        'secondary': '#fc734d',
        'secondary_rgb': '252, 115, 77',
        'accent': '#fd91cc',
        'accent_rgb': '253, 145, 204',
        'dark_bg': '#02070a',
        'card_bg': 'rgba(13, 22, 32, 0.72)',
        'btn_gradient': 'linear-gradient(135deg, #0297de, #016fa3)',
        'btn_hover_gradient': 'linear-gradient(135deg, #05a7f5, #0297de)',
        'cta_gradient': 'linear-gradient(135deg, #fc734d 0%, #d83995 100%)',
    },
    {
        'id': 'aurora-coral',
        'name': 'Neon Aurora Coral & Sunset Tangerine',
        'primary': '#ff5c77',
        'primary_rgb': '255, 92, 119',
        'secondary': '#ff9345',
        'secondary_rgb': '255, 147, 69',
        'accent': '#c084fc',
        'accent_rgb': '192, 132, 252',
        'dark_bg': '#070308',
        'card_bg': 'rgba(26, 14, 28, 0.72)',
        'btn_gradient': 'linear-gradient(135deg, #ff5c77, #d93855)',
        'btn_hover_gradient': 'linear-gradient(135deg, #ff7a91, #ff5c77)',
        'cta_gradient': 'linear-gradient(135deg, #ff9345 0%, #ff5c77 100%)',
    },
    {
        'id': 'amethyst-violet',
        'name': 'Deep Amethyst Violet & Aqua Cyan',
        'primary': '#a855f7',
        'primary_rgb': '168, 85, 247',
        'secondary': '#06b6d4',
        'secondary_rgb': '6, 182, 212',
        'accent': '#ec4899',
        'accent_rgb': '236, 72, 153',
        'dark_bg': '#05030b',
        'card_bg': 'rgba(20, 15, 34, 0.72)',
        'btn_gradient': 'linear-gradient(135deg, #a855f7, #7e22ce)',
        'btn_hover_gradient': 'linear-gradient(135deg, #c084fc, #a855f7)',
        'cta_gradient': 'linear-gradient(135deg, #06b6d4 0%, #a855f7 100%)',
    },
    {
        'id': 'emerald-matrix',
        'name': 'Obsidian Emerald & Cyber Mint',
        'primary': '#10b981',
        'primary_rgb': '16, 185, 129',
        'secondary': '#06b6d4',
        'secondary_rgb': '6, 182, 212',
        'accent': '#3b82f6',
        'accent_rgb': '59, 130, 246',
        'dark_bg': '#020a06',
        'card_bg': 'rgba(10, 24, 18, 0.72)',
        'btn_gradient': 'linear-gradient(135deg, #10b981, #047857)',
        'btn_hover_gradient': 'linear-gradient(135deg, #34d399, #10b981)',
        'cta_gradient': 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)',
    },
    {
        'id': 'fuchsia-neon',
        'name': 'Electric Fuchsia & Sky Blue',
        'primary': '#f43f5e',
        'primary_rgb': '244, 63, 94',
        'secondary': '#38bdf8',
        'secondary_rgb': '56, 189, 248',
        'accent': '#a855f7',
        'accent_rgb': '168, 85, 247',
        'dark_bg': '#0a0206',
        'card_bg': 'rgba(28, 12, 22, 0.72)',
        'btn_gradient': 'linear-gradient(135deg, #f43f5e, #be123c)',
        'btn_hover_gradient': 'linear-gradient(135deg, #fb7185, #f43f5e)',
        'cta_gradient': 'linear-gradient(135deg, #f43f5e 0%, #38bdf8 100%)',
    },
    {
        'id': 'solar-amber',
        'name': 'Solar Amber & Flame Gold',
        'primary': '#f59e0b',
        'primary_rgb': '245, 158, 11',
        'secondary': '#ef4444',
        'secondary_rgb': '239, 68, 68',
        'accent': '#8b5cf6',
        'accent_rgb': '139, 92, 246',
        'dark_bg': '#090601',
        'card_bg': 'rgba(26, 18, 8, 0.72)',
        'btn_gradient': 'linear-gradient(135deg, #f59e0b, #b45309)',
        'btn_hover_gradient': 'linear-gradient(135deg, #fbbf24, #f59e0b)',
        'cta_gradient': 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)',
    },
]

nav = '''<nav class="guide-nav" aria-label="Main navigation">
<div class="guide-nav-content">
<a class="guide-brand" href="/">
<span class="guide-logo-dot"></span>
<span class="guide-brand-text">FloatBoard</span>
</a>
<div class="guide-nav-links">
<a href="/">Overview</a>
<a href="/clipboard-manager">Clipboard</a>
<a href="/compare/floatboard-vs-powertoys-always-on-top">vs PowerToys</a>
<a href="/blog/">Editorial</a>
<a href="/pricing">Pricing</a>
</div>
<a href="/download/" class="guide-nav-btn">Download Free</a>
</div>
</nav>'''

announcement_bar = '''<aside class="editorial-top-announcement" aria-label="Product announcement">
<span>FloatBoard 1.0 — 100% offline always-on-top floating notes &amp; clipboard manager.</span>
<a href="/pricing">Get $5.99 lifetime license →</a>
</aside>'''

sidebar_download_card = '''<div class="editorial-card-sidebar" aria-label="Download FloatBoard">
<div class="editorial-sidebar-brand">
<img src="/icon.png" width="30" height="30" alt="FloatBoard icon" class="guide-brand-icon">
<div>
<h4 class="editorial-sidebar-title">FloatBoard</h4>
<p class="editorial-sidebar-sub">Windows, Mac &amp; Linux</p>
</div>
</div>
<p class="editorial-sidebar-desc">Pin scratchpad notes, code snippets, and reference images directly above your active apps.</p>
<a href="/download/" class="editorial-btn-black">Download Free App →</a>
<span class="editorial-card-footnote">$5.99 Lifetime · Offline Privacy</span>
</div>'''

incontent_dark_card = '''<div class="editorial-dark-card" aria-label="Product showcase">
<h3 class="editorial-dark-heading">FLOATBOARD.</h3>
<p class="editorial-dark-sub">Stop paying the Alt-Tab tax. Keep active notes, API keys, and reference screenshots pinned permanently above your browser or code editor. 100% offline local memory.</p>
<div class="editorial-dark-actions">
<a href="/download/" class="editorial-btn-coral">Download Free App →</a>
<span class="editorial-dark-price">$5.99 Lifetime · No Subscriptions</span>
</div>
</div>'''

footer = '<footer class="guide-footer"><a href="/">FloatBoard</a><a href="/clipboard-manager">Clipboard Manager</a><a href="/download/">Download App</a><a href="/compare/floatboard-vs-powertoys-always-on-top">vs PowerToys</a><a href="/alternatives/pureref-with-text-and-clipboard">vs PureRef</a><a href="/alternatives/windows-sticky-notes-always-on-top">vs Sticky Notes</a><a href="/alternatives/ditto-copyq-visual-clipboard">vs Ditto</a><a href="/linux/floating-clipboard-notes-ubuntu">Linux Guide</a><a href="/web-pad/">Online WebPad</a><a href="/blog/about/">About Blog</a><a href="/pricing">Pricing</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a></footer>'

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
    return (f'<video class="guide-demo" width="960" height="540" autoplay muted loop playsinline controls preload="none" poster="{poster}" '
            f'aria-label="{esc(p["demo_alt"])}">'
            f'<source src="/blog/assets/{esc(p["demo_video"])}" type="video/mp4">'
            f'<a href="/blog/assets/{esc(p["demo_video"])}">Watch the recorded workflow</a>'
            '</video>')

def generate_palette_style(pal):
    if not pal:
        return ''
    return f'''<style>
:root, body.blog-page.uisavior-theme {{
  --theme-primary: {pal['primary']};
  --theme-primary-rgb: {pal['primary_rgb']};
  --theme-secondary: {pal['secondary']};
  --theme-secondary-rgb: {pal['secondary_rgb']};
  --theme-accent: {pal['accent']};
  --theme-accent-rgb: {pal['accent_rgb']};
  --theme-dark-bg: {pal['dark_bg']};
  --theme-card-bg: {pal['card_bg']};
  --theme-btn-gradient: {pal['btn_gradient']};
  --theme-btn-hover: {pal['btn_hover_gradient']};
  --theme-cta-gradient: {pal['cta_gradient']};
  --border-glow: rgba({pal['primary_rgb']}, 0.35);
}}
body.blog-page.uisavior-theme {{
  background-color: {pal['dark_bg']} !important;
}}
.uisavior-aurora {{
  background: 
    radial-gradient(circle at 50% -8%, rgba({pal['primary_rgb']}, 0.38) 0%, rgba({pal['primary_rgb']}, 0.08) 45%, transparent 72%),
    radial-gradient(circle at 10% 25%, rgba({pal['secondary_rgb']}, 0.22) 0%, transparent 48%),
    radial-gradient(circle at 90% 28%, rgba({pal['accent_rgb']}, 0.18) 0%, transparent 48%),
    radial-gradient(circle at 50% 68%, rgba({pal['primary_rgb']}, 0.15) 0%, transparent 60%) !important;
}}
.uisavior-matrix {{
  background-image: radial-gradient(rgba({pal['primary_rgb']}, 0.2) 1.2px, transparent 1.2px) !important;
}}
</style>'''

def page(path, title, description, body, schema, picture=None, palette=None):
    url = BASE + path
    social = BASE + '/blog/assets/' + picture if picture else BASE + '/icon.png'
    is_article = schema.get('@type') == 'BlogPosting' or any(x.get('@type') == 'BlogPosting' for x in schema.get('@graph', []))
    kind = 'article' if is_article else 'website'
    title_tag = f"{esc(title)} | FloatBoard" if len(title) <= 46 else esc(title)
    style_block = generate_palette_style(palette)
    result = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_tag}</title><meta name="description" content="{esc(description)}">
<link rel="canonical" href="{url}"><link rel="icon" href="/icon.png">
<link rel="stylesheet" href="/blog/blog.css?v=20261107b">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="FloatBoard"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{social}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{social}">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace('<', chr(92)+'u003c')}</script>
{style_block}
</head><body class="blog-page uisavior-theme"><div class="uisavior-aurora"></div><div class="uisavior-matrix"></div><a class="skip-link" href="#main">Skip to content</a>{announcement_bar}{nav}<main id="main">{body}</main>{footer}<script>document.addEventListener("DOMContentLoaded",function(){{var v=document.querySelector("video.guide-demo");if(v){{v.muted=true;v.play().catch(function(){{}});}}}});</script><!-- 100% privacy-first analytics --><script data-collect-dnt="true" data-detect-404="true" async src="https://scripts.simpleanalyticscdn.com/latest.js"></script></body></html>'''
    dest = ROOT / path.strip('/') / 'index.html'
    custom_themed_slugs = {
        'blog/clear-copied-text-history-keep-working-set',
        'blog/how-to-copy-images-from-websites-directly-to-board',
        'blog/screenshot-and-copy-text-from-screen-windows-11',
        'blog/side-by-side-image-comparison-reference-board',
    }
    if path.strip('/') in custom_themed_slugs:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(result)

audiences = {
    'clipboard': {
        'title': 'Clipboard & Copied Text',
        'description': 'For people moving text and images between desktop apps. Learn when recent clipboard history helps and when a short working note needs to stay visible.',
        'guide': '/clipboard-manager.html',
        'guide_label': 'Explore Clipboard Manager',
    },
    'floating-notes': {
        'title': 'Notes That Stay In View',
        'description': 'For writing, learning, calls and debugging when the next instruction or reference disappears behind another window.',
        'guide': '/download/',
        'guide_label': 'Download FloatBoard Free',
    },
    'visual-references': {
        'title': 'Image References & Boards',
        'description': 'For designers and developers who need visual assets beside their work. Keep the original files safe and use the floating board for active decisions.',
        'guide': '/download/',
        'guide_label': 'Download Reference Board',
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
for post_index, p in enumerate(posts):
    audience = p['audience']
    assert audience in audiences, f'Unknown audience for {p["slug"]}: {audience}'
    palette = PALETTES[post_index % len(PALETTES)]
    path = '/blog/' + p['slug'] + '/'
    toc = ''.join(f'<li><a href="#{s["id"]}">{esc(s["title"])}</a></li>' for s in p['sections'])
    sections = ''.join(
        f'<section aria-labelledby="{s["id"]}"><h2 id="{s["id"]}">{esc(s["title"])}</h2>{s["html"]}</section>'
        + (incontent_dark_card if index == 2 else '')
        for index, s in enumerate(p['sections'], start=1)
    )
    related_cards = ''.join(
        f'<a href="/blog/{q["slug"]}/" class="editorial-related-card"><span>{esc(q.get("category", "Guide"))}</span><h3>{esc(q["title"])}</h3></a>'
        for q in (posts_by_slug[slug] for slug in p['related_slugs']) if q != p
    )
    updated = f' · Updated <time datetime="{p["modified"]}">{date.fromisoformat(p["modified"]).strftime("%B %d, %Y")}</time>' if p.get('modified') and p['modified'] != p['date'] else ''
    
    steps_li = ''.join(f'<li>{esc(st)}</li>' for st in p.get('quick_answer', []))
    quick_answer_row = f'''<div class="editorial-quick-answer">
<div class="editorial-quick-title"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg> <span>Quick Workflow Summary (TL;DR)</span></div>
<ol class="editorial-quick-steps">{steps_li}</ol>
</div>''' if p.get('quick_answer') else ''

    body = f'''<article class="editorial-wrapper">
<header class="editorial-hero-header">
<div class="editorial-badge-row">
<span class="editorial-category-badge">{esc(p['category'])}</span>
<a href="/blog/" class="editorial-back-link">← All guides</a>
</div>
<h1 class="editorial-title">{esc(p['title'])}</h1>
<p class="editorial-intro-text">{esc(p['intro'])}</p>
<div class="editorial-meta-row">
<span>By <a href="/blog/about/">FloatBoard</a></span>
<span>·</span>
<time datetime="{p['date']}">{date.fromisoformat(p["date"]).strftime("%B %d, %Y")}</time>
{updated}
<span>·</span>
<span>5 min read</span>
</div>
</header>
<figure class="editorial-hero-figure uisavior-mockup-window">
<div class="uisavior-mockup-header">
<div class="uisavior-mockup-dots">
<span class="uisavior-dot r"></span>
<span class="uisavior-dot y"></span>
<span class="uisavior-dot g"></span>
</div>
<div class="uisavior-mockup-title">
<span class="active-indicator"></span>
<span>FloatBoard Native · {esc(p['category'])}</span>
</div>
<span class="uisavior-mockup-badge">ACTIVE BOARD</span>
</div>
<div class="uisavior-mockup-body">
{article_media(p)}
</div>
<figcaption class="uisavior-mockup-footer">
<span>{esc(p['caption'])}</span>
<span class="uisavior-tag">OFFLINE // 100% LOCAL</span>
</figcaption>
</figure>
<div class="uisavior-chips-row">
<div class="uisavior-chip">
<div class="uisavior-chip-icon chip-accent-1">
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
</div>
<div class="uisavior-chip-content">
<h4>Always-on-Top Scratchpad</h4>
<p>Pin notes and reference crops above active full-screen applications</p>
</div>
</div>
<div class="uisavior-chip">
<div class="uisavior-chip-icon chip-accent-2">
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
</div>
<div class="uisavior-chip-content">
<h4>100% Offline Local Storage</h4>
<p>Never touches third-party cloud servers or telemetry analytics</p>
</div>
</div>
</div>
<div class="editorial-grid">
<aside class="editorial-left-col" aria-label="Table of contents and app download">
<div class="editorial-outline-box">
<div class="editorial-outline-title">Outline</div>
<ul class="editorial-outline-list">
{toc}
</ul>
</div>
{sidebar_download_card}
</aside>
<div class="editorial-content-col">
{quick_answer_row}
<div class="editorial-article-sheet">
<div class="editorial-article-body">
{sections}
</div>
</div>
<section class="editorial-related-section">
<h2>Related Guides &amp; Workflows</h2>
<div class="editorial-related-grid">
{related_cards}
</div>
</section>
</div>
</div>
</article>'''

    faq_questions = []
    for s in p['sections']:
        if 'faq' in s['id'].lower():
            import re
            items = re.findall(r'<h3>(.*?)</h3>\s*<p>(.*?)</p>', s['html'], re.DOTALL)
            for q_text, a_text in items:
                clean_q = re.sub(r'<[^>]+>', '', q_text).strip()
                clean_a = re.sub(r'<[^>]+>', '', a_text).strip()
                if clean_q and clean_a:
                    faq_questions.append({
                        '@type': 'Question',
                        'name': clean_q,
                        'acceptedAnswer': {
                            '@type': 'Answer',
                            'text': clean_a
                        }
                    })
    article_schema = {'@type':'BlogPosting','headline':p['title'],'description':p['description'],'image':[BASE+'/blog/assets/'+p['image']],'datePublished':p['date'],'dateModified':p.get('modified',p['date']),'mainEntityOfPage':BASE+path,'author':{'@type':'Organization','name':'FloatBoard','url':BASE+'/blog/about/'},'publisher':{'@type':'Organization','name':'FloatBoard','url':BASE+'/'}}
    if p.get('tags'):
        article_schema['keywords'] = p['tags']
    if faq_questions:
        schema = {
            '@context': 'https://schema.org',
            '@graph': [
                article_schema,
                {
                    '@type': 'FAQPage',
                    'mainEntity': faq_questions
                }
            ]
        }
    else:
        schema = {'@context':'https://schema.org', **article_schema}
    page(path,p['title'],p['description'],body,schema,p['image'],palette=palette)
    cards[audience].append((featured_order.get(p['slug'], 100), -date.fromisoformat(p['date']).toordinal(), f'<article class="blog-card"><a href="{path}" aria-label="{esc(p["title"])}">{image(p,True)}</a><div><p class="guide-eyebrow">{esc(p["category"])}</p><h3><a href="{path}">{esc(p["title"])}</a></h3><p>{esc(p["description"])}</p><a href="{path}">Read article →</a></div></article>'))

blog_sections = []
for key, info in audiences.items():
    entries = ''.join(markup for _, _, markup in sorted(cards[key]))
    blog_sections.append(f'<section id="{key}" class="blog-topic" aria-labelledby="{key}-heading"><h2 id="{key}-heading">{info["title"]}</h2><p>{info["description"]} <a href="{info["guide"]}">{info["guide_label"]}</a>.</p><div class="blog-grid">{entries}</div></section>')

blog_intro = '''<header class="editorial-wrapper editorial-index-header">
<div class="editorial-badge-row" style="justify-content: center; margin-bottom: 16px;">
<span class="editorial-category-badge">KNOWLEDGE BASE &amp; GUIDES</span>
</div>
<h1 class="editorial-title">Keep copied text, notes and images visible while you work</h1>
<p class="editorial-intro-text">FloatBoard is a desktop working board for short notes and image references that stays above your other windows. Explore practical workflow guides, alternatives comparisons, and multi-clipboard tips.</p>
</header>'''
blog_outro = '''<section class="editorial-wrapper editorial-index-about">
<div class="editorial-about-card">
<h2>About these guides</h2>
<p>Published by FloatBoard, the app featured in these examples. Each guide addresses a specific workflow and explains when another tool is a better fit. <a href="/blog/about/">Read our editorial approach →</a></p>
</div>
</section>'''
page('/blog/','FloatBoard Guides: Windows 11, Mac & Linux Multitasking, Clipboard & Floating Notes Tips','Practical FloatBoard guides for keeping copied text, short notes and a few image references visible while working across desktop apps.', blog_intro + ''.join(blog_sections) + blog_outro,{'@context':'https://schema.org','@type':'Blog','name':'FloatBoard Blog','url':BASE+'/blog/'}, palette=PALETTES[0])

about_body = '''<article class="editorial-wrapper editorial-about-page" style="max-width: 860px; margin: 0 auto;">
<div class="editorial-badge-row">
<span class="editorial-category-badge">EDITORIAL POLICY</span>
<a href="/blog/" class="editorial-back-link">← Back to guides</a>
</div>
<h1 class="editorial-title">About the FloatBoard blog</h1>
<p class="editorial-intro-text">This is FloatBoard’s official product blog. We publish practical guides for people working with desktop notes, copied text and image references.</p>
<div class="editorial-about-sections">
<section>
<h2>Who publishes these guides</h2>
<p>The publisher is FloatBoard, the application featured on this website. These are product guides, not independent reviews. For the app’s source and release history, visit the <a href="https://github.com/nazihyazan/floating_board">FloatBoard project</a> and <a href="https://github.com/nazihyazan/mac_test/releases">Linux releases</a>.</p>
</section>
<section>
<h2>How the guides are prepared</h2>
<p>These guides are drafted with AI assistance using product screenshots and recorded demonstrations supplied by the app owner, FloatBoard product information and linked primary documentation. We keep each guide focused on one task, describe limitations, link to current pricing and downloads, and avoid invented ratings, customer quotations or performance claims.</p>
</section>
<section>
<h2>Corrections and updates</h2>
<p>If an instruction does not match your version, <a href="/#contact">contact FloatBoard</a> with the article URL, your operating system and app version.</p>
</section>
</div>
<p style="margin-top: 32px;"><a href="/blog/" style="color: var(--theme-secondary); font-weight: 700; text-decoration: none;">← Back to guides</a></p>
</article>'''
page('/blog/about/','About FloatBoard – The Offline Always-on-Top Floating Clipboard & Scratchpad for Desktop','Who publishes the FloatBoard blog, how its workflow guides are created, and how to report an error.', about_body,{'@context':'https://schema.org','@type':'AboutPage','name':'About the FloatBoard blog','url':BASE+'/blog/about/'}, palette=PALETTES[2])

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
print('Built editorial blog index, about page and',len(posts),'articles.')
