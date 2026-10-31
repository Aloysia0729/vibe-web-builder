from pathlib import Path
import json
from datetime import datetime,timezone
from playwright.sync_api import sync_playwright
root=Path(__file__).parent
out=root/'verification';out.mkdir(exist_ok=True)
report={'time':datetime.now(timezone.utc).isoformat(),'url':'http://127.0.0.1:4187','browser':'system Chromium via Python Playwright','viewports':[],'limitations':['mailto delivery not exercised; .example is a demonstration address','basic keyboard and semantic checks are not a complete accessibility audit']}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for width,height in [(1280,900),(390,844)]:
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  response=page.goto(report['url'],wait_until='networkidle');assert response.status==200
  assert page.locator('h1').count()==1
  assert page.locator('section').count()==5
  assert page.locator('.fiction-label').count()==3
  assert page.locator('form').count()==0
  assert page.locator('a[href="mailto:hello@northstar.example"]').count()==2
  assert page.locator('img').evaluate_all('(imgs)=>imgs.every(i=>i.complete&&i.naturalWidth>0)')
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Horizontal overflow'
  assert page.evaluate("Array.from(document.links).filter(a=>a.getAttribute('href').startsWith('#')).every(a=>document.getElementById(a.hash.slice(1)))")
  navigation=[]
  for target in ['home','services','work','about','contact']:
   page.locator(f'nav a[href="#{target}"]').click()
   assert page.evaluate('location.hash')=='#'+target
   box=page.locator('#'+target).bounding_box()
   assert box['y']<height and box['y']+box['height']>0
   navigation.append({'target':target,'hash':page.evaluate('location.hash'),'section_top':round(box['y'],1)})
  page.locator('footer a').click();assert page.evaluate('location.hash')=='#home'
  page.locator('.hero .button').click();assert page.evaluate('location.hash')=='#work'
  page.goto(report['url'],wait_until='networkidle')
  page.keyboard.press('Tab');assert page.evaluate('document.activeElement.textContent')=='Skip to content'
  assert page.locator('.skip-link').bounding_box()['y']>=0
  page.keyboard.press('Enter');assert page.evaluate('document.activeElement.id')=='main'
  page.goto(report['url'],wait_until='networkidle');page.screenshot(path=str(out/f'site-{width}.png'),full_page=True)
  assert not errors,errors
  report['viewports'].append({'width':width,'height':height,'http_status':response.status,'horizontal_overflow':False,'nav':navigation,'hero_work_link':'passed','back_to_top':'passed','keyboard_skip_link':'passed','image_load':'passed','console_page_errors':errors,'screenshot':f'site-{width}.png'})
  page.close()
 browser.close()
report['result']='passed'
(out/'browser-results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
