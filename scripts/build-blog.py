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
nav = '''<nav class="guide-nav" aria-label="Main navigation">
<a class="guide-brand" href="/">
<img src="/icon.png" width="28" height="28" alt="FloatBoard" class="guide-brand-icon">
<span>FloatBoard</span>
</a>
<div class="guide-nav-links">
<a href="/blog/">Guides</a>
<a href="/floating-notes.html">Floating notes</a>
<a href="/clipboard-manager.html">Clipboard manager</a>
<a href="/pricing.html">Pricing</a>
<a href="/download/" class="guide-nav-btn">Download Free</a>
</div>
</nav>'''

announcement_bar = '''<aside class="blog-announcement-bar" aria-label="Product announcement">
<div class="announcement-content">
<span class="announcement-badge">Release</span>
<span class="announcement-text">FloatBoard Desktop — 100% offline floating clipboard &amp; notes. $5.99 lifetime license.</span>
<a href="/pricing.html" class="announcement-link">View lifetime pricing →</a>
</div>
</aside>'''

product_download_card = '''<div class="shadcn-card product-download-card" aria-label="Download FloatBoard">
<div class="card-header-flex">
<img src="/icon.png" width="38" height="38" alt="FloatBoard application icon" class="card-app-icon">
<div>
<h4 class="card-app-title">FloatBoard Desktop</h4>
<p class="card-app-meta">Windows 11, Mac &amp; Linux</p>
</div>
</div>
<p class="card-desc">Pin scratchpad notes, code snippets, and reference images directly above your active apps.</p>
<div class="feature-checklist">
<div><svg class="feature-check-icon" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd"/></svg> Always-on-top overlay</div>
<div><svg class="feature-check-icon" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd"/></svg> 100% Offline &amp; private</div>
<div><svg class="feature-check-icon" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd"/></svg> Multi-clipboard history</div>
<div><svg class="feature-check-icon" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd"/></svg> OCR text from screenshot</div>
</div>
<div class="card-actions-col">
<a href="/download/" class="btn-primary">Download Free Trial →</a>
<a href="/pricing.html" class="btn-secondary-link">$5.99 Lifetime · No Subscriptions</a>
</div>
</div>'''

incontent_spotlight = '''<div class="incontent-spotlight-card" aria-label="FloatBoard spotlight">
<span class="spotlight-badge">FloatBoard Spotlight</span>
<h3 class="spotlight-title">Keep Active Instructions Floating Above Your Work</h3>
<p class="spotlight-desc">Stop paying the Alt-Tab tax. FloatBoard keeps temporary notes, curl snippets, and screenshot references pinned permanently above your browser or code editor. 100% offline, lightweight, and private.</p>
<div class="spotlight-actions">
<a href="/download/" class="btn-spotlight-primary">Download Free App →</a>
<span class="spotlight-subtext">$5.99 lifetime license on <a href="/pricing.html">Pricing page</a>.</span>
</div>
</div>'''

sidebar_product_card = '''<div class="shadcn-card" aria-label="Product highlights">
<h4 class="sidebar-title">FloatBoard Desktop</h4>
<p class="card-desc">An offline reference board for Windows, macOS and Linux. Pin clipboard items, sticky notes and reference photos in one floating layer.</p>
<div class="card-actions-col">
<a href="/download/" class="btn-primary">Download Free →</a>
<a href="/pricing.html" class="btn-secondary-link">$5.99 Lifetime · Offline Privacy</a>
</div>
</div>'''

sidebar_comparisons_card = '''<div class="shadcn-card" aria-label="Alternative comparisons">
<h4 class="sidebar-title">Popular Comparisons</h4>
<div class="sidebar-links-list">
<a href="/alternatives/pureref-with-text-and-clipboard.html" class="sidebar-link-item">
<span class="sidebar-link-bullet">→</span>
<div><strong>FloatBoard vs PureRef</strong><span>Image board with rich notes &amp; clipboard.</span></div>
</a>
<a href="/compare/floatboard-vs-powertoys-always-on-top.html" class="sidebar-link-item">
<span class="sidebar-link-bullet">→</span>
<div><strong>vs PowerToys Always on Top</strong><span>Dedicated scratchpad vs generic window pin.</span></div>
</a>
<a href="/alternatives/windows-sticky-notes-always-on-top.html" class="sidebar-link-item">
<span class="sidebar-link-bullet">→</span>
<div><strong>vs Windows Sticky Notes</strong><span>Notes that stay visible above active apps.</span></div>
</a>
<a href="/alternatives/ditto-copyq-visual-clipboard.html" class="sidebar-link-item">
<span class="sidebar-link-bullet">→</span>
<div><strong>vs Ditto &amp; CopyQ</strong><span>Visual image clipboard history &amp; pinning.</span></div>
</a>
</div>
</div>'''

