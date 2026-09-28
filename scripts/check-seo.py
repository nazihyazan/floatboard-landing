"""Validate indexable static pages and local link destinations."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.canonical=[]; self.h1=0; self.links=[]; self.images=[]; self.schema=[]; self.in_schema=False; self.ids=set(); self.description=[]; self.title=''; self.in_title=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='title': self.in_title=True
        if tag=='link' and a.get('rel')=='canonical': self.canonical.append(a['href'])
        if tag=='meta' and a.get('name')=='description': self.description.append(a['content'])
        if tag=='a': self.links.append(a.get('href',''))
        if tag=='img': self.images.append(a)
        if tag=='script' and a.get('type')=='application/ld+json': self.in_schema=True
    def handle_endtag(self,tag):
        if tag=='script': self.in_schema=False
        if tag=='title': self.in_title=False
    def handle_data(self,data):
        if self.in_schema: self.schema.append(json.loads(data))
        if self.in_title: self.title+=data

def file_for(path):
    p=ROOT / unquote(path).lstrip('/')
    return p/'index.html' if p.is_dir() else p

urls=[e.text for e in ET.parse(ROOT/'sitemap.xml').findall('.//{*}loc')]
assert len(urls)==len(set(urls))
titles=set(); descriptions=set()
for url in urls:
    source=file_for(urlsplit(url).path)
    p=Page(); p.feed(source.read_text())
    assert p.canonical==[url],(url,'canonical')
    assert p.h1==1,(url,'H1')
    assert p.title and p.title not in titles,(url,'title'); titles.add(p.title)
    assert len(p.description)==1 and p.description[0] not in descriptions,(url,'description'); descriptions.add(p.description[0])
    for link in p.links:
        u=urlsplit(link)
        if u.scheme or u.netloc: continue
        target=file_for(u.path) if u.path.startswith('/') else source.parent/u.path if u.path else source
        assert target.exists(),(url,link)
        if u.fragment and u.fragment != '!' and target.suffix=='.html':
            q=Page(); q.feed(target.read_text()); assert u.fragment in q.ids,(url,link)
    for image in p.images:
        if image.get('src','').startswith('/'):
            image_file = file_for(image['src'])
            assert image_file.exists(), image
            if '/blog/assets/' in image['src']:
                signature = image_file.read_bytes()[:8]
                assert (image_file.suffix == '.jpg' and signature.startswith(b'\xff\xd8')) or (image_file.suffix == '.png' and signature == b'\x89PNG\r\n\x1a\n'), image_file
        if '/blog/' in url:
            assert image.get('alt') and image.get('width') and image.get('height'),image
            assert 0 < int(image['width']) < 10000 and 0 < int(image['height']) < 10000, image
    print('PASS',url)
print('Validated',len(urls),'canonical pages, metadata, internal links, images and JSON-LD.')
