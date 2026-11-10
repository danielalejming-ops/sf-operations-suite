import sys, os, time, json, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

output_dir = r"c:\Users\danie\Downloads\SF\ig_assets\all_media"
os.makedirs(output_dir, exist_ok=True)

BRAVE = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'

def download_file(url, filepath):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=15) as resp, open(filepath, 'wb') as f:
            f.write(resp.read())
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=BRAVE if os.path.exists(BRAVE) else None, headless=True)
    page = browser.new_page(user_agent=UA, viewport={"width": 1280, "height": 1000})
    
    print("Navigating to https://www.instagram.com/sfentretenimiento1/ ...")
    page.goto("https://www.instagram.com/sfentretenimiento1/", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    
    # Dismiss any login dialogs
    page.evaluate("""
        () => {
            const dialogs = document.querySelectorAll('div[role="dialog"], div[role="presentation"]');
            for (let d of dialogs) d.remove();
            document.body.style.overflow = 'auto';
        }
    """)
    
    # Scroll multiple times to collect all post links
    all_links = set()
    for scroll_idx in range(8):
        links = page.evaluate("""
            () => Array.from(document.querySelectorAll("a[href*='/p/'], a[href*='/reel/']")).map(a => a.getAttribute('href'))
        """)
        for l in links:
            if l: all_links.add(l)
        page.evaluate("window.scrollBy(0, 1200)")
        time.sleep(2)
        # Dismiss dialog if reappeared
        page.evaluate("""
            () => {
                const dialogs = document.querySelectorAll('div[role="dialog"], div[role="presentation"]');
                for (let d of dialogs) d.remove();
                document.body.style.overflow = 'auto';
            }
        """)

    print(f"Total unique post/reel links found after deep scrolling: {len(all_links)}")
    
    collected_items = []
    
    for idx, href in enumerate(list(all_links)):
        full_url = f"https://www.instagram.com{href}" if href.startswith('/') else href
        print(f"Inspecting [{idx+1}/{len(all_links)}]: {full_url}")
        try:
            p_page = browser.new_page(user_agent=UA, viewport={"width": 1280, "height": 900})
            p_page.goto(full_url, wait_until="domcontentloaded", timeout=20000)
            time.sleep(2)
            
            # Dismiss overlays
            p_page.evaluate("""
                () => {
                    const dialogs = document.querySelectorAll('div[role="dialog"], div[role="presentation"]');
                    for (let d of dialogs) d.remove();
                    document.body.style.overflow = 'auto';
                }
            """)
            time.sleep(1)
            
            # Capture clean screenshot of the post
            shot_name = f"post_detail_{idx+1}.png"
            shot_path = os.path.join(output_dir, shot_name)
            p_page.screenshot(path=shot_path)
            
            # Extract image URLs and videos
            media_info = p_page.evaluate("""
                () => {
                    const imgs = Array.from(document.querySelectorAll('article img, main img')).map(i => ({
                        src: i.src,
                        alt: i.alt || ''
                    })).filter(i => i.src && !i.src.includes('150x150') && !i.src.includes('profile_pic'));
                    
                    const videos = Array.from(document.querySelectorAll('video')).map(v => ({
                        src: v.src,
                        poster: v.poster
                    }));
                    
                    const captions = [];
                    document.querySelectorAll('article span, main span, h1').forEach(s => {
                        const t = s.innerText.trim();
                        if (t.length > 15 && !t.includes('Regístrate') && !t.includes('Iniciar sesión')) {
                            captions.push(t);
                        }
                    });
                    
                    return { imgs, videos, captions: captions.slice(0, 5) };
                }
            """)
            
            # Save media files
            saved_images = []
            for img_i, img_data in enumerate(media_info['imgs'][:3]):
                img_file = f"media_{idx+1}_{img_i+1}.jpg"
                img_path = os.path.join(output_dir, img_file)
                if download_file(img_data['src'], img_path):
                    saved_images.append(img_file)
                    
            item_entry = {
                "id": idx + 1,
                "url": full_url,
                "captions": media_info['captions'],
                "screenshot": shot_name,
                "saved_images": saved_images,
                "videos_count": len(media_info['videos'])
            }
            collected_items.append(item_entry)
            p_page.close()
            
        except Exception as e:
            print(f"Error on {full_url}: {e}")
            
    with open(os.path.join(output_dir, "deep_scrape_summary.json"), "w", encoding="utf-8") as f:
        json.dump(collected_items, f, indent=2, ensure_ascii=False)
        
    browser.close()
    print("Deep scraping completed successfully!")
