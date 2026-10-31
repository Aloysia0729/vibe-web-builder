#!/usr/bin/env python3
"""Validate local README links, anchor targets, bilingual assets and social size."""
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]

def slug(text):
    text = re.sub(r'<[^>]+>|[`*_]', '', text).lower()
    return ''.join(c for c in text if c.isalnum() or c in ' -_').replace(' ', '-')

def check(root=ROOT):
    errors=[]
    paths=[root/'README.md', root/'README.zh-CN.md']
    paths+=list((root/'docs/presentation').glob('*.md'))
    paths+=[root/'assets/demo/README.md']
    for path in paths:
        if not path.exists():
            errors.append(f'Missing: {path.relative_to(root)}'); continue
        content=path.read_text()
        prose=re.sub(r'^```.*?^```\s*$', '',content,flags=re.M|re.S)
        for link in re.findall(r'\[[^\]\n]*\]\(([^)\s]+)\)',prose):
            parts=urlsplit(link)
            if parts.scheme or parts.netloc:continue
            target=(path.parent/unquote(parts.path)).resolve() if parts.path else path
            if not target.is_relative_to(root) or not target.exists():
                errors.append(f'{path.name}: missing {link}');continue
            if parts.fragment and target.suffix=='.md':
                headings=re.findall(r'^#{1,6} (.+)$',target.read_text(),re.M)
                if unquote(parts.fragment) not in {slug(h) for h in headings}:
                    errors.append(f'{path.name}: missing anchor {link}')
        if '<!-- DEMO_MEDIA -->' in content:errors.append(f'{path.name}: unfinished demo slot')
    from PIL import Image
    media=['studio-desktop.png','studio-mobile.png','before-after.png','walkthrough.gif']
    for name in media:
        path=root/'assets/demo'/name
        if not path.is_file():errors.append(f'Missing media: {name}');continue
        try:
            with Image.open(path) as im:
                im.verify()
        except (OSError, ValueError) as error:
            errors.append(f'Invalid image: {name}: {type(error).__name__}')
        if path.stat().st_size>8_000_000:errors.append(f'Oversized: {name}')
    social=root/'assets/branding/social-preview.jpg'
    if not social.exists() or social.stat().st_size>=1_000_000:errors.append('Social cover missing or >=1 MB')
    else:
        try:
            with Image.open(social) as im:
                if abs(im.width/im.height-2)>0.01:errors.append('Social aspect ratio must be 2:1')
        except (OSError, ValueError):
            errors.append('Invalid social cover image')
    # Language versions must expose the same local media and installation command.
    if all(p.exists() for p in [root/'README.md',root/'README.zh-CN.md']):
        en=(root/'README.md').read_text();zh=(root/'README.zh-CN.md').read_text()
        for value in ['assets/branding/hero.png','assets/demo/walkthrough.gif','assets/demo/studio-desktop.png',
                      'v0.1.1','requirements-dev.txt','$skill-installer install https://github.com/Aloysia0729/vibe-web-builder/tree/main/skills/vibe-web-builder']:
            if value not in en or value not in zh:errors.append(f'Bilingual contract mismatch: {value}')
    return errors

if __name__=='__main__':
    failures=check()
    print('\n'.join(failures) if failures else 'PASS: README links/anchors, bilingual assets, image decoding, social dimensions/size')
    sys.exit(bool(failures))