sidebar_resources_card = '''<div class="shadcn-card" aria-label="Helpful tools">
<h4 class="sidebar-title">More Resources</h4>
<div class="sidebar-links-list">
<a href="/web-pad/" class="sidebar-link-item">
<span class="sidebar-link-bullet">→</span>
<div><strong>Online Floating WebPad</strong><span>Free browser-based Picture-in-Picture pad.</span></div>
</a>
<a href="/linux/floating-clipboard-notes-ubuntu.html" class="sidebar-link-item">
<span class="sidebar-link-bullet">→</span>
<div><strong>Linux &amp; Ubuntu Guide</strong><span>Debian package &amp; Wayland setup.</span></div>
</a>
<a href="/blog/about/" class="sidebar-link-item">
<span class="sidebar-link-bullet">→</span>
<div><strong>Editorial Standards</strong><span>How we research and publish guides.</span></div>
</a>
</div>
</div>'''
footer = '<footer class="guide-footer"><a href="/">FloatBoard</a><a href="/clipboard-manager.html">Floating Clipboard Manager</a><a href="/floating-notes.html">Always on Top Sticky Notes</a><a href="/download/">Download for Windows, Mac &amp; Linux</a><a href="/compare/floatboard-vs-powertoys-always-on-top.html">vs PowerToys</a><a href="/alternatives/pureref-with-text-and-clipboard.html">PureRef Alternative</a><a href="/alternatives/windows-sticky-notes-always-on-top.html">Sticky Notes Alternative</a><a href="/alternatives/ditto-copyq-visual-clipboard.html">Ditto / CopyQ Alternative</a><a href="/linux/floating-clipboard-notes-ubuntu.html">Linux &amp; Ubuntu</a><a href="/web-pad/">Online Floating Notepad</a><a href="/blog/about/">About this blog</a><a href="/pricing.html">Pricing</a><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a><a href="/#contact">Contact &amp; corrections</a></footer>'

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
    is_article = schema.get('@type') == 'BlogPosting' or any(x.get('@type') == 'BlogPosting' for x in schema.get('@graph', []))
    kind = 'article' if is_article else 'website'
    main_class = 'guide-main guide-article-main' if kind == 'article' else 'guide-main'
    title_tag = f"{esc(title)} | FloatBoard" if len(title) <= 46 else esc(title)
    result = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_tag}</title><meta name="description" content="{esc(description)}">
<link rel="canonical" href="{url}"><link rel="icon" href="/icon.png">
<link rel="stylesheet" href="/assets/content.css"><link rel="stylesheet" href="/blog/blog.css">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="FloatBoard"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{social}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{social}">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace('<', chr(92)+'u003c')}</script>
</head><body class="guide-page blog-page blog-light-mode"><a class="skip-link" href="#main">Skip to content</a>{announcement_bar}{nav}<main id="main" class="{main_class}">{body}</main>{footer}</body></html>'''
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
    sections = ''.join(
        f'<section aria-labelledby="{s["id"]}"><h2 id="{s["id"]}">{esc(s["title"])}</h2>{s["html"]}</section>'
        + (incontent_spotlight if index == 2 else '')
        for index, s in enumerate(p['sections'], start=1)
    )
    related = ''.join(f'<li><a href="/blog/{q["slug"]}/">{esc(q["title"])}</a></li>' for q in (posts_by_slug[slug] for slug in p['related_slugs']) if q != p)
    tags = ''.join(f'<li>{esc(tag)}</li>' for tag in p.get('tags', []))
    topic_list = f'<ul class="guide-tags" aria-label="Topics">{tags}</ul>' if tags else ''
    updated = f' · Updated <time datetime="{p["modified"]}">{date.fromisoformat(p["modified"]).strftime("%d %B %Y")}</time>' if p.get('modified') and p['modified'] != p['date'] else ''
    
    steps_li = ''.join(f'<li>{esc(st)}</li>' for st in p.get('quick_answer', []))
    quick_answer_row = f'''<div class="quick-answer-card">
<div class="quick-answer-header"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg> Quick Answer · TL;DR</div>
<ol class="quick-answer-steps">{steps_li}</ol>
</div>''' if p.get('quick_answer') else ''

    body = f'''<article class="article-layout blog-portal-grid"><aside class="portal-left-col" aria-label="Table of contents and app download"><div class="left-sticky-wrap"><nav class="portal-toc-box" aria-label="Table of contents"><div class="portal-toc-header">On this page</div><ol class="portal-toc-list">{toc}</ol></nav>{product_download_card}</div></aside><div class="article-content article-main-card"><a href="/blog/" class="portal-back-link">← All guides</a><header class="article-header"><div class="portal-category-badge">{esc(p['category'])}</div><h1>{esc(p['title'])}</h1><p class="byline">By <a href="/blog/about/">FloatBoard</a> · Published <time datetime="{p['date']}">{date.fromisoformat(p["date"]).strftime("%d %B %Y")}</time>{updated}</p>{topic_list}<p class="guide-intro">{esc(p['intro'])}</p></header><figure class="article-hero-figure">{article_media(p)}<figcaption>{esc(p['caption'])}</figcaption></figure>{quick_answer_row}<div class="article-body">{sections}</div><aside class="related"><h2>Related guides &amp; workflows</h2><ul>{related}</ul></aside></div><aside class="article-sidebar portal-right-col" aria-label="Product and alternatives"><div class="sidebar-sticky-wrap">{sidebar_product_card}{sidebar_comparisons_card}{sidebar_resources_card}</div></aside></article>'''
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
