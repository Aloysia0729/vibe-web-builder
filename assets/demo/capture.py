#!/usr/bin/env python3
"""Capture the actual studio snapshot and clearly labeled transcript replay.
Requires environment-provided Playwright, Chromium and Pillow. No server persists.
"""
from pathlib import Path
import html
import io
import json
import re
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from PIL import Image
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent
RUN=HERE/'recorded-run'

def capture():
    transcript=(RUN/'transcript.txt').read_text()
    chunks=re.split(r'^## Turn (\d+) — (User|Assistant)\s*\n',transcript,flags=re.M)
    turns={(int(chunks[i]),chunks[i+1]):chunks[i+2].strip() for i in range(1,len(chunks),3)}
    site=RUN/'site'
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(site)))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base=f'http://127.0.0.1:{server.server_port}'
    facts={'capture':'actual browser screenshot + explicitly labeled transcript replay','base_is_ephemeral':True,'layouts':[]}
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True)
            page=browser.new_page(viewport={'width':1280,'height':800},device_scale_factor=1)
            page.goto(base,wait_until='networkidle')
            facts['browser']=browser.version
            facts['heading']=page.locator('h1').inner_text()
            page.screenshot(path=str(HERE/'studio-desktop.png'),full_page=True)
            final_frame=page.screenshot()
            for width in [390,1280]:
                page.set_viewport_size({'width':width,'height':800})
                page.goto(base,wait_until='networkidle')
                overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth')
                assert not overflow, f'overflow at {width}'
                facts['layouts'].append({'width':width,'overflow':overflow})
                if width==390:page.screenshot(path=str(HERE/'studio-mobile.png'),full_page=True)
            # This is an editorial replay of real transcript excerpts, not a live terminal recording.
            selections=[('01 / The idea',turns[(1,'User')]),
                        ('02 / Adaptive questions',turns[(1,'Assistant')]),
                        ('03 / Clear requirements',turns[(2,'Assistant')]),
                        ('04 / First confirmation',turns[(3,'User')]),
                        ('05 / Page wireframe',turns[(3,'Assistant')]),
                        ('06 / Independent wireframe approval + build request',turns[(4,'User')])]
            page.set_viewport_size({'width':1280,'height':800})
            frames=[]
            style='body{margin:0;background:#0b1117;color:#d8e9ef;font:25px/1.55 monospace;padding:48px;box-sizing:border-box}small{color:#7aabb5;font:17px monospace}h1{color:#61efae;font:31px monospace;margin:32px 0}pre{white-space:pre-wrap;font:inherit;max-width:1150px}footer{color:#80bfc7;font:18px monospace;position:absolute;bottom:28px}'
            for title,text in selections:
                excerpt=text[:1200]
                if title.startswith('03'):excerpt='\n'.join(line for line in text.splitlines() if line.startswith('- **'))
                if title.startswith('02'):excerpt=text[text.find('1.'): ]
                if title.startswith('05'):excerpt=text.split('```text')[1].split('```')[0].strip()
                excerpt=excerpt.replace('**','')
                page.set_content(f'<style>{style}'+('pre{font-size:19px;line-height:1.3}' if title.startswith('05') else '')+f'</style><small>vibe-web-builder / recorded transcript excerpts / fictional demo</small><h1>{html.escape(title)}</h1><pre>{html.escape(excerpt)}</pre><footer>Paced replay · wait times omitted · complete transcript included</footer>')
                # Ensure visible text stays on screen; limit only excerpt length, never alter its facts.
                frames.append(Image.open(io.BytesIO(page.screenshot())).convert('RGB'))
            frames.append(Image.open(io.BytesIO(final_frame)).convert('RGB'))
            frames[0].save(HERE/'walkthrough.gif',save_all=True,append_images=frames[1:],duration=[4000,6500,6500,4000,6000,6000,6000],loop=0,optimize=True)
            # Before/after is a document comparison, expressly not a screenshot of the Skill UI.
            data=html.escape(turns[(1,'User')]); summary=html.escape('\n'.join(line for line in turns[(2,'Assistant')].splitlines() if line.startswith('- **')).replace('**',''))
            page.set_content(f'<style>{style}body{{font-size:21px}}.grid{{display:grid;grid-template-columns:1fr 1.5fr;gap:40px}}section{{border:1px solid #376367;padding:26px}}pre{{font:20px/1.5 monospace}}h2{{color:#61efae;font:26px monospace}}</style><small>Actual transcript excerpts · fictional studio · comparison graphic, not product UI</small><h1>From “not sure” to a reviewed plan</h1><div class="grid"><section><h2>BEFORE / user input</h2><p>{data}</p></section><section><h2>AFTER / requirements summary</h2><pre>{summary}</pre></section></div><footer>Requirements r2 and wireframe r1 were independently confirmed; see transcript.</footer>')
            page.screenshot(path=str(HERE/'before-after.png'))
            browser.close()
    finally:
        server.shutdown();server.server_close();thread.join(timeout=5)
        facts['temporary_server_closed']=True
    (HERE/'capture-results.json').write_text(json.dumps(facts,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':capture()
