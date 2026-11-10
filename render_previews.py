import os, time
from playwright.sync_api import sync_playwright

BRAVE = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
web_dir = r'c:\Users\danie\Downloads\SF\web'

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=BRAVE if os.path.exists(BRAVE) else None, headless=True)
    
    # 1. Desktop Index Preview
    page1 = browser.new_page(viewport={'width': 1440, 'height': 900})
    page1.goto('file:///' + os.path.join(web_dir, 'index.html').replace('\\', '/'))
    time.sleep(3)
    p1 = os.path.join(web_dir, 'page_preview.png')
    page1.screenshot(path=p1, full_page=False)
    print('Rendered desktop page_preview.png')
    page1.close()

    # 2. Index on Mobile Viewport
    page2 = browser.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    page2.goto('file:///' + os.path.join(web_dir, 'index.html').replace('\\', '/'))
    time.sleep(2)
    p2 = os.path.join(web_dir, 'index_mobile_view.png')
    page2.screenshot(path=p2, full_page=False)
    print('Rendered index_mobile_view.png')
    page2.close()

    # 3. Mobile HTML Dedicated App
    page3 = browser.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    page3.goto('file:///' + os.path.join(web_dir, 'mobile.html').replace('\\', '/'))
    time.sleep(2)
    p3 = os.path.join(web_dir, 'mobile_preview.png')
    page3.screenshot(path=p3, full_page=False)
    print('Rendered mobile_preview.png')
    page3.close()

    browser.close()

print('All web previews captured successfully!')
