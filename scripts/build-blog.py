"""Generate static blog pages with clean editorial magazine layout (inspired by The Canvas)."""
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

nav = '''<nav class="guide-nav" aria-label="Main navigation">
<a class="guide-brand" href="/">
<img src="/icon.png" width="26" height="26" alt="FloatBoard" class="guide-brand-icon">
<span>FLOATBOARD BLOG.</span>
</a>
<div class="guide-nav-links">
<a href="/blog/">Guides</a>
<a href="/floating-notes.html">Floating Notes</a>
<a href="/clipboard-manager.html">Clipboard</a>
<a href="/pricing.html">Pricing</a>
<a href="/download/" class="guide-nav-btn">Download Free</a>
</div>
</nav>'''

announcement_bar = '''<aside class="editorial-top-announcement" aria-label="Product announcement">
FloatBoard 1.0 — 100% offline always-on-top floating notes &amp; clipboard manager. <a href="/pricing.html">Get $5.99 lifetime license →</a>
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

footer = '<footer class="guide-footer"><a href="/">FloatBoard</a><a href="/clipboard-manager.html">Clipboard Manager</a><a href="/floating-notes.html">Floating Notes</a><a href="/download/">Download App</a><a href="/compare/floatboard-vs-powertoys-always-on-top.html">vs PowerToys</a><a href="/alternatives/pureref-with-text-and-clipboard.html">vs PureRef</a><a href="/alternatives/windows-sticky-notes-always-on-top.html">vs Sticky Notes</a><a href="/alternatives/ditto-copyq-visual-clipboard.html">vs Ditto</a><a href="/linux/floating-clipboard-notes-ubuntu.html">Linux Guide</a><a href="/web-pad/">Online WebPad</a><a href="/blog/about/">About Blog</a><a href="/pricing.html">Pricing</a><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a></footer>'

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

def page(path, title, description, body, schema, picture=None):
    url = BASE + path
    social = BASE + '/blog/assets/' + picture if picture else BASE + '/icon.png'
    is_article = schema.get('@type') == 'BlogPosting' or any(x.get('@type') == 'BlogPosting' for x in schema.get('@graph', []))
    kind = 'article' if is_article else 'website'
    title_tag = f"{esc(title)} | FloatBoard" if len(title) <= 46 else esc(title)
    result = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_tag}</title><meta name="description" content="{esc(description)}">
<link rel="canonical" href="{url}"><link rel="icon" href="/icon.png">
<link rel="stylesheet" href="/blog/blog.css">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="FloatBoard"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{social}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{social}">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace('<', chr(92)+'u003c')}</script>
</head><body class="blog-page"><a class="skip-link" href="#main">Skip to content</a>{announcement_bar}{nav}<main id="main">{body}</main>{footer}<script>document.addEventListener("DOMContentLoaded",function(){{var v=document.querySelector("video.guide-demo");if(v){{v.muted=true;v.play().catch(function(){{}});}}}});</script></body></html>'''
    dest = ROOT / path.strip('/') / 'index.html'
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
        'guide': '/floating-notes.html',
        'guide_label': 'Explore Floating Desktop Notes',
    },
    'visual-references': {
        'title': 'Image References & Boards',
        'description': 'For designers and developers who need visual assets beside their work. Keep the original files safe and use the floating board for active decisions.',
        'guide': '/floating-notes.html',
        'guide_label': 'Explore Reference Board',
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
<div class="editorial-quick-title">⚡ Quick Workflow Summary (TL;DR)</div>
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
<figure class="editorial-hero-figure">
{article_media(p)}
<figcaption>{esc(p['caption'])}</figcaption>
</figure>
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
    page(path,p['title'],p['description'],body,schema,p['image'])
    cards[audience].append((featured_order.get(p['slug'], 100), -date.fromisoformat(p['date']).toordinal(), f'<article class="blog-card"><a href="{path}" aria-label="{esc(p["title"])}">{image(p,True)}</a><div><p class="guide-eyebrow">{esc(p["category"])}</p><h3><a href="{path}">{esc(p["title"])}</a></h3><p>{esc(p["description"])}</p><a href="{path}">Read article →</a></div></article>'))

blog_sections = []
for key, info in audiences.items():
    entries = ''.join(markup for _, _, markup in sorted(cards[key]))
    blog_sections.append(f'<section id="{key}" class="blog-topic" aria-labelledby="{key}-heading"><h2 id="{key}-heading">{info["title"]}</h2><p>{info["description"]} <a href="{info["guide"]}">{info["guide_label"]}</a>.</p><div class="blog-grid">{entries}</div></section>')

blog_intro = '''<header class="editorial-wrapper"><p class="guide-eyebrow">The FloatBoard Blog</p>
<h1 class="editorial-title">Keep copied text, notes and images visible while you work</h1>
<p class="editorial-intro-text">FloatBoard is a desktop working board for short notes and image references that stays above your other windows. Explore practical workflow guides, alternatives comparisons, and multi-clipboard tips.</p>
</header>'''
blog_outro = '<section class="editorial-wrapper"><h2>About these guides</h2><p>Published by FloatBoard, the app featured in these examples. Each guide addresses a specific workflow and explains when another tool is a better fit. <a href="/blog/about/">Read our editorial approach</a>.</p></section>'
page('/blog/','FloatBoard Guides: Windows 11, Mac & Linux Multitasking, Clipboard & Floating Notes Tips','Practical FloatBoard guides for keeping copied text, short notes and a few image references visible while working across desktop apps.', blog_intro + ''.join(blog_sections) + blog_outro,{'@context':'https://schema.org','@type':'Blog','name':'FloatBoard Blog','url':BASE+'/blog/'})
page('/blog/about/','About FloatBoard – The Offline Always-on-Top Floating Clipboard & Scratchpad for Desktop','Who publishes the FloatBoard blog, how its workflow guides are created, and how to report an error.', '''<article class="editorial-wrapper"><h1>About the FloatBoard blog</h1><p class="editorial-intro-text">This is FloatBoard’s official product blog. We publish practical guides for people working with desktop notes, copied text and image references.</p><section><h2>Who publishes these guides</h2><p>The publisher is FloatBoard, the application featured on this website. These are product guides, not independent reviews. For the app’s source and release history, visit the <a href="https://github.com/nazihyazan/floating_board">FloatBoard project</a> and <a href="https://github.com/nazihyazan/mac_test/releases">Linux releases</a>.</p></section><section><h2>How the guides are prepared</h2><p>These guides are drafted with AI assistance using product screenshots and recorded demonstrations supplied by the app owner, FloatBoard product information and linked primary documentation. We keep each guide focused on one task, describe limitations, link to current pricing and downloads, and avoid invented ratings, customer quotations or performance claims.</p></section><section><h2>Corrections and updates</h2><p>If an instruction does not match your version, <a href="/#contact">contact FloatBoard</a> with the article URL, your operating system and app version.</p></section><p><a href="/blog/">← Back to guides</a></p></article>''',{'@context':'https://schema.org','@type':'AboutPage','name':'About the FloatBoard blog','url':BASE+'/blog/about/'})

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
